import sqlite3
import queries


class DBMan:
    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self._conn as con:
            con.executescript(queries.init_db)

    def insert_file(self):
        raise NotImplementedError

    def remove_file(self):
        raise NotImplementedError
