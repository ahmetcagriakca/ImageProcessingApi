from infrastructor.data.ConnectionStrategy import ConnectionStrategy


class DbContext:
    def __init__(self, strategy: ConnectionStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ConnectionStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ConnectionStrategy) -> None:
        self._strategy = strategy

    def db_connection(self, pdi_data, executable_script) -> None:
        result = self._strategy.make_connection(pdi_data, executable_script)
        return result

    def db_connection_write(self, pdi_data, executable_script, inserted_rows) -> None:
        result = self._strategy.make_Connection_Write(pdi_data, executable_script, inserted_rows)
        return result
