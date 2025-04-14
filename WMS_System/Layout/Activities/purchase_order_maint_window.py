from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from Layout.UI_PY.purchase_order_maint_ui import PurchaseOrderMaintUI

class PurchaseOrderMaintWindow(PurchaseOrderMaintUI):
    def __init__(self, api_client=None, po_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.po_data = po_data

        self.load_dropdowns()
        self.populate_data()

    def load_dropdowns(self):
        try:
            # Load vendors
            vendor_response = self.api_client.get("/vendors/")
            if vendor_response.status_code == 200:
                self.vendors = vendor_response.json()
                self.input_vendor.clear()
                for vendor in self.vendors:
                    self.input_vendor.addItem(vendor["vendor_code"], vendor["id"])

            # Load label/report/order types if applicable
            # You can expand this similarly with calls to /label-forms/, /order-types/, etc.
            self.input_label_form.addItems(["Wal70", "Zebra"])
            self.input_report_form.addItems(["Wal70", "Default"])
            self.input_order_type.addItems(["Sams", "Costco", "Retail"])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load dropdowns: {e}")

    def populate_data(self):
        if not self.po_data:
            return

        self.input_po_number.setText(self.po_data.get("po_number", ""))
        self.input_order_date.setDate(QDate.fromString(self.po_data.get("order_date", ""), "yyyy-MM-dd"))
        self.input_expected_date.setDate(QDate.fromString(self.po_data.get("expected_date", ""), "yyyy-MM-dd"))
        self.input_ship_date.setDate(QDate.fromString(self.po_data.get("ship_date", ""), "yyyy-MM-dd"))
        self.input_status.setCurrentText(self.po_data.get("status", "Open"))
        self.input_created_by.setText(self.po_data.get("created_by", ""))

        # Custom fields
        for idx, field in enumerate(self.custom_fields, start=1):
            field.setText(self.po_data.get(f"custom_{idx}", ""))

        # Dirección de envío (Ship From)
        ship_prefix = "ship_"
        self._set_address_group(self.tabs.widget(0).layout().itemAt(0).widget(), ship_prefix)

        # Dirección de facturación (Bill To)
        bill_prefix = "bill_"
        self._set_address_group(self.tabs.widget(0).layout().itemAt(1).widget(), bill_prefix)

        # Receipt Lines
        receipt_lines = self.po_data.get("receipt_lines", [])
        self.receipt_table.setRowCount(len(receipt_lines))
        for row_idx, line in enumerate(receipt_lines):
            for col_idx, key in enumerate(["line_number", "upc", "item_code", "description", "quantity_ordered",
                                        "quantity_expected", "quantity_received", "uom", "unit_price", "total_price"]):
                item = QtWidgets.QTableWidgetItem(str(line.get(key, "")))
                self.receipt_table.setItem(row_idx, col_idx, item)

    def _set_address_group(self, groupbox, prefix):
        form_layout = groupbox.layout()
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget().text()
            field_widget = form_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()

            if "City" in label:
                city = QtWidgets.QLineEdit()
                state = QtWidgets.QLineEdit()
                zip_code = QtWidgets.QLineEdit()

                container = field_widget.layout()
                city_widget = container.itemAt(0).widget()
                state_widget = container.itemAt(1).widget()
                zip_widget = container.itemAt(2).widget()

                city_widget.setText(self.po_data.get(f"{prefix}city", ""))
                state_widget.setText(self.po_data.get(f"{prefix}state", ""))
                zip_widget.setText(self.po_data.get(f"{prefix}zip_code", ""))

            else:
                field_widget.setText(self.po_data.get(f"{prefix}{label.lower().replace(' ', '_').replace(':', '')}", ""))



    def save_changes(self):
        QMessageBox.information(self, "Save", "Saving logic goes here.")
