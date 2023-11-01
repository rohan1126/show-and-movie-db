import sqlite3
import re
import os
from flask import Flask, request, render_template, redirect, url_for, session
from AnilistPython import Anilist
from flask import Flask, request, render_template, redirect, url_for
from AnilistPython import Anilist
from tmdbv3api import TMDb, TV
from tmdbv3api import Movie
from flask import Blueprint, render_template


watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/watchlist', methods=['GET', 'POST'])

def add_movie_to_watchlist(username, movie_title, release_date, genre,image):
    db_file = f"{username}.db"
    if not os.path.exists(db_file):
        return "User not found."

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO watchlist (movie_title, release_date, genre) VALUES (?, ?, ?)",
                   (movie_title, release_date, genre))
    connection.commit()
    connection.close()
    return "Movie added to watchlist."

def view_watchlist(username):
    db_file = f"{username}.db"
    if not os.path.exists(db_file):
        return "User not found."

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM watchlist")
    watchlist = cursor.fetchall()

    connection.close()
    return watchlist



@watchlist_bp.route('/user-dashboard', methods=['GET', 'POST'])
def user_dashboard():
    anilist = Anilist()
    if 'username' in session:
        if request.method == 'POST':
            if request.form['action'] == 'add_movie':
                movie_title = request.form['movie_title']
                movie_data = anilist.get_anime(movie_title)
                movie_name = movie_data['name_english']
                release_date = movie_data['starting_time']

                genre = movie_data['genres']
                first_genre = genre[0]
                image = movie_data['cover_image']

                add_movie_to_watchlist(session['username'], movie_name, release_date, first_genre,image)
            elif request.form['action'] == 'logout':
                session.pop('username', None)
                return redirect(url_for('homepage'))

        watchlist = view_watchlist(session['username'])
        return render_template('user_dashboard.html', watchlist=watchlist)

    return redirect(url_for('home'))
