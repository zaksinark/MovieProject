from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
import os
print( os.environ.get("FLASK_APP_API_KEY") )



@app.route('/review')
def add_review():
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":session['user_id']
    }
    return render_template('info.html',user=User.my_id(info))

@app.route('/create/movie',methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movie.validate_movie(request.form):
        return redirect('/review')
    info = {
        "stars": request.form["stars"],
        "review": request.form["review"],
        "user_id": session["user_id"]
    }
    Movie.save(info)
    return redirect('/search')

@app.route('/edit/movie/<int:id>')
def edit_movie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":id
    }
    user = {
        "id":session['user_id']
    }
    
    return render_template("info.html",movie=Movie.get_one(info),user=User.my_id(user))

@app.route('/update/movie/<int:id>',methods=['POST'])
def update_movies(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movie.validate_movie(request.form):
        return redirect(f'/edit/movie/{id}')
    info ={
        **request.form,
        'id': id,
        'user_id':session['user_id']
    }
    Movie.update(info)
    return redirect('/info')

@app.route('/info')
def movie_info():
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":id
    }
    user = {
        "id":session['user_id']
    }
    return render_template("info.html", movie=Movie.get_one(info))

@app.route('/destroy/movie/<int:id>')
def destroy_movie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    info = {
        "id":id
    }
    Movie.destroy(info)
    return redirect('/info')