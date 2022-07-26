import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()
salt = '$2b$12$'

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT,
    Password TEXT,
    Token TEXT,
    Secret TEXT,
    Language TEXT DEFAULT 'ru'
    )
    """)
db.commit()


def create_user(username, password, token, secret):
    cursor.execute("""INSERT INTO users (Username, Password, Token, Secret) VALUES (?, ?, ?, ?)""",
                   (username, password + salt, token, secret))
    db.commit()
    return True


def check_user(username):
    cursor.execute("""SELECT * FROM users WHERE Username = ?""", (username,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


def login_user(username, password):
    cursor.execute("""SELECT * FROM users WHERE Username = ? AND Password = ?""",
                   (username, password + salt))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


def get_token_and_secret(username):
    cursor.execute(
        """SELECT Token, Secret FROM users WHERE Username = ?""", (username,))
    user = cursor.fetchone()
    if user:
        return user
    else:
        return False
