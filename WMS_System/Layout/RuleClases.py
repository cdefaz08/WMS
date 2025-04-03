from PyQt5 import QtWidgets, uic
from database import SessionLocal
from crud import class_crud


class RuleClases(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/RuleClases.ui", self)

        self.load_data()

    def load_data(self):
        db = SessionLocal()

        # Get data
        putaway_data = class_crud.get_putaway_classes(db)
        restock_data = class_crud.get_restock_classes(db)
        pick_data = class_crud.get_pick_classes(db)

        db.close()

        # Fill the tables
        self.fill_table(self.tableWidget_PutawayClass, putaway_data)
        self.fill_table(self.tableWidget_RestockClass, restock_data)
        self.fill_table(self.tableWidget_PickClass, pick_data)

    def fill_table(self, table_widget, data):
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["ID", "Class Name", "Description"])

        for row_index, item in enumerate(data):
            table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.id)))
            table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.class_name))
            table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(item.description))
