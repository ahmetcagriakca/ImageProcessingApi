from dependency_injector import providers, containers
from infrastructor.Cryptography.CryptoService import CryptoService
from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from infrastructor.api.ErrorHandler import ErrorHandlers
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.data.MssqlConnector import MssqlDbConnector
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from infrastructor.logging.SqlLogger import SqlLogger
from unittests.test_configurations import TestConfigurations
from domain.imageprocessing.services.ImageProcessingService import ImageProcessingService
from controllers.ImageProcessingController import ImageProcessingController


class TestIocContainer(containers.DeclarativeContainer):
    configurations = TestConfigurations()

    errorHandlers = providers.Singleton(ErrorHandlers)

    console_logger = providers.Factory(ConsoleLogger)

    mssql_connector = providers.Factory(MssqlDbConnector,
                                        host=configurations.database_config.host,
                                        database=configurations.database_config.database,
                                        username=configurations.database_config.username,
                                        password=configurations.database_config.password)

    mssql_database_manager = providers.Factory(DatabaseManager,
                                               connector=mssql_connector)

    image_processing_service = providers.Factory(ImageProcessingService,
                                                 api_config=configurations.api_config)

    image_processing_controller = providers.Factory(ImageProcessingController,
                                                    image_processing_service=image_processing_service)

    applicationWrapper = providers.Factory(FlaskAppWrapper,
                                           api_config=configurations.api_config,
                                           handlers=errorHandlers,
                                           controllers=[image_processing_controller])