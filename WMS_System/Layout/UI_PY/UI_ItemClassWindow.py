from PyQt5.QtWidgets import QWidget, QVBoxLayout , QTableWidget
from PyQt5.QtCore import Qt

class UI_ItemClassWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Item Classes")

        # Layouts
        layout = QVBoxLayout()

        # Tabla
        self.tableWidget_ItemClass = QTableWidget(0, 3)
        self.tableWidget_ItemClass.setHorizontalHeaderLabels(["ID", "Item Class ID", "Description"])
        self.tableWidget_ItemClass.setColumnHidden(0, True)  # Oculta ID

        layout.addWidget(self.tableWidget_ItemClass)
        self.setLayout(layout)
