from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import database
import os

app = Flask(__name__)
app.secret_key = "moon_secret_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- LANDING ----------
@app.route("/")
def landing():
    return render_template("landing.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = database.login_user(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect(url_for("home"))   # ✅ FIX
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")




# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


#--------HOME-------------


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/play/<int:song_id>")
def play_song(song_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    song = database.get_song_by_id(song_id)
    return render_template("home.html", selected_song=song)

#--------UPLOAD SONG (ALBUM AUTO CREATE)------------
@app.route("/upload", methods=["POST"])
def upload_song():
    if "user_id" not in session:
        return redirect(url_for("login"))

    file = request.files.get("song_file")
    if not file:
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    file_path = f"uploads/{filename}"
    title = filename

    database.add_song(title, file_path)

    # 🔥 IMPORTANT FIX HERE
    song = database.get_last_song()   # () VERY IMPORTANT

    if song:
        return redirect(url_for("play_song", song_id=song["id"]))

    return redirect(url_for("home"))
    


@app.route("/songs")
def songs():
    if "user_id" not in session:
        return redirect(url_for("login"))

    all_songs = database.get_all_songs()
    return render_template("songs.html", songs=all_songs)




# ---------- FAVOURITES ----------
@app.route("/favourites")
def favourites():
    if "user_id" not in session:
        return redirect(url_for("login"))

    fav_songs = database.get_favourite_songs(session["user_id"])
    return render_template("favourites.html", songs=fav_songs)


# ---------- TOGGLE FAV ----------
@app.route("/toggle-favourite/<int:song_id>")
def toggle_favourite_route(song_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    database.toggle_favourite(session["user_id"], song_id)
    return redirect(request.referrer or url_for("songs"))


# ---------- ALBUMS ----------
@app.route("/albums")
def albums():
    if "user_id" not in session:
        return redirect(url_for("login"))

    albums = database.get_all_albums()
    return render_template("albums.html", albums=albums)

@app.route("/albums/<int:album_id>")
def album_songs(album_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    album = database.get_album_by_id(album_id)
    songs = database.get_songs_by_album(album_id)

    return render_template(
        "album_songs.html",
        album=album,
        songs=songs
    )


# ---------- 404 ----------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)