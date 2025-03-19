from PyQt5 import QtWidgets, uic
import sys

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/layout.ui", self)
        
        # Reference UI Elements
        self.User_input = self.findChild(QtWidgets.QLineEdit, 'User_input')
        self.Passw_data = self.findChild(QtWidgets.QLineEdit, 'Passw_data')
        self.btn_Login = self.findChild(QtWidgets.QPushButton, 'btn_Login')
        self.btn_Cancel = self.findChild(QtWidgets.QPushButton, 'btn_Cancel')

      # Connect the Login Button
        self.btn_Login.clicked.connect(self.handle_login)
        print("User_input:", self.User_input)
        print("Passw_data:", self.Passw_data)   

    def handle_login(self):
        username = self.User_input.text()
        password = self.Passw_data.text()

        # Dummy Login Logic (Connect to FastAPI in future)
        if username == "admin" and password == "password":
            QtWidgets.QMessageBox.information(self, "Success", "Login Successful!")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid Username or Password")

   

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
