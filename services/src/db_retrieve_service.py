from flask import Flask,jsonify, request
from sqlalchemy import *
import sys

app = Flask(__name__)


@app.route("/nexterApi/recommendations/<handle>")
def data(handle):
    from db_helper import DbHelper
    sys.path.append('../../')
    from recommendation_generator import generate_recommendations
    generate_recommendations(handle)
    dbObj = DbHelper()
    data = dbObj.getRecommendation(handle)
    return jsonify(data)


@app.route("/nexterApi/relatedBooks/<handle>")
def related_books(handle):
    from db_helper import DbHelper
    dbObj = DbHelper()
    data = {}
    data["recommendations"] = dbObj.get_related_books_from_feedback(handle)
    return jsonify(data)

@app.route("/nexterApi/feedback", methods=['POST'])
def feedback():
    from db_helper import DbHelper
    try:
        data = request.json
        dbObj = DbHelper()
        dbObj.getFeedback(data)
        return jsonify({})
    except Exception as e:
        print e
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

@app.route("/nexterApi/user/<handle>")
def user(handle):
    from db_helper import DbHelper
    dbObj = DbHelper()
    sys.path.append('../../scripts')
    import tweet_fetcher
    if tweet_fetcher.check_if_user_exists(handle):
        data = dbObj.insert_user(handle)
        return jsonify({})
    return jsonify({}), 500

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == "__main__":
    app.run(debug=True)
