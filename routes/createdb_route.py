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

db_bp = Blueprint('createdb', __name__)

@db_bp.route('/db', methods=['GET','POST'])


def is_valid_password(password):
    return len(password) >= 8 and re.search(r'\d', password) is not None

def create_user_database(username, password):
    db_file = f"{username}.db"

    if os.path.exists(db_file):
        return "Username already exists."

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            movie_title TEXT,
            release_date TEXT,
            genre TEXT
        )
    """)

    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_name TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (user_name, password) VALUES (?, ?)", (username, password))

    connection.commit()
    connection.close()
    return "User created successfully."


@db_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_valid_password(password):
            result = create_user_database(username, password)
            if result == "User created successfully.":
                # Redirect to the user_dashboard route upon successful signup
                session['username'] = username  # Store the username in the session
                return redirect(url_for('watchlist.user_dashboard'))
            else:
                return result
        else:
            return "Invalid password. Password must be at least 8 characters long and contain at least one digit."

    return render_template('signup.html')