from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
#from db_retrieve_model import Users, UserBookMapping, Books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pankaj:12345@localhost/nexter'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    twitter_handle = db.Column('twitter_handle', db.Unicode)
    created_on = db.Column('created_on', db.Date)
    last_synced = db.Column('last_synced', db.Date)
    is_deleted = db.Column('is_deleted', db.BOOLEAN)

class UserBookMapping(db.Model):
    __tablename__ = 'user_book_mapping'
    mapping_id = db.Column('mapping_id', db.Integer, primary_key=True)
    confidence_score = db.Column('confidence_score', db.Float)
    map_user_id = db.Column('user_id', db.Integer)
    map_book_id = db.Column('book_id', db.Integer)

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column('book_id', db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String(13))
    goodreads_book_id = db.Column('goodreads_book_id', db.Integer)
    author = db.Column('author', db.Unicode)
    title = db.Column('title', db.Unicode)
    ratings = db.Column('ratings', db.Float)
    rating_count = db.Column('rating_count', db.Integer)
    image_url = db.Column('image_url', db.Unicode)
    publication_year = db.Column('original_publication_year', db.Date)

@app.route("/data/<handle>")
def data(handle):
    data = {}
    data['twitter_handle'] = handle

    recommendation_query = db.session.query(Users, UserBookMapping, Books) \
        .filter(Users.twitter_handle == handle) \
        .filter(Users.user_id == UserBookMapping.map_user_id) \
        .filter(UserBookMapping.map_book_id == Books.book_id)

    list_of_recommendation = []
    for object in recommendation_query:
        recommendation = {}
        user, mapping, book = object
        recommendation['title'] = book.title
        recommendation['author'] = book.author
        recommendation['isbn'] = book.isbn
        recommendation['book_id'] = book.book_id
        recommendation['original_publication_year'] = book.publication_year
        recommendation['ratings'] = book.ratings
        recommendation['image_url'] = book.image_url
        recommendation['confidence_score'] = mapping.confidence_score
        list_of_recommendation.append(recommendation)
    data['recommendations'] = list_of_recommendation
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
