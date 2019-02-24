# initial imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask_cors import CORS

import pymongo
from bson.objectid import ObjectId

# instance and config
app = Flask(__name__)
#CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}}, headers='Content-Type')
app.config['TEMPLATES_AUTO_RELOAD'] = True

DB_NAME = 'chicken_2019'
DB_HOST = 'ds149365.mlab.com'
DB_PORT = 49365
DB_USER = 'chicken_eash'
DB_PASS = 'MHYHACK2019'

connection = pymongo.mongo_client.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)


#------------------------------------------------------------------------------


# database connection
# connection = pymysql.connect(host='127.0.0.1', user='root', db='DJPlayList')
# cursor = connection.cursor()


# routes
# Route for handling the login page logic
@app.route("/post", methods=['GET'])
def post():
	print(request.args)

	new_post = {
		"firstname": request.args.get('first name'),
		"lastname": request.args.get('last name'),
		"propic": request.args.get('profile pic url'),
		"gender": request.args.get('gender')
	}
	result = db.patients.insert_one(new_post)
	return ""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('main'))
    return render_template('login.html', error=error)
    
@app.route("/")
def main():
	cursor = db.patients.find({})
	patients = []
	for c in cursor:
		patients.append(c)
	return render_template('index.html', patients=patients)

@app.route("/patient/<string:user_id>")
def patient(user_id):
	cursor = db.patients.find({'_id': ObjectId(user_id)})
	print(cursor[0])
	return render_template('patient.html', patient=cursor[0])


#------------------------------------------------------------------------------


if __name__ == "__main__":
	#app.run()
	app.run()