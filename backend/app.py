from flask import Flask, session
from flask import request
from flask_cors import CORS
import json

app = Flask(__name__)
app.config.update(
    SECRET_KEY='902c099469604592941119474ab86c7e',
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
cors = CORS(app)

# setup database
from database import db_session, add_user, user_exists, user_with_password_exists, get_user_id, get_journal_entry, add_journal_entry, JournalEntry

@app.teardown_appcontext
def shutdown_session(Exception = None):
    db_session.remove()

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


@app.route('/syncChunk', methods=['POST'], endpoint='syncChunk')
def syncChunk():
    if (not isLoggedIn()):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    for i in request.json:
        key = i["key"].split('-')
        id = int(key[0])
        year = int(key[1])
        month = int(key[2])
        day = int(key[3])
        user_id = session['user_id']

        assert(id == user_id)

        text_content = i["textContent"]
        modified_time = i["modifiedTime"]

        entry = get_journal_entry(year, month, day, user_id)

        if (entry is None):
            new_entry = JournalEntry(
                UserId=user_id,
                Year=year,
                Month=month,
                Day=day,
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

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)