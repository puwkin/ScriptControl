import datetime
import sqlite3
import os


class History:
    def __init__(self, db_name):
        """
        TODO:
            - Check if table exists, if not then create it
        """
        self._db_name = db_name
        if not os.path.exists(self._db_name):
            #create new DB, create table stocks
            db = sqlite3.connect(self._db_name)
            cur = db.cursor()
            cur.execute('''CREATE TABLE history(
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                script TEXT,
                output TEXT)''')
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

    def get_last_run(self, script_name):
        """
        Return last run time from the .history file
        """
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('SELECT timestamp FROM history WHERE script=? ORDER BY timestamp DESC LIMIT 1',
                    (script_name,))
        data = all_rows = cur.fetchall()
        if data:
            return data[0][0]
        else:
            return 'Never'