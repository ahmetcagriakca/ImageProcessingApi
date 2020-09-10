import logging as log
from datetime import datetime


class ConsoleLogger:
    def __init__(self):
        self.log_level = log.DEBUG
        self.log_init()
        self.log = log

    def log_init(self):
        """
        initialization of log file.
        """
        # log.basicConfig(filename=os.path.join(self.other_config.root_directory, self.log_file),
        #                 filemode='a',
        #                 format='%(asctime)s [%(levelname)s] - %(message)s',
        #                 datefmt='%Y-%m-%d %H:%M:%S',
        #                 level=self.log_level)
        log.basicConfig(level=self.log_level)

    def prepare_message(self, message):
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return f'{log_datetime} - {message}'

    def info(self, message):
        prepared_message = self.prepare_message(message);
        self.log.info(prepared_message)

    def error(self, message):
        prepared_message = self.prepare_message(message);
        self.log.error(prepared_message)

    def warning(self, message):
        prepared_message = self.prepare_message(message);
        self.log.warning(prepared_message)
