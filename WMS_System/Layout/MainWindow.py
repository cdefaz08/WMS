from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt 
import requests
import sys
from item_search import ItemSearchWindow  # Import the new sub-window
from User_table import UsersTableWindow
from itemMaintanceDialog import ItemMaintanceDialog
from add_item_dialog import AddItemDialog
from LocationType_Win import LocationTypes
from LocationType_Maintance import LocationType_Maintance



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
        self.actionLocation_Types = self.findChild(QtWidgets.QAction,"actionLocation_Types")
        


        # Connect Actions
        
        self.actionLogout.triggered.connect(self.logout)
        self.actionItem_Search.triggered.connect(self.open_item_search)
        self.actionUser_table.triggered.connect(self.open_user_table)
        self.actionLocation_Types.triggered.connect(self.open_locationType_win)
              
        

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
        self.actionItemMaintance = self.findChild(QtWidgets.QAction, "actionItemMaintance")
        self.actionItemMaintance.setVisible(False)
        self.new_button.triggered.connect(self.toolbar_new)
        self.save_button.triggered.connect(self.toolbar_save)
        self.discard_button.triggered.connect(self.toolbar_discard)
        self.actionItemMaintance.triggered.connect(self.open_maintance_window)

    def open_maintance_window(self):
        active_window = self.get_active_window()

        if isinstance(active_window, ItemSearchWindow):
            item_id = active_window.get_selected_item_id()

            if item_id:
                try:
                    response = requests.get(f"http://localhost:8000/items/{item_id}")
                    if response.status_code == 200:
                        item_data = response.json()

                        # Crear subventana MDI
                        subwindow = QtWidgets.QMdiSubWindow()
                        item_dialog = ItemMaintanceDialog(item_data=item_data, parent=self)
                        item_dialog.subwindow = subwindow
                        item_dialog.item_updated.connect(active_window.search_items)
                        
                        subwindow.setWidget(item_dialog)
                        subwindow.setWindowTitle("Item Code Maintanance")

                        subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                        subwindow.resize(700, 600)

                        self.mdiArea.addSubWindow(subwindow)
                        subwindow.show()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window , LocationTypes):
            Locationtype = active_window.get_selected_item_id()

            if Locationtype:
                try: 
                    response = requests.get(f"http://localhost:8000/location-types/{Locationtype}")
                    if response.status_code == 200:
                        locationTypeData = response.json()
                        # Need to create the subwindow and mapp the correct data into the screnn
                        subwindow = QtWidgets.QMdiSubWindow()
                        loc_type_subwin = LocationType_Maintance(locationTypeData = locationTypeData, parent = self)
                        loc_type_subwin.subwindow = subwindow

                        subwindow.setWidget(loc_type_subwin)
                        subwindow.setWindowTitle("Location Type Maintance")

                        subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                        subwindow.resize(902, 384)
                        self.mdiArea.addSubWindow(subwindow)
                        subwindow.show()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")

    #----------------------------Tolbar New Window-----------------------------------
    def toolbar_new(self):
        active_window = self.get_active_window()

        if isinstance(active_window, ItemSearchWindow):
            for sub_window in self.mdiArea.subWindowList():
                if isinstance(sub_window.widget(), AddItemDialog):
                    sub_window.show()
                    sub_window.setFocus()
                    return 
            add_dialog = AddItemDialog(parent=self)
            

            # Create and show as MDI subwindow
            subwindow = QtWidgets.QMdiSubWindow()
            subwindow.setWidget(add_dialog)
            subwindow.setWindowTitle("Add New Item")
            subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            subwindow.resize(805,569)
            add_dialog.parent_subwindow = subwindow

            self.mdiArea.addSubWindow(subwindow)
            subwindow.show()
            
        elif isinstance(active_window, UsersTableWindow):
            active_window.add_new_user()  # Example function in UsersTableWindow
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    #----------------------------Toolbar Save Triger-----------------------------------
    def toolbar_save(self):
        active_window = self.get_active_window()

        if isinstance(active_window, UsersTableWindow):
            active_window.save_changes() 
        elif isinstance(active_window,ItemMaintanceDialog):
            active_window.save_changes()
        elif isinstance(active_window,AddItemDialog):
            active_window.createItem()
        elif isinstance(active_window,LocationType_Maintance):
            active_window.save_changes()
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    #----------------------------Toolbar Discard Triger-----------------------------------
    
    def toolbar_discard(self):
        active_window = self.get_active_window()

        if isinstance(active_window, UsersTableWindow):
            active_window.discard_users()  # Example function in UsersTableWindow
        elif isinstance(active_window,ItemSearchWindow):
            active_window.clear_filters()
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")


    #----------------------------Open location Type Window----------------------------------- 
    def open_locationType_win(self):
        for sub_window in self.mdiArea.subWindowList():
            if isinstance(sub_window.widget(),LocationTypes):
                sub_window.show()
                sub_window.setFocus()
                return
            
        locationType_subwindow = QtWidgets.QMdiSubWindow()
        self.locationType_subwindow = LocationTypes(self)
        locationType_subwindow.setWidget(self.locationType_subwindow)
        locationType_subwindow.setWindowTitle("Location Types")
        self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
        self.actionItemMaintance.setVisible(True)
        self.locationType_subwindow.destroyed.connect(self.hide_item_toolbar_action)
        locationType_subwindow.setAttribute(Qt.WA_DeleteOnClose) # Ensure the subwindow is deleted when closed
        locationType_subwindow.resize(500,600)
        self.mdiArea.addSubWindow(locationType_subwindow)
        locationType_subwindow.show()

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
        self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
        self.actionItemMaintance.setVisible(True)
        self.item_search_window.destroyed.connect(self.hide_item_toolbar_action)
        item_search_subwindow.setAttribute(Qt.WA_DeleteOnClose) # Ensure the subwindow is deleted when closed
        item_search_subwindow.resize(1089,766)
        self.mdiArea.addSubWindow(item_search_subwindow)
        item_search_subwindow.show()
    
    def hide_item_toolbar_action(self):
        self.actionItemMaintance.setVisible(False)
    #--------------------------Subwindow Focus Change----------------------------
    def handle_subwindow_focus_change(self, active_window):
        if active_window is None:
            # No subwindow active, hide the toolbar button
            self.actionItemMaintance.setVisible(False)
            return

        widget = active_window.widget()
        
        if isinstance(widget, ItemSearchWindow):
            self.actionItemMaintance.setVisible(True)
        elif isinstance(widget, LocationTypes):
            self.actionItemMaintance.setVisible(True)
        else:
            self.actionItemMaintance.setVisible(False)
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