from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
app = Flask(__name__)
from db_helper import DbHelper

@app.route("/data/<handle>")
def data(handle):
	dbObj = DbHelper()
	data = dbObj.getRecommendation(handle)
	return jsonify(data)

@app.route("/feedback",methods = ['POST'])
def feedback():
	try:
		data = request.json
		dbObj = DbHelper()
		dbObj.getFeedback(data)
		return jsonify({})
	except:
		return jsonify({}),500

if __name__ == "__main__":
	app.run(debug=True)
