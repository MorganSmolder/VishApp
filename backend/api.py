from flask import Flask, session, jsonify
from flask import request
import json
import time

from database import JournalEntry, User

def bind_api(app, db_session):
    def isLoggedIn():
        return 'username' in session;

    # public API
    @app.route('/tst', methods=['GET'], endpoint='tst')
    def submit():
        return {"HI":0}

    @app.route('/getUser', methods=['GET'], endpoint='getUser')
    def index():
        isLoggedIn = 'username' in session
        username = session['username'] if isLoggedIn else ''
        return {
            "isLoggedIn":isLoggedIn,
            "username":username, 
            "userId":session.get("user_id")
        }

    @app.route('/signOut', methods=['GET'], endpoint='signOut')
    def signOut():
        session.clear()
        return {}
    
    def user_with_password_exists(username, password):
        user = db_session.query(User).filter_by(Name=username, Password=password).first()
        return user is not None


    def add_user(username, password):
        epoch_time = int(time.time())
        new_user = User(Name=username, Password=password,JoinPoint=epoch_time)
        db_session.add(new_user)
        db_session.commit()
        return True

    def get_user_id(username, password):
        user = db_session.query(User).filter_by(Name=username,Password=password).first()
        return user.Id

    def user_exists(username):
        user = db_session.query(User).filter_by(Name=username).first()
        return user is not None


    def get_journal_entry(year, month, day, user_id):
        entry = db_session.query(JournalEntry).filter_by(Year=year,Month=month,Day=day,UserId=user_id).first()
        return entry

    def add_journal_entry(new_entry):
        db_session.add(new_entry)
        db_session.commit()

    @app.route('/signIn', methods=['POST'], endpoint='signIn')
    def signIn():
        username = request.json['username']
        password = request.json['password']

        didSucceed = user_with_password_exists(username, password)
        
        if didSucceed:
            session['username'] = username
            session['user_id'] = get_user_id(username, password)

        return {
            "isLoggedIn":didSucceed,
            "username":username, 
            "userId":session.get("user_id"),
            "message": "" if didSucceed else "No user found with given email/password"
        }

    @app.route('/signUp', methods=['POST'], endpoint='signUp')
    def signIn():
        username = request.json['username']
        password = request.json['password']

        didSucceed = not user_exists(username) and add_user(username, password)

        if didSucceed:
            session['username'] = username
            session['user_id'] = get_user_id(username, password)

        return {
            "isLoggedIn":didSucceed,
            "username":username, 
            "userId":session.get("user_id"),
            "message": "" if didSucceed else "User with given details already exists"
        }

    class Key:
        def __init__(self, year, month, day, user_id) -> None:
            self.year = year
            self.month = month
            self.day = day
            self.user_id = user_id
            pass

    def parseKey(json):
        try:
            key = request.json["key"].split('-')
            year = int(key[0])
            month = int(key[1])
            day = int(key[2])
            user_id = session['user_id']
            return Key(year, month, day, user_id)
        except:
            return None

    @app.route('/getEntriesForMonth', methods=['POST'], endpoint='getEntriesForMonth')
    def getEntriesForMonth():
        year = request.json["year"]
        month = request.json["month"]
        user_id = session.get("user_id")
        entries = None
        entries = db_session.query(JournalEntry).filter_by(Year=year,Month=month,UserId=user_id).all()
        entries = [i.Day for i in entries if i.Content != ""]
        return json.dumps({'entries':entries}), 200, {'ContentType':'application/json'} 

    @app.route('/getEntry', methods=['POST'], endpoint='getEntry')
    def getEntry():
        key = request.json["key"].split('-')
        user_id = int(key[0])
        year = int(key[1])
        month = int(key[2])
        day = int(key[3])

        entry = None
        if(user_id == session["user_id"]):        

            entry = db_session.query(JournalEntry).filter_by(Year=year,Month=month,Day=day,UserId=user_id).first()

            if (entry is not None):
                entry = {
                    "textContent":entry.Content,
                    "modifiedTime":entry.LastModified
                }

        return json.dumps({'entry':entry}), 200, {'ContentType':'application/json'} 

    class LoginInfo:
        def __init__(self, username, user_id):
            self.username = username
            self.user_id = user_id
            self.logged_in = user_id is not None

        @staticmethod
        def Get():
            user_id = session.get("user_id")
            username = session.get("username")
            return LoginInfo(username, user_id)


    class Key:
        def __init__(self, user_id, year, month, day):
            self.user_id = user_id
            self.year = year
            self.month = month
            self.day = day

    def parseKey(s):
        key = s.split('-')
        id = int(key[0])
        year = int(key[1])
        month = int(key[2])
        day = int(key[3])
        return Key(id, year, month, day)
        
    from datetime import datetime, timedelta

    @app.route('/getStreak', methods=['POST'], endpoint='getStreak')
    def getStreak():
        key = parseKey(request.json["key"])

        # Retrieve all entries for the user from the database
        entries = db_session.query(JournalEntry).filter_by(UserId=key.user_id).order_by(
            JournalEntry.Year,
            JournalEntry.Month,
            JournalEntry.Day).all()
        entries.reverse()

        for entry in entries:
            entry.datetime = datetime(entry.Year, entry.Month, entry.Day)

        output_key = 'streak'
        if not entries:
            return jsonify({output_key: 0})

        now = datetime(key.year, key.month, key.day)
        current = now
        have_entry_today = entries[0].datetime == now

        if not have_entry_today:
            yesterday = now - timedelta(days = 1)
            current = yesterday
            have_entry_yesterday = entries[0].datetime == yesterday
            if not have_entry_yesterday:
                return jsonify({output_key: 0})

        streak = 0
        for entry in entries:
            if entry.datetime != current:
                break
            streak += 1
            current = current - timedelta(days=1)
        
        return jsonify({'streak': streak})

    @app.route('/syncChunk', methods=['POST'], endpoint='syncChunk')
    def syncChunk():
        if (not isLoggedIn()):
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        for i in request.json:
            key = parseKey(i["key"])
            user_id = session['user_id']

            assert(key.user_id == user_id)

            text_content = i["textContent"]
            modified_time = i["modifiedTime"]

            entry = get_journal_entry(key.year, key.month, key.day, user_id)

            if (entry is None):
                new_entry = JournalEntry(
                    UserId=user_id,
                    Year=key.year,
                    Month=key.month,
                    Day=key.day,
                    LastModified=modified_time, 
                    Content=text_content
                )
                add_journal_entry(new_entry)
            else:
                if(entry.LastModified > modified_time):
                    # discard the edit
                    pass
                else:
                    print(f"Updating: {text_content}")
                    entry.Content = text_content
                    db_session.commit()

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    @app.route('/')
    def index():
        return {"Working":True}
