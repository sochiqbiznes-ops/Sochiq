import sqlite3

DB_NAME = "crm.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cur = conn.cursor()

    # BARBERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS barbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()