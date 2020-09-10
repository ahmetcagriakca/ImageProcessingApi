from datetime import time


class DatabaseManager:
    def __init__(self, connector, retry_count=3):
        self.connector = connector
        self.retry_count = retry_count
        self.default_retry = 1

    def _connect_to_db(self):
        self.connector.connect()

    def _disconnect_from_db(self):
        self.connector.disconnect()

    def fetch(self, query):
        self._connect_to_db()
        cur = self.connector.connection.cursor()
        cur.execute(query)

        datas = cur.fetchall()

        self._disconnect_from_db()

        data_list=[]
        for data in datas:
            rows=[]
            for row in data:
                rows.append(row)
            data_list.append(rows)
        return data_list;

    def delete(self, query) -> None:
        self._connect_to_db()
        cur = self.connector.connection.cursor()
        cur.execute(query)
        self.connector.connection.commit()
        self._disconnect_from_db()

    def insert_many(self, executable_script, inserted_rows):

        self._connect_to_db()
        cur = self.connector.connection.cursor()
        cur.prepare(executable_script)
        cur.executemany(None, inserted_rows)
        #            for rows in insertedRows:
        #                cur.execute(executableScript,rows)
        self.connector.connection.commit()
        self._disconnect_from_db()

    def insert_to_db_with_script(self, data, script):
        self._connect_to_db()
        self.connector.bulk_insert(data, script)
        self._disconnect_from_db()

    def insert_to_db(self, data):
        self._connect_to_db()
        result = self.connector.bulk_insert(data, self.sql_builder.build())
        self._disconnect_from_db()
        return result

    def insert_to_db_for_page(self, data, page, limit):
        self._connect_to_db()
        result = self._insert_to_db_with_retry(data, page, limit, self.default_retry)
        self._disconnect_from_db()
        return result

    def insert_to_db_with_paging(self, data, page, limit):

        print(f"Operation started. data_length :{len(data)} page :{page} limit :{limit}")
        data_length = len(data)
        total_fragment_count = int(data_length / limit)
        fragment_count = total_fragment_count - page
        result = False
        self._connect_to_db()
        try:
            executed_page = page
            for rec in range(fragment_count):
                processing_page = page + rec
                # preparing data
                start = processing_page * limit
                end = start + limit
                fragmented_data = data[start:end]
                result = self._insert_to_db_with_retry(fragmented_data, start, end, self.default_retry)
                if not result:
                    break
            # finish operation
            if result:
                remaining_data_count = data_length - (total_fragment_count * limit)
                # preparing data
                start = total_fragment_count * limit
                end = start + remaining_data_count
                fragmented_data = data[start:end]
                result = self._insert_to_db_with_retry(fragmented_data, start, end, self.default_retry)
        finally:
            self._disconnect_from_db()

    def _insert_to_db_with_retry(self, data, start, end, retry):
        try:
            self.connector.bulk_insert(data, self.sql_builder.build())
        except Exception as ex:
            if (retry > self.retry_count):
                print(f"Db write error on start:{start},end:{end} Error:{ex}")
                return False

            print(
                f"Getting error on insert (Operation will be retried. Retry Count:{retry}). start:{start},end:{end}, Error:{ex}")
            # retrying connect to db
            self.connector.connect()
            time.sleep(1)
            return self._insert_to_db_with_retry(data, start, end, retry + 1)

        print(f'Committed start:{start} end:{end}')
        return True

    def insert(self, executable_script):
        self._connect_to_db()
        self.connector.insert(executable_script)
        self._disconnect_from_db()
