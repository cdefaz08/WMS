from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow.ui", self)

    # Reference Logout Action
        self.actionLogout = self.findChild(QtWidgets.QAction, 'actionLogout')

        # Connect Logout Action to Logout Function
        self.actionLogout.triggered.connect(self.logout)

    def logout(self):
        confirm = QtWidgets.QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            self.close()  # Close the Main Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
