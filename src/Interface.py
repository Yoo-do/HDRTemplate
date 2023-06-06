import sys

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QMessageBox

import FileRead
import pyperclip


class Interface(QWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.data_init()
        self.window_init()

        self.app.exec_()

    def window_init(self):
        self.show()
        self.resize(1200, 800)
        self.move(300, 100)
        # self.showMaximized()
        self.setWindowTitle('HDRTemplate')

        window_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(window_layout)

        # schema选项框
        self.schema_list_widget = QListWidget(self)
        window_layout.addWidget(self.schema_list_widget)
        self.schema_list_widget.addItems(self.data.get_schema_names())
        self.schema_list_widget.itemClicked.connect(self.schema_selected)
        window_layout.setStretchFactor(self.schema_list_widget, 1)

        # table选项框
        self.table_list_widget = QListWidget(self)
        window_layout.addWidget(self.table_list_widget)
        self.table_list_widget.itemClicked.connect(self.tabel_selected)
        window_layout.setStretchFactor(self.table_list_widget, 4)

        # column展示和按钮组
        column_operation_layout = QBoxLayout(QBoxLayout.TopToBottom)
        window_layout.addLayout(column_operation_layout)
        window_layout.setStretchFactor(column_operation_layout, 5)

        # column展示框
        self.column_table = QTableWidget(self)
        self.column_table.show()
        column_operation_layout.addWidget(self.column_table)

        # 按钮组
        self.operation_bar = QToolBar(self)
        self.show()
        column_operation_layout.addWidget(self.operation_bar)

        button_export_sql = QPushButton('导出sql语句')
        button_export_sql.clicked.connect(self.export_sql_action)
        self.operation_bar.addWidget(button_export_sql)


    def export_sql_action(self):
        if self.table_list_widget.currentItem() == None:
            QMessageBox.critical(self, '消息提示', '未选择表格', QMessageBox.Ok)
        else:
            QMessageBox.information(self, '消息提示', '已复制内容到粘贴板', QMessageBox.Ok)
            copy_text = ''

            copy_text += 'select' + '\n'
            for row in range(0, self.column_table.rowCount()):
                for col in range(0, self.column_table.columnCount()):
                    item = self.column_table.item(row, col)
                    copy_text += item.text() + ',' if row < self.column_table.rowCount() - 1 else '' +' -- ' if col == 0 else item.text() + '  '


                copy_text += '\n'

            copy_text += 'from' + '\n'
            copy_text += self.schema_list_widget.currentItem().text() + '.' + self.table_list_widget.currentItem().text()

            pyperclip.copy(copy_text)



    def data_init(self):
        self.data = FileRead.HDRData()

    def schema_selected(self):
        curr_schema_name = self.schema_list_widget.currentItem().text()
        self.table_list_widget.clear()

        self.table_list_widget.addItems(self.data.get_table_names(curr_schema_name))

        for index, note in enumerate(self.data.get_table_notes(curr_schema_name)):
            self.table_list_widget.item(index).setToolTip(note)

    def tabel_selected(self):
        curr_schema_name = self.schema_list_widget.currentItem().text()
        curr_table_name = self.table_list_widget.currentItem().text()

        tittle_info, column_info = self.data.get_table_column_infos(curr_schema_name, curr_table_name)

        self.column_table.clear()
        self.column_table.setColumnCount(len(tittle_info))
        self.column_table.setRowCount(len(column_info))

        self.column_table.setHorizontalHeaderLabels(tittle_info)
        for row, column_list in enumerate(column_info):
            for col, column in enumerate(column_list):
                new_item = QTableWidgetItem(column)
                self.column_table.setItem(row, col, new_item)


if __name__ == '__main__':
    interface = Interface()
