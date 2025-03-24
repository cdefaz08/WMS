from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt 
import sys
from item_search import ItemSearchWindow  # Import the new sub-window
from User_table import UsersTableWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/MainWindow.ui", self)

        #connect Tollbar
        self.connect_toolbar()

        self.mdiArea = self.findChild(QtWidgets.QMdiArea, 'mdiArea')

        # Reference Actions
        self.actionLogout = self.findChild(QtWidgets.QAction, 'actionLogout')
        self.actionItem_Search = self.findChild(QtWidgets.QAction, 'actionItem_Search')
        self.actionUser_table = self.findChild(QtWidgets.QAction, 'actionUsers')

        # Connect Actions
        
        self.actionLogout.triggered.connect(self.logout)
        self.actionItem_Search.triggered.connect(self.open_item_search)
        self.actionUser_table.triggered.connect(self.open_user_table)

        

        #toolbar Actions
        

    def get_active_window(self):
        active_subwindow = self.mdiArea.activeSubWindow()
        if active_subwindow:
            return active_subwindow.widget()
        return None  # No active window
        
    def logout(self):
        confirm = QtWidgets.QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.close()  # Close the Main Window

    #----------------------------Connect the Toolbar-----------------------------------
    def connect_toolbar(self):
        self.new_button = self.findChild(QtWidgets.QAction, 'actionNew')
        self.save_button = self.findChild(QtWidgets.QAction, 'actionSave')
        self.discard_button = self.findChild(QtWidgets.QAction, 'actionDiscard')
        self.refresh_button = self.findChild(QtWidgets.QAction, 'actionRefresh')

        self.new_button.triggered.connect(self.toolbar_new)
        self.save_button.triggered.connect(self.toolbar_save)
        self.discard_button.triggered.connect(self.toolbar_discard)
    #----------------------------Tolbar New Window-----------------------------------
    def toolbar_new(self):
        active_window = self.get_active_window()

        if isinstance(active_window, ItemSearchWindow):
            active_window.open_add_item_dialog()  # Example function in ItemSearchWindow
        elif isinstance(active_window, UsersTableWindow):
            active_window.add_new_user()  # Example function in UsersTableWindow
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    #----------------------------Toolbar Save Triger-----------------------------------
    def toolbar_save(self):
        active_window = self.get_active_window()

        if isinstance(active_window, ItemSearchWindow):
            active_window.save_changes()  # Example function in ItemSearchWindow
        elif isinstance(active_window, UsersTableWindow):
            active_window.save_changes()  # Example function in UsersTableWindow
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    #----------------------------Toolbar Discard Triger-----------------------------------
    
    def toolbar_discard(self):
        active_window = self.get_active_window()

        if isinstance(active_window, ItemSearchWindow):
            active_window.discard_changes()  # Example function in ItemSearchWindow
        elif isinstance(active_window, UsersTableWindow):
            active_window.discard_users()  # Example function in UsersTableWindow
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    #----------------------------Open Item Search Table----------------------------------- 
    def open_item_search(self):
        # Check if the window is already open to avoid duplicates
        for sub_window in self.mdiArea.subWindowList():
            if isinstance(sub_window.widget(), ItemSearchWindow):
                sub_window.show()
                sub_window.setFocus()
                return  

        # Create a new QMdiSubWindow
        item_search_subwindow = QtWidgets.QMdiSubWindow()
        self.item_search_window = ItemSearchWindow(self)
        item_search_subwindow.setWidget(self.item_search_window)
        item_search_subwindow.setWindowTitle("Item Search")

        # Ensure the subwindow is deleted when closed
        item_search_subwindow.setAttribute(Qt.WA_DeleteOnClose)

        item_search_subwindow.resize(600,400)

        self.mdiArea.addSubWindow(item_search_subwindow)
        item_search_subwindow.show()

    #----------------------------Open User Table----------------------------------- 
    def open_user_table(self):
        for sub_window in self.mdiArea.subWindowList():
            if isinstance(sub_window.widget(), UsersTableWindow):
                sub_window.show()
                sub_window.setFocus()
                return
        
        user_search_subwindow = QtWidgets. QMdiSubWindow()
        self.user_search_window = UsersTableWindow()
        user_search_subwindow.setWidget(self.user_search_window)
        user_search_subwindow.setWindowTitle ("User Search")

        #Ensure the subwindow is deleted when closed
        user_search_subwindow.setAttribute(Qt.WA_DeleteOnClose)

        user_search_subwindow.resize(600, 400)

        self.mdiArea.addSubWindow(user_search_subwindow)
        user_search_subwindow.show()
    
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())