from PyQt5 import QtWidgets, uic , QtCore
import requests
from Create_NewUser import NewUserDialog  # Import the new dialog
import json

class UsersTableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("WMS_System/UI/Users.ui", self)

        # Reference UI Elements
        self.tableWidget_Users = self.findChild(QtWidgets.QTableWidget, 'tableWidget_Users')
        self.toolButton_Save = self.findChild(QtWidgets.QToolButton, 'toolButton_Save')
        self.toolButton_Reset = self.findChild(QtWidgets.QToolButton, 'toolButton_Reset')
        self.toolButton_New = self.findChild(QtWidgets.QToolButton, 'toolButton_New')

        # Enable editing for the QTableWidget
        self.tableWidget_Users.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # Load Users on Start
        self.load_users()

        # Connect Buttons to Functions
        self.toolButton_Save.clicked.connect(self.save_changes)
        self.toolButton_Reset.clicked.connect(self.reset_changes)
        self.toolButton_New.clicked.connect(self.open_new_user_dialog)

        # Track changes
        self.changes = {}

        # Connect cell change tracking
        self.tableWidget_Users.itemChanged.connect(self.track_changes)

    def open_new_user_dialog(self):
        """Open the New User Dialog when the 'New' button is clicked."""
        dialog = NewUserDialog()
        if dialog.exec_():
            self.load_users()  # Refresh data if a new user was created

    def load_users(self):
        """Load all users when the window opens."""
        try:
            response = requests.get("http://localhost:8000/Users/")

            if response.status_code == 200:
                self.populate_table(response.json())
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load users")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

    def populate_table(self, users):
        """Populate the table with user data without displaying user_id."""
        self.tableWidget_Users.setRowCount(len(users))
        self.tableWidget_Users.setColumnCount(3)  # Only display Username and Role, Password
        self.tableWidget_Users.setHorizontalHeaderLabels(["Username", "Role","Password"])

        for row, user in enumerate(users):
            # Store user_id as "hidden" data using Qt.UserRole
            user_id_item = QtWidgets.QTableWidgetItem(str(user["username"]))
            user_id_item.setData(QtCore.Qt.UserRole, user["user_id"])  # Hidden ID tracking
            self.tableWidget_Users.setItem(row, 0, QtWidgets.QTableWidgetItem(user["username"].upper()))
            self.tableWidget_Users.setItem(row, 1, QtWidgets.QTableWidgetItem(user["role"]))
            self.tableWidget_Users.setItem(row, 2, QtWidgets.QTableWidgetItem(""))  
            
            # Add the user_id data to track changes efficiently
            self.tableWidget_Users.setItem(row, 0, user_id_item)

   
    def track_changes(self, item):
        """Track changes when cells are modified."""
        row = item.row()
        column = item.column()

        # Track the item ID
        item_id = self.tableWidget_Items.item(row, 0).text()

        # Ensure valid item_id
        if not item_id:
            return

        # Fetch the original value from the stored data
        original_value = self.original_data.get(item_id, {}).get(
            "item_code" if column == 1 else "price", ""
        )

        # Capture the new value
        new_value = item.text().strip()

        print(f"Original Value: {original_value}")
        print(f"New Value: {new_value}")

        # Track the modified data only if different from original
        if item_id not in self.changes:
            self.changes[item_id] = {}

        if column == 1 and new_value != original_value:  # Item Code Column
            self.changes[item_id]["item_code"] = new_value

        elif column == 2 and new_value != original_value:  # Price Column
            self.changes[item_id]["price"] = new_value

        # Clean up if no changes remain for this item
        if not self.changes[item_id]:
            del self.changes[item_id]

        print(f"🟡 Changes Tracked: {self.changes}")


    def save_changes(self):
        if not self.changes:
            QtWidgets.QMessageBox.information(self, "No Changes", "No changes to save.")
            return

        try:
            for user_id, updated_data in self.changes.items():
                print(f"🔍 Data Before Sending: {updated_data}")

                if user_id == "NEW":
                    QtWidgets.QMessageBox.warning(self, "Error", "Cannot create new users in this view.")
                    continue

                user_data = {
                    "username": updated_data.get("username", "").upper(),
                    "role": updated_data.get("role", "")
                }

                # Add password if provided
                if "password" in updated_data and updated_data["password"].strip():
                    user_data["password"] = updated_data["password"]

                print(f"✅ Final Data Sent to API: {user_data}")

                response = requests.put(
                    f"http://localhost:8000/Users/{user_id}",
                    json=user_data,  
                    headers={"Content-Type": "application/json"} 
                )

                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", f"User {user_id} updated successfully!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update user {user_id}")

            self.changes.clear()

        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")



    def reset_changes(self):
        """Reload the data from the database to discard unsaved changes."""
        confirm = QtWidgets.QMessageBox.question(
            self, "Reset", "Are you sure you want to reset all unsaved changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            self.load_users()  # Reload data to reset changes
            self.changes.clear()
            QtWidgets.QMessageBox.information(self, "Reset", "All unsaved changes have been discarded.")