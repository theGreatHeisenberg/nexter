from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from db_retrieve_service import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pankaj:12345@localhost/nexter'
db = SQLAlchemy(app)
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    twitter_handle = db.Column('twitter_handle', db.Unicode)
    created_on = db.Column('created_on', db.Date)
    last_synced = db.Column('last_synced', db.Date)
    is_deleted = db.Column('is_deleted', db.BOOLEAN)

class UserInterests(db.Model):
    __tablename__ = 'user_interests'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    label = db.Column('label', db.Unicode, primary_key=True)
    affinity_score = db.Column('affinity_score',db.Float)

class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column('tag_id', db.Integer, primary_key=True)
    tag = db.Column('tag', db.Unicode)
    label = db.Column('uber_label', db.Unicode)

class UserBookMapping(db.Model):
    __tablename__ = 'user_book_mapping'
    confidence_score = db.Column('confidence_score', db.Float)
    map_user_id = db.Column('user_id', db.Integer, primary_key=True)
    map_book_id = db.Column('book_id', db.Integer, primary_key=True)
    feedback = db.Column('user_feedback',db.Integer)

    def __init__(self, map_user_id, map_book_id,feedback = None,confidence_score = 0.0):
        self.map_user_id = map_user_id
        self.map_book_id = map_book_id
        self.feedback = feedback
        self.confidence_score = confidence_score

class BooksTagsMapping(db.Model):
    __tablename__ = 'books_tags_mapping'
    id = db.Column('id', db.Integer, primary_key=True)
    tag_id = db.Column('tag_id', db.Integer)
    book_id = db.Column('book_id', db.Integer)

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column('book_id', db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String(13))
    #goodreads_book_id = db.Column('goodreads_book_id', db.Integer)
    author = db.Column('author', db.Unicode)
    title = db.Column('title', db.Unicode)
    ratings = db.Column('ratings', db.Float)
    rating_count = db.Column('ratings_count', db.Integer)
    image_url = db.Column('image_url', db.Unicode)
    publication_year = db.Column('original_publication_year', db.Date)

class DbHelper():
    def getRecommendation(self,handle):
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
        return data

    def getFeedback(self, data):
        handle = data['twitter_handle']
        book_id = data['book_id']
        #feedback = data['feedback']
        if data['feedback'] == True:
            feedback = 1
        else:
            feedback = 0

        user = Users.query.filter_by(twitter_handle = handle).first()
        row = db.session.query(UserBookMapping) \
              .filter(UserBookMapping.map_user_id == user.user_id, UserBookMapping.map_book_id == book_id)

        entry = [x for x in row]
        entry[0].feedback = feedback
        print entry[0].map_user_id, entry[0].feedback
        db.session.commit()

    def interested_books(self,uid):
        query = db.session.query(UserInterests) \
            .filter(UserInterests.user_id == uid) \
            .order_by(UserInterests.affinity_score.desc()) \
            .limit(2)
        labels = [x for x in query]
        #print labels[0].label,labels[1].label

        recom_query = db.session.query(UserBookMapping) \
            .filter(UserBookMapping.map_user_id == uid)
        already_recommended = [x.map_book_id for x in recom_query]
        print  'already Recommended:',already_recommended

        booklist_obj = []
        booktag_obj = []
        for each_label in labels:
            query = db.session.query(Tags, BooksTagsMapping) \
                .filter(each_label.label == Tags.label) \
                .filter(Tags.tag_id == BooksTagsMapping.tag_id)
            book_ids_to_show = []
            for tags, book_tag_map in query:
                #book_ids_to_show.append(book_tag_map.book_id)
                if book_tag_map.book_id not in already_recommended:
                    book_ids_to_show.append(book_tag_map.book_id)
                else:
                    pass
                    #print book_tag_map.book_id
            query = db.session.query(Books) \
                .filter(Books.book_id.in_(list(book_ids_to_show))) \
                .order_by(Books.ratings.desc()) \
                .limit(5)
            for book in query:
                one_book = {}
                if book.book_id not in booktag_obj:
                    booktag_obj.append(book.book_id)
                    '''one_book['title'] = book.title.encode('utf-8')
                    one_book['label'] = each_label.label.encode('utf-8')
                    one_book['ratings'] = book.ratings
                    one_book['id'] = book.book_id
                    booklist_obj.append(one_book)
        for x in booklist_obj:
            print x'''
        # print booktag_obj #[4373, 3554, 9569, 3491]
        return booktag_obj

    def update_db_interests(self,uid):
        list_of_update = self.interested_books(uid)
        for book_id in list_of_update:
            try:
                obj = UserBookMapping(uid,book_id)
                db.session.add(obj)
                db.session.commit()
            except:
                pass