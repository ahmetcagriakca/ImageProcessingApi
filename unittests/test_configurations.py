import os
import yaml

from models.configs.ApiConfig import ApiConfig
from models.configs.DatabaseConfig import DatabaseConfig

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_application_conf.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class TestConfigurations:
    def __init__(self):
        ################################################################################################################
        # Api Information
        environment = os.getenv('API_ENVIRONMENT', cfg['API']['ENVIRONMENT'])
        api_name = os.getenv('API_NAME', cfg['API']['NAME'])
        is_debug = os.getenv('API_IS_DEBUG', cfg['API']['IS_DEBUG'])
        api_port = os.getenv('API_PORT', cfg['API']['PORT'])
        root_directory = os.path.dirname(os.path.abspath(__file__))
        self.api_config = ApiConfig(environment, api_name, is_debug, api_port, root_directory)
        ################################################################################################################
        # Database Information
        dbms_driver = os.getenv('DATABASE_DRIVER', cfg['DATABASE']['DRIVER'])
        dbms_host = os.getenv('DATABASE_HOST', cfg['DATABASE']['HOST'])
        dbms_database = os.getenv('DATABASE_DATABSAE', cfg['DATABASE']['DATABSAE'])
        dbms_username = os.getenv('DATABASE_USERNAME', cfg['DATABASE']['USERNAME'])
        dbms_password = os.getenv('DATABASE_PASSWORD', cfg['DATABASE']['PASSWORD'])
        self.database_config = DatabaseConfig(dbms_driver, dbms_host, dbms_database, dbms_username, dbms_password)
