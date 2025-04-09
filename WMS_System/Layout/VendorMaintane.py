from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import requests
from Layout.UI_PY.vendor_maintance_ui import Ui_VendorMaintance
from config import API_BASE_URL

class VendorMaintanceDialog(QtWidgets.QDialog, Ui_VendorMaintance):
    vendor_updated = pyqtSignal()

    def __init__(self, vendor_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Vendor Maintenance")
        self.original_data = vendor_data or {}
        
        if vendor_data:
            self.load_vendor_data(vendor_data)

    def load_vendor_data(self, vendor):
        self.lineEdit_VendorCode.setText(vendor.get("vendor_code", ""))
        self.lineEdit_VendorName.setText(vendor.get("vendor_name", ""))
        self.lineEdit_ContactName.setText(vendor.get("contact_name", ""))
        self.lineEdit_TaxId.setText(vendor.get("tax_id", ""))
        self.lineEdit_Phone.setText(vendor.get("phone", ""))
        self.lineEdit_Email.setText(vendor.get("email", ""))
        self.lineEdit_City.setText(vendor.get("city", ""))
        self.lineEdit_State.setText(vendor.get("state", ""))
        self.lineEdit_Address.setText(vendor.get("address", ""))
        self.lineEdit_Country.setText(vendor.get("country", ""))
        self.lineEdit_ZipCode.setText(vendor.get("zip_code", ""))
        self.textEdit_notes.setPlainText(vendor.get("notes", ""))

    def get_updated_fields(self):
        updated = {}

        def check(key, widget):
            current = widget.text().strip()
            original = str(self.original_data.get(key, "") or "").strip()
            if current != original:
                updated[key] = current

        check("vendor_code", self.lineEdit_VendorCode)
        check("vendor_name", self.lineEdit_VendorName)
        check("contact_name", self.lineEdit_ContactName)
        check("tax_id", self.lineEdit_TaxId)
        check("phone", self.lineEdit_Phone)
        check("email", self.lineEdit_Email)
        check("city", self.lineEdit_City)
        check("state", self.lineEdit_State)
        check("address", self.lineEdit_Address)
        check("country", self.lineEdit_Country)
        check("zip_code", self.lineEdit_ZipCode)

        current_notes = self.textEdit_notes.toPlainText().strip()
        original_notes = str(self.original_data.get("notes", "") or "").strip()
        if current_notes != original_notes:
            updated["notes"] = current_notes


        return updated

    def save_changes(self):
        updated_fields = self.get_updated_fields()
        if not updated_fields:
            QtWidgets.QMessageBox.information(self, "No Changes", "No fields were modified.")
            return

        vendor_id = self.original_data.get("id")
        if not vendor_id:
            QtWidgets.QMessageBox.warning(self, "Error", "Vendor ID is missing.")
            return

        try:
            print("JSON to send:",vendor_id, updated_fields)
            response = requests.put(f"{API_BASE_URL}/vendors/{vendor_id}", json=updated_fields)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Vendor updated successfully.")
                if hasattr(self, "parent_subwindow") and self.parent_subwindow:
                    self.parent_subwindow.close()
                else:
                    self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update vendor:\n{response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Connection Error", "Could not connect to server.")
