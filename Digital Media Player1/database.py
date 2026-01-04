import sqlite3
import os

# ---------------- PATH ----------------
os.makedirs("database", exist_ok=True)
DB_PATH = "database/media.db"


# ---------------- CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- TABLES ----------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # ALBUMS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        image_path TEXT
    )
    """)

    # SONGS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        file_path TEXT UNIQUE NOT NULL,
        album_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (album_id) REFERENCES albums(id)
    )
    """)

    # FAVOURITES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favourites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, song_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (song_id) REFERENCES songs(id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- DEFAULT USER ----------------
def create_default_user():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username=?", ("admin",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin")
        )

    conn.commit()
    conn.close()


# ---------------- AUTH ----------------
def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )

    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None




# ---------------- ALBUMS ----------------
def get_or_create_album(name, image_path=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM albums WHERE name=?", (name,))
    row = cur.fetchone()

    if row:
        album_id = row["id"]
    else:
        cur.execute(
            "INSERT INTO albums (name, image_path) VALUES (?, ?)",
            (name, image_path)
        )
        album_id = cur.lastrowid

    conn.commit()
    conn.close()
    return album_id


def get_all_albums():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, image_path FROM albums")
    rows = cur.fetchall()

    conn.close()
    return rows


# ---------------- SONGS ----------------
def add_song(title, file_path, album_id=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO songs (title, file_path, album_id)
        VALUES (?, ?, ?)
    """, (title, file_path, album_id))

    conn.commit()
    conn.close()


def get_all_songs():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, file_path
        FROM songs
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_song_by_id(song_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, file_path
        FROM songs
        WHERE id=?
    """, (song_id,))

    row = cur.fetchone()
    conn.close()
    return row


def get_last_song():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, file_path
        FROM songs
        ORDER BY created_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()
    return row
def get_songs_by_albums(album_id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT id, title, file_path
                FROM songs
                WHERE albums_id=?
                ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------- FAVOURITES ----------------
def toggle_favourite(user_id, song_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM favourites
        WHERE user_id=? AND song_id=?
    """, (user_id, song_id))

    row = cur.fetchone()

    if row:
        cur.execute("""
            DELETE FROM favourites
            WHERE user_id=? AND song_id=?
        """, (user_id, song_id))
    else:
        cur.execute("""
            INSERT INTO favourites (user_id, song_id)
            VALUES (?, ?)
        """, (user_id, song_id))

    conn.commit()
    conn.close()


def get_favourite_songs(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            songs.id,
            songs.title,
            songs.file_path,
            albums.name AS album_name,
            albums.image_path
        FROM favourites
        JOIN songs ON favourites.song_id = songs.id
        LEFT JOIN albums ON songs.album_id = albums.id
        WHERE favourites.user_id=?
        ORDER BY favourites.created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows

# ---------------- ALBUM BY ID ----------------
def get_album_by_id(album_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, image_path
        FROM albums
        WHERE id=?
    """, (album_id,))

    row = cur.fetchone()
    conn.close()
    return row


# ---------------- SONGS BY ALBUM ----------------
def get_songs_by_album(album_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, file_path
        FROM songs
        WHERE album_id=?
        ORDER BY created_at DESC
    """, (album_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# ---------------- INIT ----------------
create_tables()
create_default_user()