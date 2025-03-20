from PyQt5 import QtWidgets, uic
import requests

class NewUserDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("WMS_System/UI/CreateNewUser.ui", self)

        # Reference UI Elements
        self.user_input = self.findChild(QtWidgets.QLineEdit, 'User_Input')
        self.password_input = self.findChild(QtWidgets.QLineEdit, 'Password_Input')
        self.role_input = self.findChild(QtWidgets.QLineEdit, 'Role_Input')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')

        # Connect the "OK" and "Cancel" buttons
        self.buttonBox.accepted.connect(self.save_new_user)
        self.buttonBox.rejected.connect(self.reject)

    def save_new_user(self):
        """Send the new user data to FastAPI for saving."""
        username = self.user_input.text().strip().upper()
        password = self.password_input.text().strip()
        role = self.role_input.text().strip()

        # Input validation
        if not username or not password or not role:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required!")
            return

        # Prepare data for the API request
        new_user_data = {
            "username": username,
            "password": password,
            "role": role
        }

        try:
            response = requests.post("http://localhost:8000/Users/", json=new_user_data)

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "New user created successfully!")
                self.accept()  # Close the dialog
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to create new user.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")
