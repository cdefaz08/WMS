from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget


class Ui_RuleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rule Manager")
        self.resize(800, 400)

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)

        # Crear las tablas para cada pestaña
        self.putaway_table = self.create_table()
        self.restock_table = self.create_table()
        self.pick_table = self.create_table()

        # Añadir pestañas
        self.tab_widget.addTab(self.putaway_table, "Putaway")
        self.tab_widget.addTab(self.restock_table, "Restock")
        self.tab_widget.addTab(self.pick_table, "Pick")

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Rule Name", "Description"])
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 410)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        return table
