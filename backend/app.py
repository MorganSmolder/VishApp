from flask import Flask, session
from flask import request
from flask_cors import CORS

app = Flask(__name__)
# app.secret_key = '902c099469604592941119474ab86c7e'
app.config.update(
    SECRET_KEY='902c099469604592941119474ab86c7e',
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
cors = CORS(app)


# setup database
from database import db_session, add_user, user_exists, user_with_password_exists

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# public API
@app.route('/tst', methods=['GET'], endpoint='tst')
def submit():
    if request.method == 'GET':
        return {"HI":0}
    else:
        return 'Only POST requests are allowed'

@app.route('/submit', methods=['POST'], endpoint='submit')
def submit():
    if request.method == 'POST':
        # Access form data or JSON data sent in the POST request
        data = request.form  # For form data
        data = request.json  # For JSON data if sent
        
        # Process the received data (for demonstration, returning as JSON)
        return {'received_data': data}
    else:
        return 'Only POST requests are allowed'

@app.route('/getUser', methods=['GET'], endpoint='getUser')
def index():
    isLoggedIn = 'username' in session
    username = session['username'] if isLoggedIn else ''
    return {
        "isLoggedIn":isLoggedIn,
        "username":username
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

    return {
        "didFindUser" : didSucceed
    }

@app.route('/signUp', methods=['POST'], endpoint='signUp')
def signIn():
    username = request.json['username']
    password = request.json['password']

    didSucceed = not user_exists(username) and add_user(username, password)

    if didSucceed:
        session['username'] = username

    return {
        "didSucceed" : didSucceed
    }

@app.route('/')
def index():
    return {"Working":True}

if __name__ == "__main__":
    from waitress import serve
    # with app.app_context():
    #     db.create_all()
    serve(app, host="0.0.0.0", port=8080)