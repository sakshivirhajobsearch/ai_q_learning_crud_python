import sqlite3

DB_NAME = "q_values.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS q_values (
        state TEXT,
        action TEXT,
        value REAL,
        PRIMARY KEY (state, action)
    )
    """)
    conn.commit()
    conn.close()
