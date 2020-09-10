from datetime import datetime
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.logging.ConsoleLogger import ConsoleLogger


class SqlLogger:
    def __init__(self, environment, mssql_database_manager: DatabaseManager, console_logger: ConsoleLogger):
        self.console_logger = console_logger
        self.mssql_database_manager = mssql_database_manager
        self.environment = environment

    #######################################################################################
    def logger_method(self, type_of_log, log_string):
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        comment = f'Python Data Integrator {self.environment}'
        executable_script = f"INSERT INTO NEMS_COMMON.LOG(TYPE_ID,CONTENT,DATETIME,COMMENTS,TENANT_ID) VALUES ({type_of_log},'{log_string}', convert(datetime,'{log_datetime}'),'{comment}',1)"
        self.console_logger.info(log_string)
        self.mssql_database_manager.insert(executable_script)

    #######################################################################################
    def error_Log(self, errorString):
        self.logger_method(4, errorString)

    #######################################################################################
    def info_Log(self, infoString):
        self.logger_method(2, infoString)
