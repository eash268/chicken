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
@app.route("/post/<q_num>", methods=['GET'])
def post(q_num):

	try:
		print(request.args)
		logger = db.requests.insert_one(request.args.to_dict(flat=False))
	except:
		pass

	query = {
		"firstname": request.args.get('first name'),
		"lastname": request.args.get('last name'),
		"gender": request.args.get('gender'),
		"provider": "Dr. Samarth Sharma",
	}

	response = request.args.get('last clicked button name')

	cursor = db.patients.find(query)
	if cursor.count() == 0:
		print("new user!")
		new_post = {
			"firstname": request.args.get('first name'),
			"lastname": request.args.get('last name'),
			"propic": request.args.get('profile pic url'),
			"gender": request.args.get('gender'),
			"provider": "Dr. Samarth Sharma",
		    "scores": {
		        "depression": {
		        	"q1": [],
		        	"q2": [],
		        	"q3": [],
		        	"q4": [],
		        	"q5": [],
		        	"q6": [],
		        	"q7": [],
		        	"q8": [],
		        	"q9": [],
		        },
		        "anxiety": {},
		        "well-being": {},
		        "PTSD": {}
		    }
		}
		result = db.patients.insert_one(new_post)
	elif cursor.count() == 1:
		print("existing user!")
		user = cursor[0]
		user["scores"]["depression"][q_num].append(response)
		result = db.patients.update(query, user)
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