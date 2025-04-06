from PyQt5 import QtWidgets, uic
import requests
from config import API_BASE_URL

class NewUserDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/CreateNewUser.ui", self)

        # Reference UI Elements
        self.UserName = self.findChild(QtWidgets.QLineEdit, 'UserName')
        self.FullName = self.findChild(QtWidgets.QLineEdit, 'FullName')
        self.Password_Input = self.findChild(QtWidgets.QLineEdit, 'Password_Input')
        self.Role = self.findChild(QtWidgets.QLineEdit, 'Role')
        self.MaxLogins = self.findChild(QtWidgets.QLineEdit, 'MaxLogins')
        self.EmailAddres = self.findChild(QtWidgets.QLineEdit, 'EmailAddres')
        self.PallCap = self.findChild(QtWidgets.QLineEdit, 'PallCap')
        self.Comments = self.findChild(QtWidgets.QLineEdit, 'Comments')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')

        # Connect the "OK" and "Cancel" buttons
        self.buttonBox.accepted.connect(self.save_new_user)
        self.buttonBox.rejected.connect(self.reject)

    def save_new_user(self):
        """Send the new user data to FastAPI for saving."""
        username = self.UserName.text().strip().upper()
        fullname = self.FullName.text().strip()
        password = self.Password_Input.text().strip()
        role = self.Role.text().strip()
        maxLogins = self.MaxLogins.text().strip()
        emailAddr = self.EmailAddres.text().strip()
        pallCap = self.PallCap.text().strip()
        comments = self.Comments.text().strip()


        # Input validation
        if not username or not password or not role:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required!")
            return

        # Prepare data for the API request
        new_user_data = {
            "username": username,
            "full_name": fullname,
            "password": password,
            "role": role,
            "max_logins": maxLogins,
            "email_addr": emailAddr,
            "pall_cap": pallCap,
            "comments": comments
        }

        try:
            response = requests.post(f"{API_BASE_URL}/Users/", json=new_user_data)

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "New user created successfully!")
                self.accept()  # Close the dialog
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to create new user.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")
