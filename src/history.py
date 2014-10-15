import datetime
import sqlite3

class History:
    def __init__(self, db_name):
        """
        TODO:
            - Check if table exists, if not then create it
        """
        self._db_name = db_name
        #self._create_table()

    def _create_table(self):
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('''
            CREATE TABLE history(
              id INTEGER PRIMARY KEY,
              timestamp TEXT,
              script TEXT,
              output TEXT)
        ''')
        db.commit()

    def get_timestamp(self):
        """Returns current timestamp"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self, script_name, output):
        """Write output to database"""
        if not isinstance(output, str):
            output = '\\n'.join(map(str, output))
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('INSERT INTO history(timestamp, script, output) VALUES(?,?,?)',
                    (self.get_timestamp(),script_name, output))
        db.commit()

    def get_all(self, script_name):
        """
        Return all output history of script
        """
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('SELECT timestamp, output FROM history WHERE script=? ORDER BY timestamp DESC',
                    (script_name,))
        data = all_rows = cur.fetchall()
        return data

    def get_last(self, script_name, limit=1):
        """
        Return most recent output from the .history file
        """
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('SELECT timestamp, output FROM history WHERE script=? ORDER BY timestamp DESC LIMIT ?',
                    (script_name, limit,))
        data = all_rows = cur.fetchall()
        return data