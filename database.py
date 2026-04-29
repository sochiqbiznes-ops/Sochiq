import sqlite3

conn = sqlite3.connect("crm.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price INTEGER DEFAULT 0,
    taken INTEGER DEFAULT 0,
    paid INTEGER DEFAULT 0
)
""")

conn.commit()


def add_client(name):
    cur.execute("INSERT OR IGNORE INTO clients (name) VALUES (?)", (name,))
    conn.commit()


def get_clients():
    cur.execute("SELECT name FROM clients")
    return cur.fetchall()


def get_client(name):
    cur.execute("SELECT * FROM clients WHERE name=?", (name,))
    return cur.fetchone()


def update_field(name, field, value):
    cur.execute(f"UPDATE clients SET {field} = {field} + ? WHERE name=?", (value, name))
    conn.commit()


def set_field(name, field, value):
    cur.execute(f"UPDATE clients SET {field}=? WHERE name=?", (value, name))
    conn.commit()