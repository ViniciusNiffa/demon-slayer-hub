import sqlite3
from config import DATABASE
from werkzeug.security import generate_password_hash

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            foto TEXT,
            biografia TEXT,
            respiracao_tipo TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fanarts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            imagem TEXT NOT NULL,
            categoria TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )                
            """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            fanart_id INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (fanart_id) REFERENCES fanarts (id)
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seguidores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seguidor_id INTEGER NOT NULL,
        seguido_id INTEGER NOT NULL,
        FOREIGN KEY (seguidor_id) REFERENCES users (id),
        FOREIGN KEY (seguido_id) REFERENCES users (id)
    )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            fanart_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (fanart_id) REFERENCES fanarts (id)
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            fanart_id INTEGER NOT NULL,
            motivo TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (fanart_id) REFERENCES fanarts (id)
    )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users(nome, email, senha, foto, is_admin)
        VALUES(?, ?, ?, ?, 1)
    """, ('Admin', 'admin@gmail.com', generate_password_hash('aDmin@ç132'), 'default.png'))
    
    conn.commit()
    cursor.close()
    conn.close()