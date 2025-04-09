# vendor_search_window.py

from PyQt5 import QtWidgets, QtCore
import requests
from config import API_BASE_URL
from Layout.UI_PY.vendor_search_ui import Ui_VendorSearch  # Update path if needed
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class VendorSearchWindow(QtWidgets.QDialog, Ui_VendorSearch):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Connect ENTER key for all fields
        self.lineEdit_VendorCode.returnPressed.connect(self.search_vendors)
        self.lineEdit_VendorName.returnPressed.connect(self.search_vendors)
        self.lineEdit_ContactName.returnPressed.connect(self.search_vendors)
        self.lineEdit_Phone.returnPressed.connect(self.search_vendors)
        self.lineEdit_Email.returnPressed.connect(self.search_vendors)
        self.lineEdit_TaxId.returnPressed.connect(self.search_vendors)
        self.lineEdit_City.returnPressed.connect(self.search_vendors)
        self.lineEdit_State.returnPressed.connect(self.search_vendors)
        self.lineEdit_Country.returnPressed.connect(self.search_vendors)
        self.lineEdit_ZipCode.returnPressed.connect(self.search_vendors)

        self.pushButton_Search.clicked.connect(self.search_vendors)

        self.tableViewItemSearch.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewItemSearch.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewItemSearch.verticalHeader().setVisible(False)

    def search_vendors(self):
        search_data = {
            "vendor_code": self.lineEdit_VendorCode.text().strip().lower(),
            "vendor_name": self.lineEdit_VendorName.text().strip().lower(),
            "contact_name": self.lineEdit_ContactName.text().strip().lower(),
            "phone": self.lineEdit_Phone.text().strip(),
            "email": self.lineEdit_Email.text().strip(),
            "tax_id": self.lineEdit_TaxId.text().strip(),
            "city": self.lineEdit_City.text().strip().lower(),
            "state": self.lineEdit_State.text().strip().lower(),
            "country": self.lineEdit_Country.text().strip().lower(),
            "zip_code": self.lineEdit_ZipCode.text().strip()
        }

        try:
            response = requests.get(f"{API_BASE_URL}/vendors/")
            if response.status_code == 200:
                vendors = response.json()

                if not any(search_data.values()):
                    self.populate_table(vendors)
                    return

                filtered = []
                for vendor in vendors:
                    match = True
                    for key, value in search_data.items():
                        if value:
                            vendor_value = str(vendor.get(key, "")).lower()
                            if value not in vendor_value:
                                match = False
                                break
                    if match:
                        filtered.append(vendor)

                self.populate_table(filtered)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load vendors")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")

    def populate_table(self, vendors):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "ID", "Code", "Name", "Contact", "Phone", "Email", "City", "State", "Country", "Zip"
        ])

        for vendor in vendors:
            vendor_id_item = QStandardItem(str(vendor.get("id", "")))
            vendor_id_item.setData(str(vendor.get("id", "")), QtCore.Qt.UserRole)

            row = [
                vendor_id_item,
                QStandardItem(str(vendor.get("vendor_code", ""))),
                QStandardItem(str(vendor.get("vendor_name", ""))),
                QStandardItem(str(vendor.get("contact_name", ""))),
                QStandardItem(str(vendor.get("phone", ""))),
                QStandardItem(str(vendor.get("email", ""))),
                QStandardItem(str(vendor.get("city", ""))),
                QStandardItem(str(vendor.get("state", ""))),
                QStandardItem(str(vendor.get("country", ""))),
                QStandardItem(str(vendor.get("zip_code", ""))),
            ]
            model.appendRow(row)

        self.tableViewItemSearch.setModel(model)
        self.tableViewItemSearch.setColumnHidden(0, True)
        self.Records.setText(f"Records found: <b>{len(vendors)}</b>")

        self.tableViewItemSearch.setColumnWidth(0, 50)   # ID
        self.tableViewItemSearch.setColumnWidth(1, 100)  # Code
        self.tableViewItemSearch.setColumnWidth(2, 180)  # Name
        self.tableViewItemSearch.setColumnWidth(3, 150)  # Contact
        self.tableViewItemSearch.setColumnWidth(4, 100)  # Phone
        self.tableViewItemSearch.setColumnWidth(5, 160)  # Email
        self.tableViewItemSearch.setColumnWidth(6, 100)  # City
        self.tableViewItemSearch.setColumnWidth(7, 80)   # State
        self.tableViewItemSearch.setColumnWidth(8, 100)  # Country
        self.tableViewItemSearch.setColumnWidth(9, 80)   # Zip

        self.tableViewItemSearch.horizontalHeader().setStretchLastSection(True)

    def get_selected_vendor_id(self):
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

        return model.index(row, 0).data(QtCore.Qt.UserRole)
    
    def clear_filters(self):
        self.lineEdit_VendorCode.clear()
        self.lineEdit_VendorName.clear()
        self.lineEdit_ContactName.clear()
        self.lineEdit_Phone.clear()
        self.lineEdit_Email.clear()
        self.lineEdit_TaxId.clear()
        self.lineEdit_City.clear()
        self.lineEdit_State.clear()
        self.lineEdit_Country.clear()
        self.lineEdit_ZipCode.clear()

    def delete_selected_vendor(self):
        vendor_id = self.get_selected_vendor_id()

        if not vendor_id:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a vendor to delete.")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete the selected vendor?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.No:
            return

        try:
            response = requests.delete(f"{API_BASE_URL}/vendors/{vendor_id}")
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Vendor deleted successfully.")
                self.search_vendors()  # Refresh list
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete vendor:\n{response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")
    

