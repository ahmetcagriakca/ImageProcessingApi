import pyodbc

from infrastructor.Cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionStrategy import ConnectionStrategy
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.data.MssqlConnector import MssqlDbConnector
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from infrastructor.logging.SqlLogger import SqlLogger


class MssqlConnectionStrategy(ConnectionStrategy):
    def __init__(self, crypto_service: CryptoService, sql_logger: SqlLogger):
        self.sql_logger = sql_logger
        self.mssql_connector: MssqlDbConnector = None
        self.database_manager: DatabaseManager = None
        self.crypto_service: CryptoService = crypto_service

    def make_connection(self, pdi_data, executable_script):
        user = 'ONENT_PYTH'
        password = 'Pyth123'
        if pdi_data[8] is not None:
            user = self.crypto_service.decrypt_code(pdi_data[8].encode())
        if pdi_data[9] is not None:
            password = self.crypto_service.decrypt_code(pdi_data[9].encode())
        #            connectionString=""
        #            mssql='DRIVER={ODBC Driver 13 for SQL Server};'
        #            connectionString=f"{mssql}SERVER={pdiDATA[6]};DATABASE={pdiDATA[3]};UID=ONENT_PYTH;PWD=Pyth123"
        server = 'VOLVOFCI05.ng.entp.tgc,62595'
        database = 'ONENT'
        self.mssql_connector: MssqlDbConnector = MssqlDbConnector(server, database, user, password)
        self.database_manager: DatabaseManager = DatabaseManager(self.mssql_connector)
        data = self.database_manager.fetch(executable_script)
        return data

    def make_Connection_Write(self, pdi_data, executable_script, inserted_rows):
        user = 'ONENT_PYTH'
        password = 'Pyth123'
        if pdi_data[18] is not None:
            user = self.crypto_service.decrypt_code(pdi_data[18].encode())
        if pdi_data[19] is not None:
            password = self.crypto_service.decrypt_code(pdi_data[19].encode())
        self.mssql_connector: MssqlDbConnector = MssqlDbConnector(pdi_data[16], pdi_data[13], user, password)
        self.database_manager: DatabaseManager = DatabaseManager(self.mssql_connector)
        odi_drop_sql = f"DELETE FROM {pdi_data[20]}.{pdi_data[21]}"
        if pdi_data[22] == 1:
            self.database_manager.delete(odi_drop_sql)

        self.database_manager.insert_many(executable_script, inserted_rows)
