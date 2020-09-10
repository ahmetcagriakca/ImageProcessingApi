from infrastructor.Cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionStrategy import ConnectionStrategy
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.data.OracleConnector import OracleDbConnector


class OracleConnectionStrategy(ConnectionStrategy):
    def __init__(self, crypto_service: CryptoService):
        self.oracle_connector: OracleDbConnector = None
        self.database_manager: DatabaseManager = None
        self.crypto_service: CryptoService = crypto_service

    def make_connection(self, pdi_data, executable_script):
        if pdi_data[8] is not None:
            user = self.crypto_service.decrypt_code(pdi_data[8].encode())

        if pdi_data[9] is not None:
            password = self.crypto_service.decrypt_code(pdi_data[9].encode())
        print( f'user:{user}-pass:{user}-host:{pdi_data[14]}-host:{pdi_data[15]}-host:{pdi_data[17]}-host:{pdi_data[7]}')
        if pdi_data[7] is not None:
            self.oracle_connector = OracleDbConnector(None, pdi_data[14], pdi_data[15], pdi_data[17], user, password)
        else:
            connection_string = f"{user.decode('utf-8')}/{password.decode('utf-8')}@{pdi_data[4]}:{pdi_data[5]}/{pdi_data[3]}"
            self.oracle_connector = OracleDbConnector(connection_string)

        self.database_manager = DatabaseManager(self.oracle_connector, None)
        data = self.database_manager.fetch(executable_script)
        return data

    def make_Connection_Write(self, pdi_data, executable_script, inserted_rows):
        if pdi_data[18] is not None:
            user = self.crypto_service.decrypt_code(pdi_data[18].encode())

        if pdi_data[19] is not None:
            password = self.crypto_service.decrypt_code(pdi_data[19].encode())

        if pdi_data[17] is not None:
            self.oracle_connector = OracleDbConnector(None, pdi_data[14], pdi_data[15], pdi_data[17], user, password)
        else:
            connection_string = f"{user.decode('utf-8')}/{password.decode('utf-8')}@{pdi_data[14]}:{pdi_data[15]}/{pdi_data[13]}"
            self.oracle_connector = OracleDbConnector(connection_string)

        self.database_manager = DatabaseManager(self.oracle_connector)

        odi_drop_sql = f"DELETE FROM {pdi_data[20]}.{pdi_data[21]}"
        if pdi_data[22] == 1:
            self.database_manager.delete(odi_drop_sql)

        self.database_manager.insert_many(executable_script, inserted_rows)

        return True
