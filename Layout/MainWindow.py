from PyQt5 import QtWidgets, uic
import sys
from item_search import ItemSearchWindow  # Import the new sub-window

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow.ui", self)

        # Reference Actions
        self.actionLogout = self.findChild(QtWidgets.QAction, 'actionLogout')
        self.actionItem_Search = self.findChild(QtWidgets.QAction, 'actionItem_Search')

        # Connect Actions
        self.actionLogout.triggered.connect(self.logout)
        self.actionItem_Search.triggered.connect(self.open_item_search)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
