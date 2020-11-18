import sqlite3


class Storage:
    """
    Abstraction over the sqlite3 database to make it easy to use from
    the App.
    """

    def __init__(self, config):
        self.config = config
        self.conn = sqlite3.connect(config.SQLITE_DB_PATH)
        self.create_table()

    def create_table(self):
        """
        Creates the table only if it doesn't exist.
        """
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS monitoria (ts integer, code integer)")

    def set(self, unix_ts: int, code: int):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO monitoria (ts, code) VALUES (?, ?)",
            (unix_ts, code),
        )
        self.conn.commit()
        return c.lastrowid

    def items(self):
        c = self.conn.cursor()
        for row in c.execute("SELECT ts, code FROM monitoria ORDER BY ts DESC"):
            yield (row[0], row[1])
