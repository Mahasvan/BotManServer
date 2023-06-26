import sqlite3


class Database:
    def __init__(self, dbfile: str = "service/database.db"):
        self.dbfile = dbfile
        self.connection = sqlite3.connect(self.dbfile)
        self.cursor = self.connection.cursor()

    def execute(self, query: str, *args):
        self.cursor.execute(query, *args)
        self.connection.commit()

    def fetchone(self, query: str, *args):
        self.cursor.execute(query, *args)
        return self.cursor.fetchone()

    def fetchall(self, query: str, *args):
        self.cursor.execute(query, *args)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()
