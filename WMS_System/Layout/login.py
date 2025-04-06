from PyQt5 import QtWidgets, uic
from config import API_BASE_URL
import requests
from Layout.MainWindow import MainWindow
from PyQt5.QtGui import QFont

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/Login_layout.ui", self)

        font = QFont("Segoe UI", 60, QFont.Bold)
        
        # Reference UI Elements
        self.User_input = self.findChild(QtWidgets.QLineEdit, 'User_input')
        self.Passw_data = self.findChild(QtWidgets.QLineEdit, 'Passw_data')
        self.btn_Login = self.findChild(QtWidgets.QPushButton, 'btn_Login')
        self.btn_Cancel = self.findChild(QtWidgets.QPushButton, 'btn_Cancel')
        self.lb_Welcome = self.findChild(QtWidgets.QLabel, 'lb_Welcome')

        self.User_input.textChanged.connect(self.force_uppercase)
        self.lb_Welcome.setFont(font)

        # Set Password Field to Show `******`
        self.Passw_data.setEchoMode(QtWidgets.QLineEdit.Password)

        self.Passw_data.returnPressed.connect(self.handle_login)  # Enter triggers Login

        # Connect the Login Button
        self.btn_Login.clicked.connect(self.handle_login)

    def force_uppercase(self):
        text = self.User_input.text()
        self.User_input.setText(text.upper())

    def handle_login(self):
        username = self.User_input.text()
        password = self.Passw_data.text()

        #FastAPI enpoint
        url = f"{API_BASE_URL}/login/"

        #Sta to send to FastAPI
        data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=data)  # Note: Using `params` for query parameters
            if response.status_code == 200:
                self.open_main_window()
            elif response.status_code == 404:
                QtWidgets.QMessageBox.warning(self, "Error", "User not found")
            elif response.status_code == 400:
                QtWidgets.QMessageBox.warning(self, "Error", "Incorrect password")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Login failed for unknown reasons")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

    def open_main_window(self):
        self.main_window = MainWindow()  # Create instance of Main Window
        self.main_window.showMaximized()         # Show the Main Window
        self.close()
