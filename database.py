import sqlite3

DB = "ecochat.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        voice_path TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id TEXT,
        receiver_id TEXT,
        text TEXT,
        audio_path TEXT
    )
    """)

    con.commit()
    con.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized")
