import sqlite3


DATABASE = "sentinelhub.db"


def get_connection():
    return sqlite3.connect(DATABASE)

def init_database():
    with get_connection() as conn:
        conn.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude1 REAL NOT NULL,
    longitude1 REAL NOT NULL,
    latitude2 REAL NOT NULL,
    longitude2 REAL NOT NULL
)""")
        conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS location_idx ON locations (name);""")
        conn.commit()