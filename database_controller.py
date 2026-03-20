import sqlite3
import json

class database_controller:
    def __init__(self, db_path="events.db"):
        self.db_path = db_path
        print("database_controller initialized")

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def init_event_db(self):
        con = self._connect()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS event(
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                description TEXT NOT NULL,
                location  TEXT NOT NULL,
                start     TEXT NOT NULL,
                duration  TEXT NOT NULL,
                food      INTEGER NOT NULL,
                media     TEXT NOT NULL
            )
        """)
        con.commit()
        con.close()

    def init_channel_db(self):
        con = self._connect()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS server_channels(
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id  TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                UNIQUE(server_id, channel_id)
            )
        """)
        con.commit()
        con.close()

    def insert_channel(self, server_id, channel_id):
        con = self._connect()
        cur = con.cursor()

        cur.execute(
            "INSERT OR IGNORE INTO server_channels(server_id, channel_id) VALUES (?, ?)",
            (str(server_id), str(channel_id))
        )
        con.commit()
        con.close()

    def retrieve_channels(self, server_id):
        con = self._connect()
        cur = con.cursor()
        cur.execute(
            "SELECT channel_id FROM server_channels WHERE server_id = ?",
            (str(server_id),)
        )
        rows = cur.fetchall()
        con.close()
        return [row[0] for row in rows]

    def delete_channel(self, server_id, channel_id):
        con = self._connect()
        cur = con.cursor()
        cur.execute(
            "DELETE FROM server_channels WHERE server_id = ? AND channel_id = ?",
            (str(server_id), str(channel_id))
        )
        affected = cur.rowcount
        con.commit()
        con.close()
        return affected > 0

    def init_source_db(self):
        con = sqlite3.connect("sources.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS discord(id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, timestamp TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS mail(id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, body TEXT, timestamp TEXT)")
        con.commit()
        con.close()

    def insert_event(self, name, description, location, start, duration, food, media):
        con = self._connect()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO event(name, description, location, start, duration, food, media) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, description, location, start, duration, int(food), json.dumps(media))
        )
        con.commit()
        con.close()
    
    def delete_event(self, event_id):
        con = self._connect()
        cur = con.cursor()

        cur.execute("DELETE FROM event WHERE id = ?", (event_id,))
        hasChanged = cur.rowcount

        con.commit()
        con.close()

        return hasChanged > 0

    def retrieve_events(self):
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT id, name, description, location, start, duration, food, media FROM event")
        rows = cur.fetchall()
        con.close()

        events = []
        for row in rows:
            events.append({
                "id":          row[0],
                "name":        row[1],
                "description": row[2],
                "location":    row[3],
                "start":       row[4],
                "duration":    row[5],
                "food":        bool(row[6]),
                "media":       json.loads(row[7]),
            })
        return events

    def retrieve_event(self, event_id):
        con = self._connect()
        cur = con.cursor()
        cur.execute("SELECT id, name, description, location, start, duration, food, media FROM event WHERE id = ?", (event_id,))
        row = cur.fetchone()
        con.close()

        if row is None:
            return None

        return {
            "id":          row[0],
            "name":        row[1],
            "description": row[2],
            "location":    row[3],
            "start":       row[4],
            "duration":    row[5],
            "food":        bool(row[6]),
            "media":       json.loads(row[7]),
        }