import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    towel_count INTEGER DEFAULT 0,
    debt INTEGER DEFAULT 0
)
""")

conn.commit()


def add_client(name):
    try:
        cursor.execute(
            "INSERT INTO clients (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        return True
    except:
        return False