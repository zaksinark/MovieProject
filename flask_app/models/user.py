from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import movie
from flask_app import DATABASE

class User:
    
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,email,password) VALUES(%(name)s,%(email)s,%(password)s)"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def my_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def my_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN movies ON users.id = movies.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            movie_list = []

            this_user = cls(results[0])
            for row in results:
                movie_info = {
                    **row,
                    'id' : row['movies.id'],
                    'created_at' : row['movies.created_at'],
                    'updated_at' : row['movies.updated_at']
                }
                this_movie = movie.Movie(movie_info)
                movie_list.append(this_user)
            this_user.goer = movie_list
            return this_movie
        return False

    @staticmethod
    def validate(user):
        valid = True
        
        if len(user['name']) < 3:
            flash("First name must be at least 3 characters","register")
            valid= False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            valid= False

        elif not user['password'] == user['confirm']:
            flash("Passwords don't match","register")
            valid= False

        if len(user['email']) <= 1:
            valid=False
            return valid

        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            valid=False
            return valid

        else: email_dictionary = {
            'email':user['email']
        }
        
        my_user = User.my_email(email_dictionary)

        if my_user:
            valid = False
            flash("Email already taken.","register")
        
        return valid