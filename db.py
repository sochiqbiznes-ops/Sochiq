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

    # CLIENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        barber TEXT,
        received INTEGER DEFAULT 0,
        paid INTEGER DEFAULT 0,
        price INTEGER DEFAULT 2000
    )
    """)

    # ACCESS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS access (
        user_id INTEGER,
        barber TEXT
    )
    """)

    conn.commit()
    conn.close()