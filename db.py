import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value REAL
)
""")
conn.commit()


def add(v):
    cur.execute("INSERT INTO history (value) VALUES (?)", (v,))
    conn.commit()


def get(limit=200):
    cur.execute("SELECT value FROM history ORDER BY id DESC LIMIT ?", (limit,))
    return list(reversed([x[0] for x in cur.fetchall()]))
