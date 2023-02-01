from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import user

class Movie:
    
    def __init__(self,data):
        self.id = data['id']
        self.stars = data['stars']
        self.review = data['review']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO movies (stars, review, user_id) VALUES (%(stars)s,%(review)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies JOIN users ON movies.user_id = users.id;"
        results =  connectToMySQL(DATABASE).query_db(query)
        return results
    
    @classmethod
    def  get_one (cls,data):
        query = "SELECT * FROM movies LEFT JOIN users ON users.id = movies.user_id WHERE movies.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            for row in results:
                movie_instance = cls(results[0]) 
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                user_instance = user.User(user_data)
                movie_instance.goer = user_instance
                return movie_instance
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE movies SET stars=%(stars)s, review=%(review)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)