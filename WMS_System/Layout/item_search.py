from PyQt5 import QtWidgets, uic, QtCore 
from add_item_dialog import AddItemDialog
import requests

class ItemSearchWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/item_search1.ui", self)

        # Ensure there's a layout (add one if missing)
        if not self.layout():
            layout = QtWidgets.QGridLayout(self)
            self.setLayout(layout)

        # Reference UI Elements
        self.tableWidget_Items = self.findChild(QtWidgets.QTableWidget, 'tableWidget_Items')
        self.lineEdit_Search = self.findChild(QtWidgets.QLineEdit, 'lineEdit_Search')
        self.btn_Search = self.findChild(QtWidgets.QPushButton, 'btn_Search')
        self.actionNew = self.findChild(QtWidgets.QAction, 'actionNew') 

        self.lineEdit_Search.returnPressed.connect(self.search_items)
        self.btn_Search.clicked.connect(self.search_items)
        self.installEventFilter(self)


        # Add Search Bar and Button (Row 1)
        self.layout().addWidget(self.lineEdit_Search, 1, 0, 1, 2)
        self.layout().addWidget(self.btn_Search, 1, 2)

        # Add Table at the Bottom (Row 2)
        self.layout().addWidget(self.tableWidget_Items, 2, 0, 1, 3)

        # Track cell changes
        self.changes = {}
        self.original_data = {}
        self.tableWidget_Items.itemChanged.connect(self.track_changes)

        self.clear_table()


    def open_add_item_dialog(self):
        """Open the Add Item Dialog when the 'Add New' button is clicked."""
        dialog = AddItemDialog()
        if dialog.exec_():  # If accepted
            item_data = dialog.get_item_data()
            self.createItem(item_data)  # ✅ Separate method to handle data insertion


    def createItem(self, item_data):
        """Send the new item to FastAPI and refresh the table."""
        try:
            response = requests.post("http://localhost:8000/items/", json=item_data)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "New item added successfully!")
                self.search_items()  # Refresh the table
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to add item.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")
            

    def track_changes(self, item):
        """Track changes when cells are modified."""
        row = item.row()
        column = item.column()

        # Retrieve the item ID from the hidden data
        item_id = self.tableWidget_Items.item(row, 0).data(QtCore.Qt.UserRole)
        if not item_id:
            return

        # Ensure the item ID is properly initialized
        if str(item_id) not in self.original_data:
            return  # Ignore entries that were not originally loaded

        # Initialize the original value properly
        original_value = None
        if column == 0:  # Item ID Column
            original_value = self.original_data[str(item_id)]["item_id"]
        elif column == 1:
            original_value = self.original_data[str(item_id)]["description"]
        elif column == 2:  # Price Column
            original_value = str(self.original_data[str(item_id)]["price"])
        elif column == 3:  # Active Column
            original_value = "Yes" if self.original_data[str(item_id)]["is_offer"] else "No"

        # Capture the new value
        new_value = item.text().strip()

        # Track the modified data only if different from original
        if str(item_id) not in self.changes:
            self.changes[str(item_id)] = {}

        # Correctly track individual fields
        if column == 0 and new_value != original_value:
            self.changes[str(item_id)]["item_id"] = new_value
        elif column == 1 and new_value != original_value:
            self.changes[str(item_id)]["description"] = new_value
        elif column == 2 and new_value != original_value:
            self.changes[str(item_id)]["price"] = new_value
        elif column == 3 and new_value != original_value:
            self.changes[str(item_id)]["is_offer"] = True if new_value == "Yes" else False

        # ✅ Ensure empty entries are properly removed
        if not self.changes[str(item_id)]:
            del self.changes[str(item_id)]

        print("print changes:", self.changes)



    # ---------------------------- SEARCH FUNCTION ---------------------------- #
    def search_items(self):
        search_term = self.lineEdit_Search.text().strip()
        self.changes.clear()

        try:
            response = requests.get("http://localhost:8000/items/")
            if response.status_code == 200:
                items = response.json()

                if not search_term:
                    self.populate_table(items)
                else:
                    filtered_items = [
                        item for item in items if search_term.lower() in item['item_id'].lower()
                    ]
                    self.populate_table(filtered_items)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load items")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

    # ---------------------------- TABLE POPULATION FUNCTION ---------------------------- #
    def populate_table(self, items):
        """Populate the table with item data and store original values."""
        self.original_data = {}
        self.tableWidget_Items.setRowCount(len(items))
        self.tableWidget_Items.setColumnCount(4)
        self.tableWidget_Items.setHorizontalHeaderLabels(["Item ID","Description", "Price", "Active"])

        for row, item in enumerate(items):
            item_id_item = QtWidgets.QTableWidgetItem(str(item["item_id"]))
            item_id_item.setData(QtCore.Qt.UserRole, item["id"])

            self.tableWidget_Items.setItem(row, 0, item_id_item)
            self.tableWidget_Items.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item["description"])))
            self.tableWidget_Items.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item["price"])))

            active_value = "Yes" if item.get("is_offer") else "No"
            self.tableWidget_Items.setItem(row, 3, QtWidgets.QTableWidgetItem(active_value))

            self.original_data[str(item["id"])] = {
                "item_id": item["item_id"],
                "description": item["description"],
                "price": str(item["price"]),
                "is_offer": item.get("is_offer", False)
            }



    def save_changes(self):
        """Send only the tracked changes to the API."""
        if not self.changes:
            QtWidgets.QMessageBox.information(self, "No Changes", "No changes to save.")
            return

        try:
            for item_id, updated_data in self.changes.items():
                response = requests.put(
                    f"http://localhost:8000/items/{item_id}",
                    json=updated_data,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", f"Item {item_id} updated successfully!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update item {item_id}")

            # Clear changes only after a successful save
            self.changes.clear()

        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")


    # ---------------------------- CLEAR TABLE FUNCTION ---------------------------- #
    def clear_table(self):
        self.tableWidget_Items.setRowCount(0)
        self.tableWidget_Items.setColumnCount(4)
        self.tableWidget_Items.setHorizontalHeaderLabels(["Item ID","Description", "Price","Active"])

    # ---------------------------- RESET CHANGES FUNCTION ---------------------------- #
    def discard_changes(self):
        """Check if there are changes before asking for confirmation."""
        if not self.changes:
            self.search_items()
            QtWidgets.QMessageBox.information(self, "Info", "No unsaved changes to discard.")
            return  # Exit early since no changes exist

        # Ask for confirmation only if there are changes
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Reset",
            "Are you sure you want to reset all unsaved changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            self.changes.clear()
            self.clear_table()
            self.search_items()
            QtWidgets.QMessageBox.information(self, "Reset", "All unsaved changes have been discarded.")

