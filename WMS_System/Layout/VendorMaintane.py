from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import requests
from Layout.UI_PY.vendor_maintance_ui import Ui_VendorMaintance
from config import API_BASE_URL

class VendorMaintanceDialog(QtWidgets.QDialog, Ui_VendorMaintance):
    vendor_updated = pyqtSignal()

    def __init__(self,api_client = None, vendor_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Vendor Maintenance")
        self.api_client = api_client
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
        vendor_id = self.original_data.get("id")
        is_edit = vendor_id is not None

        if is_edit:
            updated_fields = self.get_updated_fields()
            if not updated_fields:
                QtWidgets.QMessageBox.information(self, "No Changes", "No fields were modified.")
                return
            payload = updated_fields
            url = f"{API_BASE_URL}/vendors/{vendor_id}"
            method = requests.put
        else:
            # Collect all fields for creation
            payload = {
                "vendor_code": self.lineEdit_VendorCode.text().strip(),
                "vendor_name": self.lineEdit_VendorName.text().strip(),
                "contact_name": self.lineEdit_ContactName.text().strip(),
                "tax_id": self.lineEdit_TaxId.text().strip(),
                "phone": self.lineEdit_Phone.text().strip(),
                "email": self.lineEdit_Email.text().strip(),
                "address": self.lineEdit_Address.text().strip(),
                "city": self.lineEdit_City.text().strip(),
                "state": self.lineEdit_State.text().strip(),
                "country": self.lineEdit_Country.text().strip(),
                "zip_code": self.lineEdit_ZipCode.text().strip(),
                "notes": self.textEdit_notes.toPlainText().strip()
            }
            url = f"{API_BASE_URL}/vendors/"
            method = requests.post

        try:
            response = method(url, json=payload)
            if response.status_code in (200, 201):
                QtWidgets.QMessageBox.information(self, "Success", "Vendor saved successfully.")  
                mdi = self.parent()
                while mdi and not isinstance(mdi, QtWidgets.QMdiSubWindow):
                    mdi = mdi.parent()
                if mdi:
                    mdi.close()
                else:
                    self.close()      
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to save vendor:\n{response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Connection Error", "Could not connect to server.")

