from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import user

class Review:
    
    def __init__(self,data):
        self.id = data['id']
        self.stars = data['stars']
        self.review = data['review']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO reviews (stars, review, user_id) VALUES (%(stars)s,%(review)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews JOIN users ON reviews.user_id = users.id;"
        results =  connectToMySQL(DATABASE).query_db(query)
        return results
    
    @classmethod
    def  get_one (cls,data):
        query = "SELECT * FROM reviews LEFT JOIN users ON users.id = reviews.user_id WHERE reviews.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            for row in results:
                review_instance = cls(results[0]) 
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                user_instance = user.User(user_data)
                review_instance.goer = user_instance
                return review_instance
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET stars=%(stars)s, review=%(review)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)