
from datetime import datetime
import sqlite3

class Log:
    def __init__(self, dbName):
        """
        TODO:
            - Check if table exists, if not then create it
        """
        self._db_name = dbName
        #self._create_table()

    def _create_table(self):
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('''
            CREATE TABLE log(
              id INTEGER PRIMARY KEY,
              timestamp TEXT,
              type TEXT,
              message TEXT)
        ''')
        db.commit()

    def get_timestamp(self):
        """returns a current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_message(self, type, message):
        """Write logs to database"""
        db = sqlite3.connect(self._db_name)
        cur = db.cursor()
        cur.execute('INSERT INTO log(timestamp, type, message) VALUES(?,?,?)',
                    (self.get_timestamp(),type, message))
        db.commit()

    def info(self, message):
        """Log INFO messages"""
        self.log_message('INFO', message)

    def warning(self, message):
        """Log WARNING messages"""
        self.log_message('WARNING', message)

    def error(self, message):
        """Log ERROR messages"""
        self.log_message('ERROR', message)