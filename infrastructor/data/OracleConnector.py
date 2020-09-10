import cx_Oracle
import time


class OracleDbConnector:
    def __init__(self, connection_string, host=None, port=None, service_name=None, username=None, password=None):
        self.connection_string = connection_string
        self.host = host
        self.port = port
        self.service_name = service_name
        self.username = username
        self.password = password
        self._tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
        self.connection_string = None
        self.connection = None
        self.cursor = None

    def set_connection_string(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        if self.connection_string is not None:
            self.connection = cx_Oracle.connect(self.connection_string)
        else:
            self.connection = cx_Oracle.connect(self.username, self.password, self._tns, encoding="UTF-8",
                                                nencoding="UTF-8")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

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
