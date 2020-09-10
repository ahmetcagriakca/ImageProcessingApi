from dependency_injector import providers, containers
from configurations import Configurations
from controllers.ImageProcessingController import ImageProcessingController
from domain.imageprocessing.services.ImageProcessingService import ImageProcessingService, Detection
from infrastructor.api.ErrorHandler import ErrorHandlers
from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from infrastructor.data.DatabaseManager import DatabaseManager
from infrastructor.data.MssqlConnector import MssqlDbConnector
from infrastructor.file.file_operations import FileOperations
from infrastructor.logging.ConsoleLogger import ConsoleLogger


class IocContainer(containers.DeclarativeContainer):
    configurations = Configurations()

    errorHandlers = providers.Singleton(ErrorHandlers)

    console_logger = providers.Factory(ConsoleLogger)

    mssql_connector = providers.Factory(MssqlDbConnector,
                                        host=configurations.database_config.host,
                                        database=configurations.database_config.database,
                                        username=configurations.database_config.username,
                                        password=configurations.database_config.password)

    mssql_database_manager = providers.Factory(DatabaseManager,
                                               connector=mssql_connector)

    file_operations = providers.Factory(FileOperations,
                                        api_config=configurations.api_config)
    image_processing_service = providers.Factory(ImageProcessingService,
                                                 file_operations=file_operations)

    image_processing_controller = providers.Factory(ImageProcessingController,
                                                    image_processing_service=image_processing_service,
                                                    file_operations=file_operations)

    applicationWrapper = providers.Factory(FlaskAppWrapper,
                                           api_config=configurations.api_config,
                                           handlers=errorHandlers,
                                           controllers=[image_processing_controller])

    Detection.start_detection()
