from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets


class GroupMaintanceUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Group Maintance")

        # Layout principal
        layout = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Crear tabs individuales
        self.putaway_tab = self.create_group_tab()
        self.restock_tab = self.create_group_tab()
        self.pick_tab = self.create_group_tab()

        self.tabs.addTab(self.putaway_tab, "Putaway")
        self.tabs.addTab(self.restock_tab, "Restock")
        self.tabs.addTab(self.pick_tab, "Pick")

    def create_group_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels(["GROUP NAME", "DESCRIPTION"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        tab.table = table  # puedes acceder a este atributo si lo necesitas luego
        layout.addWidget(table)

        return tab
