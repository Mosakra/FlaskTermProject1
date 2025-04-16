from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_session import Session
import os
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

file_save_location = "static/images"
allowed_types = [".png", ".jpg"]

def get_games_from_session():
    return session.get("videoGames", [])
@app.route("/", methods=["GET"])
def index():
    games = get_games_from_session()
    return render_template("index.html", games=games, file_location=file_save_location)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        if "videoGames" not in session:
            print("Clearing session data")
            session["videoGames"] = []
        title = request.form.get("title", "invalid")
        plat = request.form.get("plat", "invalid")
        year = request.form.get("year", "invalid")
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            extension = os.path.splitext(uploaded_file.filename)[1]
            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                session["videoGames"].append({"title": title, "plat": plat, "year": year, "image": unique_name})
            else:
                flash("The file is of the wrong type", "error")
                return redirect("./add")


        print(session.get("videoGames"))
        session.modified = True
        flash("Good job! You have added a new game to your collection", "message")
        return redirect("/")

@app.route("/remove", methods=["GET"])
def remove():
    games = get_games_from_session()
    return render_template('remove.html', games=games)

@app.route("/remove_game/<int:index>", methods=["POST"])
def remove_game(index):
    games = get_games_from_session()
    if 0 <= index < len(games):
        game_to_remove = games.pop(index)
        session["videoGames"] = games
        session.modified = True
        image_path = os.path.join(file_save_location, game_to_remove.get("image", ""))
        if os.path.exists(image_path) and game_to_remove.get("image"):
            try:
                os.remove(image_path)
                flash(f'Game "{game_to_remove["title"]}" and its image removed.', 'success')
            except OSError as e:
                flash(f'Error removing image for "{game_to_remove["title"]}": {e}', 'warning')
        else:
            flash(f'Game "{game_to_remove["title"]}" removed.', 'success')
        return redirect(url_for('remove'))
    else:
        flash('Invalid game selection', 'error')
        return redirect(url_for('remove'))

@app.route("/game_inventory")
def game_inventory():
    games = get_games_from_session()
    return render_template("game_inventory.html", games=games, file_location=file_save_location)

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")


