from abc import abstractmethod, ABC


class ConnectionStrategy(ABC):
    @abstractmethod
    def make_connection(self, pdi_data, executable_script):
        pass

    @abstractmethod
    def make_Connection_Write(self, pdi_data, executable_script, inserted_rows):
        pass