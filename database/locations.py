from .database import get_connection

def add_location(name, min_lon, max_lon, min_lat, max_lat):
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO locations (name, longitude1, longitude2, latitude1, latitude2)
                     VALUES (?, ?, ?, ?, ?)""",
                     (name, min_lon, max_lon, min_lat, max_lat))

def get_location(name):
    with get_connection() as conn:
        return conn.execute("""
        SELECT name, longitude1, longitude2, latitude1, latitude2 FROM locations WHERE name = ?""",
                     (name,)).fetchall()

def list_locations():
    with get_connection() as conn:
        return conn.execute("""
        SELECT name, latitude1, longitude1, latitude2, longitude2 FROM locations ORDER BY name""").fetchall()

def remove_location(name):
    with get_connection() as conn:
        conn.execute("""DELETE FROM locations where name = ?""", (name,))