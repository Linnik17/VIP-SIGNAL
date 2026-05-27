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


def add_value(v: float):
    cur.execute("INSERT INTO history (value) VALUES (?)", (v,))
    conn.commit()


def get_history(limit=200):
    cur.execute("SELECT value FROM history ORDER BY id DESC LIMIT ?", (limit,))
    return [x[0] for x in reversed(cur.fetchall())]
