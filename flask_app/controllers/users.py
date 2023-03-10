from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask import jsonify, request
from flask_app.models.user import User
from flask_app.models.movie import Review
import requests
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/get_data')
def get_data():
    return jsonify()

@app.route('/')
def index():
    return render_template('loginreg.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': hash_pw
    }
        
    id=User.save(data)
    session['user_id'] = id

    return redirect('/search')

@app.route('/login',methods=['POST'])
def login():
    user=User.my_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/search')

@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    
    if 'title' in session and len(session['title']) > 1:
        MOVIE = session['title']
        session.pop('title')
        result = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&query={MOVIE}&page=1&include_adult=false')
        movie_list =  result.json()

        return render_template("search.html",user=User.my_id(data), movies=movie_list['results'])

    result = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&page=1')
    movie_list =  result.json()

    return render_template("search.html",user=User.my_id(data), movies=movie_list['results'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

