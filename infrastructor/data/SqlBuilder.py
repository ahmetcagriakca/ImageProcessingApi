class SqlBuilder:
    def __init__(self):
        pass
        
    def build(self):
        pass

    
class DefaultInsertSqlBuilder(SqlBuilder):
    def __init__(self, table_name, length):
        self.table_name = table_name
        self.length = length

    def build(self):
        value_sql = ''
        for rec in range(self.length):

            value_sql += f':{rec + 1}'
            if rec != self.length - 1:
                value_sql += ','

        return f"INSERT INTO {self.table_name} values ({value_sql})"
