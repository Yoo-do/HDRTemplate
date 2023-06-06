# 标准化 将原始excel文件转变为json文件
import xlwings
import json
import re


class Column:
    def __init__(self, column_name, sort_no, chinese_name, column_type, allow_null):
        self.column_name = column_name
        self.sort_no = sort_no
        self.chinese_name = chinese_name
        self.column_type = column_type
        self.allow_null = allow_null

    def __json__(self):
        return {'column_name': self.column_name,
                'sort_no': self.sort_no,
                'chinese_name': self.chinese_name,
                'column_type': self.column_type,
                'allow_null': self.allow_null}


class Table:
    def __init__(self, table_name, table_note):
        self.table_name = table_name
        self.table_note = table_note
        self.columns: list[Column] = []

    def add_column(self, column: Column):
        self.columns.append(column)

    def __json__(self):
        return {'table_name': self.table_name, 'table_note': self.table_note,
                'columns': [x.__json__() for x in self.columns]}


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

    def __json__(self):
        return {self.schema_name: {'tables': [x.__json__() for x in self.tables]}}


def read_sheet(schema_name, sheet: xlwings.main.Sheet) -> Schema:
    schema = Schema(schema_name)
    curr_row = 1

    while True:
        curr_data = sheet.range('A' + curr_row.__str__() + ':' + 'E' + curr_row.__str__()).value
        if len([x for x in curr_data if x is not None]) == 0:
            if schema.get_table_num() != 0:
                break
            else:
                curr_row += 1
                continue

        if curr_data[0] is not None and len([x for x in curr_data if x is not None]) == 1:
            schema.add_table(Table(re.findall(r'[^（）]+', curr_data[0])[0],
                                   '' if len(re.findall(r'[^（）]+', curr_data[0])) == 1 else
                                   re.findall(r'[^（）]+', curr_data[0])[1]))
        elif 0 < len([x for x in curr_data if x is not None]) < len(curr_data):
            pass
        elif curr_data[0] == '序号':
            pass
        else:
            schema.tables[-1].add_column(Column(column_name=curr_data[1],
                                                sort_no=curr_data[0],
                                                chinese_name=curr_data[2],
                                                column_type=curr_data[3],
                                                allow_null=curr_data[4]))

        curr_row += 1

    return schema


def read_sd_file() -> list[Schema]:
    app = xlwings.App(visible=False)
    sd_book = app.books.open('../resoures/sd.xlsx')
    sd_sheet = sd_book.sheets['sd']

    sd_schema = read_sheet('sd', sd_sheet)

    sd_book.close()
    app.quit()

    return [sd_schema]


def read_hdr_file() -> list[Schema]:

    app = xlwings.App(visible=False)
    hdr_book = app.books.open('../resoures/hdr.xlsx')

    hdr_sheets: list[xlwings.Sheet] = hdr_book.sheets
    hdr_schemas = []

    for sheet in [x for x in hdr_sheets if re.match(r'^[a-z]+$', x.name)]:
        hdr_schemas.append(read_sheet(sheet.name, sheet))




    hdr_book.close()
    app.quit()

    return hdr_schemas

def schema_export_json(schemas: list[Schema]):
    data = {}
    for schema in schemas:
        data.update(schema.__json__())

    with open('../data/hdr.json', 'w') as f:
        json.dump(data, f)


def load_all_schema():
    schemas = []
    schemas += read_sd_file()
    schemas += read_hdr_file()
    schema_export_json(schemas)

if __name__ == '__main__':
    load_all_schema()

