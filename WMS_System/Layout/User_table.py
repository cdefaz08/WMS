from PyQt5 import QtWidgets, uic
import requests

class UsersTableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("WMS_System/UI/Users.ui", self)

        # Reference UI Elements
        self.tableWidget_Users = self.findChild(QtWidgets.QTableWidget, 'table_Users')

        # Load Users on Start
        self.load_users()

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
