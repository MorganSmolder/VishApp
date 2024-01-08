from flask import Flask
from flask_cors import CORS
from api import bind_api
from database import setup_session, create_all

app = Flask(__name__)
app.config.update(
    SECRET_KEY='902c099469604592941119474ab86c7e',
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
cors = CORS(app)

connection_string = 'mysql://root:password@localhost:3306/JournalAppDb'
db_session = setup_session(connection_string)
create_all()
bind_api(app, db_session)

@app.teardown_appcontext
def shutdown_session(Exception = None):
    db_session.remove()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)