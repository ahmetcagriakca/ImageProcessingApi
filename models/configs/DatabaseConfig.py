class DatabaseConfig:
    def __init__(self,
                 driver: str = None,
                 host: str = None,
                 database: str = None,
                 username: str = None,
                 password: str = None,
                 ):
        self.driver = driver
        self.host = host
        self.database = database
        self.username = username
        self.password = password
