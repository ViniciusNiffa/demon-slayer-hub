import sqlite3
from config import DATABASE
from werkzeug.security import generate_password_hash

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            foto TEXT,
            biografia TEXT,
            is_admin INTEGER DEFAULT 0
            )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS fanarts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            image blob NOT NULL,
            categoria TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )                
            """)
    conn.execute("""
        INSERT OR IGNORE INTO users
    """)