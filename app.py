from flask import Flask, request, render_template, redirect, url_for
from flask import Flask
from routes.watchlist_route import watchlist_bp
from routes.login_route import login_bp
from routes.createdb_route import db_bp


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key



app.register_blueprint(login_bp)
app.register_blueprint(db_bp)
app.register_blueprint(watchlist_bp)


@app.route('/')
def homepage():
    return render_template('index.html')

# anilist = Anilist()
#     if request.method == 'POST':
#         user_show = request.form['show_name']
#         data = anilist.get_anime(user_show)
#         if data:
#             return render_template('anime_info.html', data=data)
#         else:
#             return "Anime not found. Please try another title."

if __name__ == "__main__":
    app.run(debug=True)
