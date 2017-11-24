from flask import Flask,jsonify
from sqlalchemy import *

app = Flask(__name__)
from db_helper import DbHelper


@app.route("/data/<handle>")
def data(handle):
    dbObj = DbHelper()
    data = dbObj.getRecommendation(handle)
    return jsonify(data)


@app.route("/feedback", methods=['POST'])
def feedback():
    try:
        data = request.json
        dbObj = DbHelper()
        dbObj.getFeedback(data)
        return jsonify({})
    except:
        return jsonify({}), 500
'''
@app.route("/interest/<uid>")
def user_interest(uid):
    try:
        dbObj = DbHelper()
        dbObj.update_db_interests(uid)
        return jsonify({})
    except:
        return jsonify({}),500
    #print data
    #return jsonify(data)
'''
if __name__ == "__main__":
    app.run(debug=True)
