from PyQt5 import QtWidgets, uic
import sys
from item_search import ItemSearchWindow  # Import the new sub-window
from User_table import UsersTableWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("WMS_System/UI/MainWindow.ui", self)

        # Reference Actions
        self.actionLogout = self.findChild(QtWidgets.QAction, 'actionLogout')
        self.actionItem_Search = self.findChild(QtWidgets.QAction, 'actionItem_Search')
        self.actionUser_table = self.findChild(QtWidgets.QAction, 'actionUsers')

        # Connect Actions
        
        self.actionLogout.triggered.connect(self.logout)
        self.actionItem_Search.triggered.connect(self.open_item_search)
        self.actionUser_table.triggered.connect(self.open_user_table)

    def logout(self):
        confirm = QtWidgets.QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.close()  # Close the Main Window

    def open_item_search(self):
        self.item_search_window = ItemSearchWindow()
        self.item_search_window.show()

    def open_user_table(self):
        self.Users_window = UsersTableWindow()
        self.Users_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())