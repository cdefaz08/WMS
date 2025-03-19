from PyQt5 import QtWidgets, uic
import requests

class ItemSearchWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/item_search.ui", self)

        # Reference UI Elements
        self.tableWidget_Items = self.findChild(QtWidgets.QTableWidget, 'tableWidget_Items')
        self.lineEdit_Search = self.findChild(QtWidgets.QLineEdit, 'lineEdit_Search')
        self.btn_Search = self.findChild(QtWidgets.QPushButton, 'btn_Search')

        # Connect Search Button to Search Function
        self.btn_Search.clicked.connect(self.search_items)

        # Initialize the Table as Blank
        self.clear_table()

    def clear_table(self):
        """Initialize the table with no data (blank)."""
        self.tableWidget_Items.setRowCount(0)
        self.tableWidget_Items.setColumnCount(3)  # ID, Name, Price
        self.tableWidget_Items.setHorizontalHeaderLabels(["ID", "Name", "Price"])

    def search_items(self):
        """Search for items or fetch all data if the search bar is empty."""
        search_term = self.lineEdit_Search.text().strip()

        try:
            response = requests.get("http://localhost:8000/items/")
            if response.status_code == 200:
                items = response.json()

                # Show all items if the search term is empty
                if not search_term:
                    self.populate_table(items)
                else:
                    filtered_items = [
                        item for item in items if search_term.lower() in item['name'].lower()
                    ]
                    self.populate_table(filtered_items)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load items")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

    def populate_table(self, items):
        """Populate the table with item data."""
        self.tableWidget_Items.setRowCount(len(items))
        self.tableWidget_Items.setColumnCount(3)  # Assuming item fields: ID, Name, Price
        self.tableWidget_Items.setHorizontalHeaderLabels(["ID", "Name", "Price"])

        for row, item in enumerate(items):
            self.tableWidget_Items.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item["id"])))
            self.tableWidget_Items.setItem(row, 1, QtWidgets.QTableWidgetItem(item["name"]))
            self.tableWidget_Items.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item["price"])))
