class ApiConfig:
    def __init__(self,
                 environment: str = None,
                 name: str = None,
                 is_debug: bool = None,
                 port: int = None,
                 root_directory: str = None):
        self.port = port
        self.is_debug = is_debug
        self.name = name
        self.environment = environment
        self.root_directory = root_directory
