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

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = login()

        if result == "Login successful":
            session['username'] = username
            return redirect(url_for('watchlist.user_dashboard'))
        else:
            return result

    return render_template('login.html')




def login():
    username = request.form['username']
    password = request.form['password']
    db_file = f"{username}.db"
    if not os.path.exists(db_file):
        return "Login failed. User not found."

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE user_name=?", (username,))
    stored_password = cursor.fetchone()
    connection.close()

    if stored_password and stored_password[0] == password:
        return "Login successful"
    return "Login failed"


