# ReceiptMaintance.py
from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_ReceiptMaintance import Ui_OrderMaintance
from Layout.Activities.ReceiptLinesWindow import ReceiptLinesWindow
import requests
from config import API_BASE_URL
from datetime import datetime

class ReceiptMaintanceWindow(QtWidgets.QDialog, Ui_OrderMaintance):
    def __init__(self, api_client=None, receipt_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.receipt_data = receipt_data
        self.init_receipt_lines_tab_if_ready()

        self.original_data = receipt_data.copy() if receipt_data else {}
        self.setWindowTitle("Edit Receipt" if self.receipt_data else "Create Receipt")

        self.dateEdit_OrderDate.setCalendarPopup(True)
        self.dateEdit_ShipDate.setCalendarPopup(True)
        self.dateEdit_ExpectedDate.setCalendarPopup(True)
        self.dateEdit_OrderDate.setDisplayFormat("MM/dd/yyyy")
        self.dateEdit_ShipDate.setDisplayFormat("MM/dd/yyyy")
        self.dateEdit_ExpectedDate.setDisplayFormat("MM/dd/yyyy")
        self.lineEdit_CreatedDate.setReadOnly(True)
        self.lineEdit_CreatedDate.setStyleSheet("background-color: #f0f0f0;")


        self.lineEdit_CreatedBy.setReadOnly(True)
        self.lineEdit_Status.setReadOnly(True)
        self.lineEdit_CreatedBy.setStyleSheet("background-color: #f0f0f0;")
        self.lineEdit_Status.setStyleSheet("background-color: #f0f0f0;")

        if not self.receipt_data:
            self.dateEdit_OrderDate.setDate(QtCore.QDate.currentDate())

        self.load_dropdowns()

        if self.receipt_data:
            self.populate_fields()
        else:
            self.original_data = self.collect_form_data()

    def init_receipt_lines_tab_if_ready(self):
        if not self.receipt_data:
            self.tabWidget.setTabEnabled(self.tabWidget.count() - 1, False)
            return

        receipt_number = self.receipt_data.get("receipt_number")
        if receipt_number:
            self.receipt_lines_tab = ReceiptLinesWindow(receipt_number=receipt_number, api_client=self.api_client)
            self.tabWidget.addTab(self.receipt_lines_tab, "Receipt Lines")
        else:
            self.tabWidget.setTabEnabled(self.tabWidget.count() - 1, False)


    def load_dropdowns(self):
        try:
            label_forms_response = self.api_client.get(f"/label_forms")
            if label_forms_response.status_code == 200:
                label_forms = label_forms_response.json()
                self.comboBox_Label_Form.clear()
                for lf in label_forms:
                    self.comboBox_Label_Form.addItem(lf["label_form"])

            document_forms_response = self.api_client.get(f"/document_forms")
            if document_forms_response.status_code == 200:
                document_forms = document_forms_response.json()
                self.comboBox_Doc_Form.clear()
                for df in document_forms:
                    self.comboBox_Doc_Form.addItem(df["document_form"])

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo cargar datos.")

    def populate_fields(self):
        data = self.receipt_data

        self.lineEdit_order_number.setText(data.get("receipt_number", ""))
        self.lineEdit_customer_name.setText(data.get("release_num", ""))
        self.lineEdit_Vendor_Name.setText(data.get("vendor_name", ""))
        self.lineEdit_Vendor_num.setText(str(data.get("vendor_id", "")))
        self.comboBox_Label_Form.setCurrentText(data.get("label_form", ""))
        self.comboBox_Doc_Form.setCurrentText(data.get("document_form", ""))
        self.lineEdit_PO.setText(str(data.get("po_id", "")))
        self.lineEdit_InvoiceNumber.setText(data.get("invoice_num", ""))
        self.lineEdit_Status.setText(data.get("status", ""))
        self.lineEdit_CreatedBy.setText(str(data.get("created_by", "")))
        created_date_str = data.get("created_date", "")
        if created_date_str:
            try:
                created_date = QtCore.QDate.fromString(created_date_str[:10], QtCore.Qt.ISODate)
                formatted_date = created_date.toString("MM/dd/yy")
                self.lineEdit_CreatedDate.setText(formatted_date)
            except Exception:
                self.lineEdit_CreatedDate.setText("Invalid date")
        else:
            self.lineEdit_CreatedDate.setText("")
        self.lineEdit_Carrier.setText(data.get("carrier", ""))
        self.lineEdit_Ship_method.setText(data.get("seal_num", ""))

        self.dateEdit_OrderDate.setDate(self.safe_parse_date(data.get("receipt_date")))
        self.dateEdit_ExpectedDate.setDate(self.safe_parse_date(data.get("date_expected")))
        self.dateEdit_ShipDate.setDate(self.safe_parse_date(data.get("date_shipped")))

        self.checkBox.setChecked(data.get("close_receipt", False))

    def safe_parse_date(self, date_str):
        if date_str:
            try:
                return QtCore.QDate.fromString(date_str[:10], QtCore.Qt.ISODate)
            except Exception:
                return QtCore.QDate.currentDate()
        return QtCore.QDate.currentDate()

    def collect_form_data(self):
        def get(field):
            widget = getattr(self, f"lineEdit_{field}", None)
            return widget.text().strip() if widget else ""

        def get_combo(field): return getattr(self, f"comboBox_{field}", None).currentText().strip()
        def get_date(widget): return widget.date().toString("yyyy-MM-dd")

        data = {
            "receipt_number": get("order_number"),
            "release_num": get("customer_name"),
            "vendor_name": get("Vendor_Name"),
            "vendor_id": int(get("Vendor_num")) if get("Vendor_num").isdigit() else None,
            "label_form": get_combo("Label_Form"),
            "document_form": get_combo("Doc_Form"),
            "po_id": int(get("PO")) if get("PO").isdigit() else None,
            "invoice_num": get("InvoiceNumber"),
            "status": get("Status"),
            "created_by": int(get("CreatedBy")) if get("CreatedBy").isdigit() else None,
            "created_date": self.original_data.get("created_date"),
            "carrier": get("Carrier"),
            "seal_num": get("Ship_method"),
            "receipt_date": get_date(self.dateEdit_OrderDate),
            "date_expected": get_date(self.dateEdit_ExpectedDate),
            "date_shipped": get_date(self.dateEdit_ShipDate),
            "close_receipt": self.checkBox.isChecked()
        }
        return {k: v for k, v in data.items() if v not in [None, ""]}

    def get_updated_fields(self):
        updated = {}
        current_data = self.collect_form_data()

        for key, current_value in current_data.items():
            original_value = self.original_data.get(key, "")

            # ✅ Normalizar fechas a yyyy-MM-dd si contienen T
            if "date" in key.lower():
                if isinstance(original_value, str) and "T" in original_value:
                    original_value = original_value.split("T")[0]
                if isinstance(current_value, str) and "T" in current_value:
                    current_value = current_value.split("T")[0]
                if isinstance(current_value, str) and "/" in current_value:
                    try:
                        current_value = datetime.strptime(current_value, "%m/%d/%y").strftime("%Y-%m-%d")
                    except Exception:
                        pass

            if str(current_value).strip() != str(original_value).strip():
                print(f"🔁 Diferencia detectada: {key} | original: {original_value} | actual: {current_value}")
                updated[key] = current_value

        return updated



    def has_unsaved_changes(self):
        return bool(self.get_updated_fields())

    def save_receipt(self):
        if self.receipt_data and "id" in self.receipt_data:
            updated_data = self.get_updated_fields()
            if not updated_data:
                return
            response = self.api_client.put(f"/receipts/{self.receipt_data['id']}", json=updated_data)
        else:
            full_data = self.collect_form_data()
            response = self.api_client.post(f"/receipts", json=full_data)

        if response.status_code in (200, 201):
            self.original_data = self.collect_form_data()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to save receipt: {response.text}")

    def save_all(self):
        receipt_saved = self.save_receipt()
        lines_saved = False

        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if isinstance(tab, ReceiptLinesWindow):
                lines_saved = tab.save_changes()
                break

        if receipt_saved and lines_saved:
            QtWidgets.QMessageBox.information(self, "Success", "Receipt and lines saved successfully.")
        elif receipt_saved:
            QtWidgets.QMessageBox.information(self, "Success", "Receipt saved successfully.")
        elif lines_saved:
            QtWidgets.QMessageBox.information(self, "Success", "Receipt lines saved successfully.")
        else:
            QtWidgets.QMessageBox.information(self, "Success", "No Changes Detected")


    def get_receipt_number(self):
        if self.receipt_data and "receipt_number" in self.receipt_data:
            return self.receipt_data["receipt_number"]
        return self.lineEdit_order_number.text().strip()

    def closeEvent(self, event):
        if self.has_unsaved_changes():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you really want to close?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
