from flask import Flask
from flask import request
from flaskext.mysql import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'JournalAppDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Change this if your database is hosted elsewhere
app.config['MYSQL_DATABASE_PORT'] = 3306  # Change if necessary

mysql = MySQL()
mysql.init_app(app)

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


@app.route('/')
def index():
    # Example query
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM User")
    data = cursor.fetchall()
    cursor.close()

    sql = ('INSERT INTO {} (date, time, tag, power) VALUES '
       '(%s, %s, %s, %s)'.format(self.db_scan_table))

    # Process data or render template
    return str(data)  # For demonstration purposes, returning fetched data as a string

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)