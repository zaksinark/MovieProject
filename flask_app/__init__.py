from flask import Flask
app = Flask(__name__)
app.secret_key = "the most secretest key"

DATABASE = 'movie_project'