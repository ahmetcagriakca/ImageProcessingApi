
import pyodbc
from infrastructor.logging.ConsoleLogger import ConsoleLogger


class MssqlDbConnector:
    def __init__(self,  host, database, username, password):
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.host = host
        self.db = database
        self.username = username
        self.password = password
        self.connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
            self.driver, self.host, self.db, self.username, self.password)

        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insert(self, executable_script):
        self.cursor.execute(executable_script)
        self.connection.commit()
        
    # bulk insert
    # Getting insert script from sql_builder
    def bulk_insert(self, data, script):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.prepare(script)  ##statment prepared from sql_builder
            self.cursor.executemany(None, data)  ##insert
            self.connection.commit()
            self.cursor.close()
        finally:
            pass
            # if self.cursor is not None:
            #    self.cursor.close()
