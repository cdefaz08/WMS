from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets , QtCore
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
            vendor_response = self.api_client.get("/vendors/")
            if vendor_response.status_code == 200:
                self.vendors = vendor_response.json()
                self.input_vendor.clear()
                for vendor in self.vendors:
                    self.input_vendor.addItem(vendor["vendor_code"], vendor["id"])
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

        for idx, field in enumerate(self.custom_fields, start=1):
            field.setText(self.po_data.get(f"custom_{idx}", ""))

        self._set_address_group(self.tabs.widget(0).layout().itemAt(0).widget(), "ship_")
        self._set_address_group(self.tabs.widget(0).layout().itemAt(1).widget(), "bill_")

        receipt_lines = self.po_data.get("receipt_lines", [])
        self.original_lines = receipt_lines.copy()
        self.receipt_table.setRowCount(len(receipt_lines))
        for row_idx, line in enumerate(receipt_lines):
            for col_idx, key in enumerate(["line_number", "upc", "item_code", "description", "quantity_ordered",
                                           "quantity_expected", "quantity_received", "uom", "unit_price", "total_price"]):
                item = QtWidgets.QTableWidgetItem(str(line.get(key, "")))
                self.receipt_table.setItem(row_idx, col_idx, item)
            self.receipt_table.setItem(row_idx, 11, QtWidgets.QTableWidgetItem(str(line.get("id", ""))))

    def _set_address_group(self, groupbox, prefix):
        form_layout = groupbox.layout()
        for i in range(form_layout.rowCount()):
            label = form_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget().text()
            field_widget = form_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()

            if "City" in label:
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
        if not self.po_data:
            return

        self.save_order_lines()
        updated_fields = {}
        current_values = {
            "expected_date": self.input_expected_date.date().toString("yyyy-MM-dd"),
            "ship_date": self.input_ship_date.date().toString("yyyy-MM-dd"),
            "status": self.input_status.currentText(),
        }

        for key, new_value in current_values.items():
            old_value = str(self.po_data.get(key, "") or "")
            if new_value != old_value:
                updated_fields[key] = new_value

        for idx, field in enumerate(self.custom_fields, start=1):
            key = f"custom_{idx}"
            current = field.text().strip()
            previous = str(self.po_data.get(key, "") or "")
            if current != previous:
                updated_fields[key] = current

        for tab_index, prefix in [(0, "ship_"), (1, "bill_")]:
            form_layout = self.tabs.widget(0).layout().itemAt(tab_index).widget().layout()
            for i in range(form_layout.rowCount()):
                label = form_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget().text()
                field_widget = form_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()
                key = f"{prefix}{label.lower().replace(' ', '_').replace(':', '')}"

                if "city" in label.lower():
                    container = field_widget.layout()
                    for sub_key, widget in zip(["city", "state", "zip_code"], [container.itemAt(j).widget() for j in range(3)]):
                        full_key = f"{prefix}{sub_key}"
                        current_value = widget.text().strip()
                        if current_value != str(self.po_data.get(full_key, "") or ""):
                            updated_fields[full_key] = current_value
                else:
                    current = field_widget.text().strip()
                    if current != str(self.po_data.get(key, "") or ""):
                        updated_fields[key] = current

        if not updated_fields:
            QMessageBox.information(self, "No Changes", "No changes detected.")
            return

        po_id = self.po_data.get("id")
        response = self.api_client.put(f"/purchase-orders/{po_id}", json=updated_fields)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Purchase Order updated successfully.")
        else:
            QMessageBox.critical(self, "Error", f"Failed to update PO: {response.text}")

    def save_order_lines(self):
        if not self.po_data:
            return

        url = "/purchase-order-lines/"
        current_data = self.get_order_lines_data()

        for i, row_data in enumerate(current_data):
            if not row_data.get("item_id") or not row_data.get("quantity_received"):
                continue

            line_id = row_data.get("id")
            is_new = not line_id
            is_modified = is_new or self.is_line_modified(row_data, i)

            if not is_modified:
                continue

            payload = row_data.copy()
            payload["purchase_order_id"] = self.po_data["id"]

            try:
                payload["item_id"] = int(payload["item_id"])
                payload["quantity_ordered"] = int(payload["quantity_ordered"])
                payload["quantity_expected"] = int(payload["quantity_expected"])
                payload["quantity_received"] = int(payload["quantity_received"])
                payload["unit_price"] = float(payload["unit_price"])
                payload["line_total"] = float(payload["total_price"])
            except Exception:
                continue

            payload.pop("po_number", None)
            payload.pop("total_price", None)

            if is_new:
                response = self.api_client.post(url, json=payload)
            else:
                response = self.api_client.put(f"{url}{line_id}", json=payload)

            if response.status_code not in (200, 201):
                QtWidgets.QMessageBox.warning(self, "Line Save Error", f"Failed to save line: {response.text}")

    def is_line_modified(self, new_row, index):
        try:
            original = self.original_lines[index]
        except IndexError:
            return True

        for key in new_row:
            if key in ["po_number", "total_price"]:
                continue
            new_val = str(new_row.get(key, "")).strip()
            old_val = str(original.get(key, "")).strip()
            try:
                if float(new_val) == float(old_val):
                    continue
            except ValueError:
                if new_val == old_val:
                    continue
            return True

        return False

    def add_order_line_row(self, data=None):
        row = self.receipt_table.rowCount()
        self.receipt_table.insertRow(row)

        default = {
            "line_number": row + 1, "upc": "", "item_code": "",
            "description": "", "quantity_ordered": 0, "quantity_expected": 0, "quantity_received": 0,
            "uom": "Pieces", "unit_price": 0.0, "total_price": 0.0
        }
        values = data or default

        for col, key in enumerate([
            "line_number", "upc", "item_code", "description", "quantity_ordered",
            "quantity_expected", "quantity_received", "uom", "unit_price", "total_price"
        ]):
            item = QtWidgets.QTableWidgetItem(str(values.get(key, "")))
            editable_keys = ["upc", "quantity_received", "quantity_ordered"]
            flags = item.flags()
            item.setFlags(flags | QtCore.Qt.ItemIsEditable if key in editable_keys else flags & ~QtCore.Qt.ItemIsEditable)
            self.receipt_table.setItem(row, col, item)

        self.receipt_table.itemChanged.connect(self.handle_orderline_item_change)

    def handle_orderline_item_change(self, item):
        if not item:
            return

        row = item.row()
        col = item.column()
        key = self.receipt_table.horizontalHeaderItem(col).text().lower().replace(" ", "_")

        if key == "upc":
            self.receipt_table.blockSignals(True)
            self.handle_upc_change(item, row)
            self.receipt_table.blockSignals(False)
        elif key == "quantity_received":
            self.update_orderline_total_price(row)

    def handle_upc_change(self, item, row):
        upc_value = item.text().strip()
        if not upc_value.isdigit():
            QtWidgets.QMessageBox.warning(self, "UPC Error", "UPC must be numeric.")
            return

        response = self.api_client.get(f"/items?upc={upc_value}")
        if response.status_code != 200:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to server.")
            return

        items = response.json()
        if not items:
            QtWidgets.QMessageBox.warning(self, "UPC Not Found", f"No item found with UPC {upc_value}")
            return

        product = items[0]
        self.receipt_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(product["item_id"])))
        self.receipt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(product.get("description", "")))
        self.receipt_table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(product.get("price", 0.0))))
        self.receipt_table.setItem(row, 11, QtWidgets.QTableWidgetItem(str(product.get("id", ""))))
        self.update_orderline_total_price(row)

    def update_orderline_total_price(self, row):
        try:
            quantity = int(self.receipt_table.item(row, 6).text())
            unit_price = float(self.receipt_table.item(row, 8).text())
            total = quantity * unit_price
            self.receipt_table.setItem(row, 9, QtWidgets.QTableWidgetItem(f"{total:.2f}"))
        except (ValueError, TypeError):
            self.receipt_table.setItem(row, 9, QtWidgets.QTableWidgetItem("0.00"))

    def get_order_lines_data(self):
        data = []
        for row in range(self.receipt_table.rowCount()):
            row_data = {
                "po_number": self.input_po_number.text().strip(),
                "line_number": self.receipt_table.item(row, 0).text(),
                "upc": self.receipt_table.item(row, 1).text(),
                "item_id": self.receipt_table.item(row, 2).text(),
                "description": self.receipt_table.item(row, 3).text(),
                "quantity_ordered": self.receipt_table.item(row, 4).text(),
                "quantity_expected": self.receipt_table.item(row, 5).text(),
                "quantity_received": self.receipt_table.item(row, 6).text(),
                "uom": self.receipt_table.item(row, 7).text(),
                "unit_price": self.receipt_table.item(row, 8).text(),
                "total_price": self.receipt_table.item(row, 9).text(),
            }
            data.append(row_data)
        return data

    def delete_selected_order_line(self):
        selected = self.receipt_table.currentRow()
        if selected >= 0:
            self.receipt_table.removeRow(selected)