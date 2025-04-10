from PyQt5 import QtWidgets, QtCore
import requests
from config import API_BASE_URL
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.Location_search_ui import Ui_LocationSearch

class LocationSearchWindow(QtWidgets.QDialog, Ui_LocationSearch):
    def __init__(self,api_client = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client

        self.pushButton_Search.clicked.connect(self.search_locations)
        self.load_class_dropdowns()


        self.tableViewItemSearch.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableViewItemSearch.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewItemSearch.verticalHeader().setVisible(False)

        # Trigger search on Enter
        self.lineEdit_Location.returnPressed.connect(self.search_locations)
        self.lineEdit_Aisle.returnPressed.connect(self.search_locations)
        self.lineEdit_Bay.returnPressed.connect(self.search_locations)
        self.lineEdit_Level.returnPressed.connect(self.search_locations)
        self.lineEdit_Slot.returnPressed.connect(self.search_locations)
        self.lineEdit_ProximityIN.returnPressed.connect(self.search_locations)
        self.lineEdit_ProximityOUT.returnPressed.connect(self.search_locations)


    def load_class_dropdowns(self):
        try:
            restock_response = requests.get(f"{API_BASE_URL}/classes/restock")
            putaway_response = requests.get(f"{API_BASE_URL}/classes/putaway")
            pick_response = requests.get(f"{API_BASE_URL}/classes/pick")
            location_type = requests.get(f"{API_BASE_URL}/location-types")

            if restock_response.status_code == 200:
                restock_classes = restock_response.json()
                self.comboBox_ResotckClass.clear()
                self.comboBox_ResotckClass.addItem("")  # Optional default blank
                for r in restock_classes:
                    self.comboBox_ResotckClass.addItem(r["class_name"])

            if putaway_response.status_code == 200:
                putaway_classes = putaway_response.json()
                self.comboBox_PutawasClass.clear()
                self.comboBox_PutawasClass.addItem("")
                for p in putaway_classes:
                    self.comboBox_PutawasClass.addItem(p["class_name"])

            if pick_response.status_code == 200:
                pick_classes = pick_response.json()
                self.comboBox_PickClass.clear()
                self.comboBox_PickClass.addItem("")
                for p in pick_classes:
                    self.comboBox_PickClass.addItem(p["class_name"])

            if location_type.status_code == 200:
                location_types = location_type.json()
                self.comboBoxLocationType.clear()
                self.comboBoxLocationType.addItem("")
                for lt in location_types:
                    self.comboBoxLocationType.addItem(lt["location_type"])

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load class data.\n{str(e)}")


    def search_locations(self):
        # Build search filters (can be expanded later)
        filters = {
            "location_id": self.lineEdit_Location.text().strip().lower(),
            "aisle": self.lineEdit_Aisle.text().strip().lower(),
            "bay": self.lineEdit_Bay.text().strip().lower(),
            "loc_level": self.lineEdit_Level.text().strip().lower(),
            "slot": self.lineEdit_Slot.text().strip().lower(),
            "putaway_class": self.comboBox_PutawasClass.currentText().strip().lower(),
            "rstk_class": self.comboBox_ResotckClass.currentText().strip().lower(),
            "pick_class": self.comboBox_PickClass.currentText().strip().lower(),
            "blocked_code": self.comboBox_BlockCode.currentText().strip().lower(),
            "location_type": self.comboBoxLocationType.currentText().strip().lower(),
            "proximiti_in": self.lineEdit_ProximityIN.text().strip().lower(),
            "proximiti_out": self.lineEdit_ProximityOUT.text().strip().lower()
        }

        try:
            response = requests.get(f"{API_BASE_URL}/locations")
            if response.status_code == 200:
                locations = response.json()

                # If all filters are empty, return everything
                if not any(filters.values()):
                    self.populate_table(locations)
                    return

                filtered = []
                for loc in locations:
                    match = True
                    for key, val in filters.items():
                        if val and val not in str(loc.get(key, "")).lower():
                            match = False
                            break
                    if match:
                        filtered.append(loc)

                self.populate_table(filtered)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to fetch locations.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to server.")

    def populate_table(self, locations):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Location ID", "Scan Location", "Location Type", "Putaway", "Restock", "Pick", 
            "Aisle", "Bay", "Level", "Slot"
        ])

        for loc in locations:
            row = [
                QStandardItem(loc.get("location_id", "")),
                QStandardItem(loc.get("scan_location", "")),
                QStandardItem(loc.get("location_type", "")),
                QStandardItem(loc.get("putaway_class", "")),
                QStandardItem(loc.get("rstk_class", "")),
                QStandardItem(loc.get("pick_class", "")),
                QStandardItem(loc.get("aisle", "")),
                QStandardItem(loc.get("bay", "")),
                QStandardItem(loc.get("loc_level", "")),
                QStandardItem(loc.get("slot", ""))
            ]
            model.appendRow(row)

        self.tableViewItemSearch.setModel(model)
        self.Records.setText(f"Records found: <b>{len(locations)}</b>")
        self.tableViewItemSearch.horizontalHeader().setStretchLastSection(True)


    def clear_filters(self):
        self.lineEdit_Location.clear()
        self.lineEdit_Aisle.clear()
        self.lineEdit_Bay.clear()
        self.lineEdit_Level.clear()
        self.lineEdit_Slot.clear()
        self.lineEdit_ProximityIN.clear()
        self.lineEdit_ProximityOUT.clear()

        self.comboBox_PutawasClass.setCurrentIndex(0)
        self.comboBox_ResotckClass.setCurrentIndex(0)
        self.comboBox_PickClass.setCurrentIndex(0)
        self.comboBox_BlockCode.setCurrentIndex(0)
        self.comboBoxLocationType.setCurrentIndex(0)

    def get_selected_location_id(self):
        if not self.tableViewItemSearch:
            return None

        selection_model = self.tableViewItemSearch.selectionModel()
        if not selection_model:
            return None

        indexes = selection_model.selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewItemSearch.model()
        row = indexes[0].row()

        location_id = model.index(row, 0).data(QtCore.Qt.DisplayRole)
        return location_id.strip() if location_id else None

    
    def delete_selected_location(self):
        print(">>> delete_selected_location() called")

        # Prevent double-click issue
        if getattr(self, "_is_deleting", False):
            print(">>> Already deleting, skipping.")
            return
        self._is_deleting = True

        try:
            location_id = self.get_selected_location_id()
            if not location_id:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a location to delete.")
                return

            confirm = QtWidgets.QMessageBox.question(
                self,
                "Confirm Delete",
                "Are you sure you want to delete this location?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm != QtWidgets.QMessageBox.Yes:
                return

            url = f"{API_BASE_URL}/locations/{location_id}"
            print("DELETE URL:", url)

            response = requests.delete(url)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Deleted", "Location successfully deleted.")
                self.search_locations()
            elif response.status_code == 404:
                QtWidgets.QMessageBox.warning(self, "Error", "Location not found.")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete location.\n{response.text}")

        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
        finally:
            self._is_deleting = False






