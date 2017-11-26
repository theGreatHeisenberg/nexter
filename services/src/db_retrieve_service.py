from flask import Flask,jsonify
from sqlalchemy import *

app = Flask(__name__)


@app.route("/data/<handle>")
def data(handle):
    from db_helper import DbHelper
    dbObj = DbHelper()
    data = dbObj.getRecommendation(handle)
    return jsonify(data)


@app.route("/feedback", methods=['POST'])
def feedback():
    from db_helper import DbHelper
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
