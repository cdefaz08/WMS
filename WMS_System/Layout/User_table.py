from PyQt5 import QtWidgets, uic , QtCore
import requests
from Create_NewUser import NewUserDialog  # Import the new dialog
import json

class UsersTableWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Users.ui", self)

        # Reference UI Elements
        self.tableWidget_Users = self.findChild(QtWidgets.QTableWidget, 'tableWidget_Users')

        # Enable editing for the QTableWidget
        self.tableWidget_Users.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # Load Users on Start
        self.load_users()


        # Track changes
        self.changes = {}

        # Connect cell change tracking
        self.tableWidget_Users.itemChanged.connect(self.track_changes)

    def add_new_user(self):
        """Open the New User Dialog when the 'New' button is clicked."""
        dialog = NewUserDialog()
        if dialog.exec_():
            self.load_users()  # Refresh data if a new user was created



    def populate_table(self, users):
        """Populate the table with user data without displaying user_id."""
        self.tableWidget_Users.blockSignals(True)  # 🚨 Block signals before loading data

        self.tableWidget_Users.setRowCount(len(users))
        self.tableWidget_Users.setColumnCount(7)
        self.tableWidget_Users.setHorizontalHeaderLabels([
            "Username", "Role", "Password", "Full Name", "Email", "Max Logins", "Pallet Cap"
        ])


        self.original_data = {}  # Snapshot for tracking original data

        for row, user in enumerate(users):
            user_id_item = QtWidgets.QTableWidgetItem(str(user["username"]))
            user_id_item.setData(QtCore.Qt.UserRole, user["id"])  # Cambia a "id" si ese es el nombre real

            self.tableWidget_Users.setItem(row, 0, user_id_item)
            self.tableWidget_Users.setItem(row, 1, QtWidgets.QTableWidgetItem(user["role"]))
            self.tableWidget_Users.setItem(row, 2, QtWidgets.QTableWidgetItem(""))  # Empty password
            self.tableWidget_Users.setItem(row, 3, QtWidgets.QTableWidgetItem(user.get("full_name", "")))
            self.tableWidget_Users.setItem(row, 4, QtWidgets.QTableWidgetItem(user.get("email_addr", "")))
            self.tableWidget_Users.setItem(row, 5, QtWidgets.QTableWidgetItem(str(user.get("max_logins", ""))))
            self.tableWidget_Users.setItem(row, 6, QtWidgets.QTableWidgetItem(str(user.get("pall_cap", ""))))

            self.original_data[user["id"]] = {
                "username": user["username"].upper(),
                "role": user["role"],
                "password": "",
                "full_name": user.get("full_name", ""),
                "email_addr": user.get("email_addr", ""),
                "max_logins": str(user.get("max_logins", "")),
                "pall_cap": str(user.get("pall_cap", ""))
    }


        print(f"🟡 Original Data Snapshot: {self.original_data}")
        
        self.tableWidget_Users.blockSignals(False)  # ✅ Enable signals back after loading


   
    def track_changes(self, item):
        """Track changes when cells are modified."""
        row = item.row()
        column = item.column()

        # Retrieve user_id for change tracking
        user_id_item = self.tableWidget_Users.item(row, 0)
        user_id = user_id_item.data(QtCore.Qt.UserRole)

        if not user_id:
            print(f"❗Skipping row {row} - No user_id found")
            return

        # Reference original data
        original_values = self.original_data.get(user_id, {})

        # Capture the new value
        new_value = item.text().strip()

        # Track changes only if new value differs from original
        if user_id not in self.changes:
            self.changes[user_id] = {}

        # Username
        if column == 0 and new_value != original_values.get("username", ""):
            self.changes[user_id]['username'] = new_value

        # Role
        elif column == 1 and new_value != original_values.get("role", ""):
            self.changes[user_id]['role'] = new_value

        # Password
        elif column == 2 and new_value:
            self.changes[user_id]['password'] = new_value

        # Full Name
        elif column == 3 and new_value != original_values.get("full_name", ""):
            self.changes[user_id]['full_name'] = new_value

        # Email
        elif column == 4 and new_value != original_values.get("email_addr", ""):
            self.changes[user_id]['email_addr'] = new_value

        # Max Logins
        elif column == 5 and new_value != original_values.get("max_logins", ""):
            self.changes[user_id]['max_logins'] = new_value

        # Pallet Cap
        elif column == 6 and new_value != original_values.get("pall_cap", ""):
            self.changes[user_id]['pall_cap'] = new_value


        print(f"🟩 Tracking Changes: {self.changes}")



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

                user_data = {}

                if "username" in updated_data:
                    user_data["username"] = updated_data["username"].upper()

                if "role" in updated_data:
                    user_data["role"] = updated_data["role"]

                if "full_name" in updated_data:
                    user_data["full_name"] = updated_data["full_name"]

                if "email_addr" in updated_data:
                    user_data["email_addr"] = updated_data["email_addr"]

                if "max_logins" in updated_data:
                    try:
                        user_data["max_logins"] = int(updated_data["max_logins"])
                    except ValueError:
                        user_data["max_logins"] = 0  # O manejar de otra forma

                if "pall_cap" in updated_data:
                    try:
                        user_data["pall_cap"] = int(updated_data["pall_cap"])
                    except ValueError:
                        user_data["pall_cap"] = 0

                if "password" in updated_data and updated_data["password"].strip():
                    user_data["password"] = updated_data["password"]


                if "password" in updated_data and updated_data["password"].strip():
                    user_data["password"] = updated_data["password"]
                    
                print(f"🧩 Updating User ID: {user_id}")
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

            # ✅ Reload table after successful updates
            self.changes.clear()
            self.load_users()

        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

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


    def discard_users(self):
        """Reload the data from the database to discard unsaved changes."""
        confirm = QtWidgets.QMessageBox.question(
            self, "Reset", "Are you sure you want to reset all unsaved changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            self.load_users()  # Reload data to reset changes
            self.changes.clear()
            QtWidgets.QMessageBox.information(self, "Reset", "All unsaved changes have been discarded.")