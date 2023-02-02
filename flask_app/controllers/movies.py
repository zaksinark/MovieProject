from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Review
import requests
import os
print( os.environ.get("FLASK_APP_API_KEY") )




@app.route('/search/movie', methods=['POST'])
def search_movies():
    if 'user_id' not in session:
        return redirect('/logout')

    if len(request.form['title']) < 1:
        return redirect('/search')

    session['title'] = request.form['title']
    

    return redirect('/search')

@app.route('/info/<movie_selected>')
def movie_info(movie_selected):
    if 'user_id' not in session:
        return redirect('/logout')
    user = {
        "id":session['user_id']
    }


    MOVIE = movie_selected
    result = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key=203336aef5e949156c0daf7b699052dd&language=en-US&query={MOVIE}&page=1&include_adult=false')
    movie =  result.json()
    print(movie['results'][0])
    return render_template("info.html", movie=movie['results'][0], user=User.my_id(user))

@app.route('/review')
def add_review():
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":session['user_id']
    }
    return render_template('info.html',user=User.my_id(info))

@app.route('/create/review',methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect('/review')
    info = {
        "stars": request.form["stars"],
        "review": request.form["review"],
        "user_id": session["user_id"]
    }
    Review.save(info)
    return redirect('/search')

@app.route('/edit/review/<int:id>')
def edit_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":id
    }
    user = {
        "id":session['user_id']
    }
    
    return render_template("info.html",movie=Review.get_one(info),user=User.my_id(user))

@app.route('/update/review/<int:id>',methods=['POST'])
def update_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Review.validate_movie(request.form):
        return redirect(f'/edit/review/{id}')
    info ={
        **request.form,
        'id': id,
        'user_id':session['user_id']
    }
    Review.update(info)
    return redirect('/info')


@app.route('/destroy/review/<int:id>')
def destroy_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":id
    }
    Review.destroy(info)
    return redirect('/info')