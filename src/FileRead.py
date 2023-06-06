import json


class Column:
    def __init__(self, column_name, sort_no, chinese_name, column_type, allow_null):
        self.column_name = column_name
        self.sort_no = sort_no
        self.chinese_name = chinese_name
        self.column_type = column_type
        self.allow_null = allow_null


class Table:
    def __init__(self, table_name, table_note):
        self.table_name = table_name
        self.table_note = table_note
        self.columns: list[Column] = []

    def add_column(self, column: Column):
        self.columns.append(column)

    def column_sort(self):
        self.columns.sort(key=lambda x: x.sort_no, reverse=False)


class Schema:
    def __init__(self, schema_name):
        self.schema_name = schema_name
        self.tables: list[Table] = []

    def add_table(self, table: Table):
        self.tables.append(table)

    def get_table_num(self):
        return len(self.tables)

    def set_tables(self, tables: list[Table]):
        self.tables = tables

    def table_column_sort(self):
        for table in self.tables:
            table.column_sort()


class HDRData:
    def __init__(self):
        self.schemas: list[Schema] = []

        self.init_schema()

    def init_schema(self):
        self.schemas = read_schema_file()

    def get_schemas(self):
        return self.schemas

    def get_tables(self, schema_name):
        return [x for x in self.schemas if x.schema_name == schema_name][0].tables

    def get_columns(self, schema_name, table_name):
        return [x for x in self.get_tables(schema_name) if x.table_name == table_name][0].columns

    def get_schema_names(self):
        return [x.schema_name for x in self.schemas]

    def get_table_names(self, schema_name):
        return [x.table_name for x in self.get_tables(schema_name)]

    def get_table_notes(self, schema_name):
        return [x.table_note for x in self.get_tables(schema_name)]

    def get_column_names(self, schema_name, table_name):
        return [x.column_name for x in self.get_columns(schema_name, table_name)]

    def get_table_column_infos(self, schema_name, table_name):
        columns = self.get_columns(schema_name, table_name)

        tittle_info = ['字段', '字段名', '类型', '允许空']
        result_info = []

        for column in columns:
            result_info.append(
                [column.column_name, column.chinese_name, column.column_type, column.allow_null])

        return tittle_info, result_info


def read_schema_file() -> list[Schema]:
    schemas = []

    with open('../data/hdr.json', 'r') as f:
        schemas_dict: dict = json.load(f)

    for schema_name, schema_val in schemas_dict.items():
        schema_obj = Schema(schema_name)
        for table in schema_val['tables']:
            table_obj = Table(table['table_name'], table['table_note'])
            for column in table['columns']:
                column_obj = Column(column_name=column['column_name'],
                                    sort_no=column['sort_no'],
                                    chinese_name=column['chinese_name'],
                                    column_type=column['column_type'],
                                    allow_null=column['allow_null'])
                table_obj.add_column(column_obj)
            table_obj.column_sort()
            schema_obj.add_table(table_obj)
        schemas.append(schema_obj)



    return schemas


if __name__ == '__main__':
    schemas = read_schema_file()
