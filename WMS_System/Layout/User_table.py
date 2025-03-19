from PyQt5 import QtWidgets, uic
import requests

class UsersTableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("WMS_System/UI/Users.ui", self)  # Verify this path

        # Reference UI Elements
        self.tableWidget_Users = self.findChild(QtWidgets.QTableWidget, 'tableWidget_Users')

        # Debugging Check
        print("tableWidget_Users:", self.tableWidget_Users)  # Should NOT print 'None'

        # Enable editing for the QTableWidget
        if self.tableWidget_Users:
            self.tableWidget_Users.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
            self.load_users()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Users table not found in UI file!")

        # Reference Save Button
        self.toolButton_Save = self.findChild(QtWidgets.QToolButton, 'toolButton_Save')
        self.toolButton_Save.clicked.connect(self.save_changes)

        self.changes = {}  # Track changes
        self.tableWidget_Users.itemChanged.connect(self.track_changes)

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
        """Populate the table with user data."""
        self.tableWidget_Users.setRowCount(len(users))
        self.tableWidget_Users.setColumnCount(3)  # Assuming columns: ID, Username, Role
        self.tableWidget_Users.setHorizontalHeaderLabels(["ID", "Username", "Role"])

        for row, user in enumerate(users):
            self.tableWidget_Users.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user["id"])))
            self.tableWidget_Users.setItem(row, 1, QtWidgets.QTableWidgetItem(user["username"]))
            self.tableWidget_Users.setItem(row, 2, QtWidgets.QTableWidgetItem(user["role"]))

    def track_changes(self, item):
        """Track cell changes and apply uppercase for usernames."""
        row = item.row()
        column = item.column()

        # Force uppercase only on the Username column
        if column == 1:
            item.setText(item.text().upper())

        column_name = ["id", "username", "role"][column]  # Column mapping
        user_id = self.tableWidget_Users.item(row, 0).text()

        # Store changes in a dictionary
        if user_id not in self.changes:
            self.changes[user_id] = {}

        self.changes[user_id][column_name] = item.text()

    def save_changes(self):
        """Send the updated data to FastAPI for saving in the database."""
        if not self.changes:
            QtWidgets.QMessageBox.information(self, "No Changes", "No changes to save.")
            return

        try:
            for user_id, updated_data in self.changes.items():
                response = requests.put(f"http://localhost:8000/Users/{user_id}", json=updated_data)

                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", f"User {user_id} updated successfully!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update user {user_id}")

            # Clear changes after successful save
            self.changes.clear()

        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")
