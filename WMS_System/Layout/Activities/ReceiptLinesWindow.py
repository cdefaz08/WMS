from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_ReceiptLines import Ui_Form

class ReceiptLinesWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, receipt_number=None, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.receipt_number = receipt_number
        self.original_data = []

        self.headers = [
            "id", "line_number", "upc", "item_code", "description",
            "quantity_ordered", "quantity_expected", "quantity_received",
            "uom", "unit_price", "total_price", "lot_number",
            "expiration_date", "location_received", "comments",
            "custom_1", "custom_2", "custom_3"
        ]

        self.tableWidget_OrderLines.setColumnCount(len(self.headers))
        self.tableWidget_OrderLines.setHorizontalHeaderLabels([h.upper().replace("_", " ") for h in self.headers])
        self.tableWidget_OrderLines.setColumnHidden(0, True)
        self.tableWidget_OrderLines.verticalHeader().setVisible(False)
        self.tableWidget_OrderLines.horizontalHeader().setStretchLastSection(True)

        self.tableWidget_OrderLines.itemChanged.connect(self.handle_item_change)
        self.load_data()

    def load_data(self):
        url = f"/receipt-lines/receipt/{self.receipt_number}"
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.original_data = response.json()
            self.tableWidget_OrderLines.blockSignals(True)
            self.tableWidget_OrderLines.setRowCount(0)
            for row_data in self.original_data:
                self.add_row(row_data)
            self.tableWidget_OrderLines.blockSignals(False)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to load receipt lines.")

    def add_row(self, data=None):
        row = self.tableWidget_OrderLines.rowCount()
        self.tableWidget_OrderLines.insertRow(row)

        default = {
            "id": "", "line_number": row + 1, "upc": "", "item_code": "",
            "description": "", "quantity_ordered": 0, "quantity_expected": 0, "quantity_received": 0,
            "uom": "Pieces", "unit_price": 0.0, "total_price": 0.0,
            "lot_number": "", "expiration_date": QtCore.QDate.currentDate().toString("yyyy-MM-dd"),
            "location_received": "", "comments": "",
            "custom_1": "", "custom_2": "", "custom_3": ""
        }

        values = data or default

        for col, key in enumerate(self.headers):
            value = values.get(key, "")
            item = QtWidgets.QTableWidgetItem(str(value))

            if key in ["upc", "quantity_ordered", "quantity_expected", "quantity_received",
                    "uom", "comments", "lot_number", "expiration_date", 
                    "location_received", "custom_1", "custom_2", "custom_3"]:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            else:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

            self.tableWidget_OrderLines.setItem(row, col, item)

    def add_new_blank_row(self):
        self.add_row()

    def handle_item_change(self, item):
        if not item or not item.text().strip():
            return

        row = item.row()
        col = item.column()
        key = self.headers[col]

        if key == "item_code":
            QtWidgets.QMessageBox.warning(self, "Not Allowed", "You can't manually edit the item code.")
            self.tableWidget_OrderLines.blockSignals(True)
            # Restaurar el valor original si existe
            original_value = self.original_data[row].get("item_code", "") if row < len(self.original_data) else ""
            self.tableWidget_OrderLines.item(row, item.column()).setText(str(original_value))

            self.tableWidget_OrderLines.blockSignals(False)
            return


        if key == "upc":
            self.handle_upc_change(item, row)
        elif key == "quantity_received":
            self.update_total_price(row)

    def handle_upc_change(self, item, row):
        upc_value = item.text().strip()

        if not upc_value.isdigit():
            QtWidgets.QMessageBox.warning(self, "UPC Error", "UPC must be numeric.")
            return

        response = self.api_client.get(f"/items?upc={upc_value}")
        if response.status_code != 200:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            return

        items = response.json()
        if not items:
            QtWidgets.QMessageBox.warning(self, "UPC Not Found", f"No item found with UPC {upc_value}")
            return

        product = items[0]
        item_code = product["item_id"]
        unit_price = product["price"]
        description = product.get("description", "")

        self.tableWidget_OrderLines.blockSignals(True)

        # Asignar valores protegidos
        item_code_item = QtWidgets.QTableWidgetItem(str(item_code))
        item_code_item.setFlags(item_code_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.tableWidget_OrderLines.setItem(row, self.headers.index("item_code"), item_code_item)

        price_item = QtWidgets.QTableWidgetItem(str(unit_price))
        price_item.setFlags(price_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.tableWidget_OrderLines.setItem(row, self.headers.index("unit_price"), price_item)

        # También asignar descripción
        desc_item = QtWidgets.QTableWidgetItem(description)
        desc_item.setFlags(desc_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.tableWidget_OrderLines.setItem(row, self.headers.index("description"), desc_item)

        self.update_total_price(row, unit_price)

        self.tableWidget_OrderLines.blockSignals(False)


    def update_total_price(self, row, unit_price=None):
        quantity_item = self.tableWidget_OrderLines.item(row, self.headers.index("quantity_received"))
        price_item = self.tableWidget_OrderLines.item(row, self.headers.index("unit_price"))

        try:
            quantity = int(quantity_item.text()) if quantity_item else 0
            unit_price = unit_price if unit_price is not None else float(price_item.text()) if price_item else 0.0
            total = quantity * unit_price
        except ValueError:
            total = 0.0

        self.tableWidget_OrderLines.setItem(row, self.headers.index("total_price"), QtWidgets.QTableWidgetItem(f"{total:.2f}"))

    def get_current_data(self):
        data = []
        for row in range(self.tableWidget_OrderLines.rowCount()):
            row_data = {}
            for col, key in enumerate(self.headers):
                item = self.tableWidget_OrderLines.item(row, col)
                row_data[key] = item.text().strip() if item else ""
            row_data["receipt_number"] = self.receipt_number
            data.append(row_data)
        return data

    def is_row_modified(self, new_row, row_index):
        try:
            original = self.original_data[row_index]
        except IndexError:
            return True

        for key in self.headers:
            if key == "id":
                continue

            new_value = str(new_row.get(key, "")).strip()
            original_value = str(original.get(key, "")).strip()

            try:
                if float(new_value) == float(original_value):
                    continue
            except ValueError:
                if new_value == original_value:
                    continue

            return True

        return False

    def save_changes(self):
        url = "/receipt-lines/"
        current_data = self.get_current_data()

        for i, row_data in enumerate(current_data):
            if not row_data.get("item_code") or not row_data.get("quantity_received"):
                continue

            is_new = not row_data.get("id")
            is_modified = is_new or self.is_row_modified(row_data, i)

            if not is_modified:
                continue

            payload = row_data.copy()
            line_id = payload.pop("id", None)

            print("Payload:", payload)

            if line_id:
                response = self.api_client.put(f"{url}{line_id}", json=payload)
            else:
                response = self.api_client.post(url, json=payload)

            if response.status_code in (200, 201):
                QtWidgets.QMessageBox.information(self, "Success", "Receipt saved successfully.")
                self.original_data = self.get_current_data()
                return True
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to save receipt: {response.text}")
                return False

        self.load_data()
        self.original_data = self.get_current_data()

    def delete_selected_row(self):
        selected = self.tableWidget_OrderLines.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "Delete Error", "No row selected to delete.")
            return

        id_item = self.tableWidget_OrderLines.item(selected, 0)
        line_id = id_item.text() if id_item else None

        if line_id:
            confirm = QtWidgets.QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete this line?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                response = self.api_client.delete(f"/receipt-lines/{line_id}")
                if response.status_code not in (200, 204):
                    QtWidgets.QMessageBox.warning(self, "Delete Error", f"Failed to delete: {response.text}")

        self.tableWidget_OrderLines.removeRow(selected)
