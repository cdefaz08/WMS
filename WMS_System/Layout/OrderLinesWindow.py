from PyQt5 import QtWidgets, QtCore, uic
from Layout.UI_PY.UI_OrderLines import Ui_Form

class OrderLinesWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, order_number=None, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.order_number = order_number
        self.original_data = []

        self.headers = ["id", "upc", "item_code", "quantity", "unit_price", "line_total", "comments"]
        self.tableWidget_OrderLines.setColumnCount(len(self.headers))
        self.tableWidget_OrderLines.setHorizontalHeaderLabels([h.upper().replace("_", " ") for h in self.headers])
        self.tableWidget_OrderLines.verticalHeader().setVisible(False)
        self.tableWidget_OrderLines.horizontalHeader().setStretchLastSection(True)

        self.tableWidget_OrderLines.itemChanged.connect(self.handle_item_change)
        self.load_data()

    def load_data(self):
        url = f"/order-lines/by-order/{self.order_number}"
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.original_data = response.json()
            self.tableWidget_OrderLines.setRowCount(0)
            for row_data in self.original_data:
                self.add_row(row_data)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to load order lines.")

    def add_row(self, data=None):
        row = self.tableWidget_OrderLines.rowCount()
        self.tableWidget_OrderLines.insertRow(row)

        default = {
            "id": "",
            "upc": "",
            "item_code": "",
            "quantity": 0,
            "unit_price": 0.0,
            "line_total": 0.0,
            "comments": ""
        }

        values = data or default

        for col, key in enumerate(self.headers):
            value = values.get(key, "")
            item = QtWidgets.QTableWidgetItem(str(value))

            if key in ["upc", "quantity", "comments"]:
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

        if key == "upc":
            self.handle_upc_change(item, row)
        elif key == "quantity":
            self.update_line_total(row)

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

        self.tableWidget_OrderLines.blockSignals(True)

        self.tableWidget_OrderLines.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item_code)))

        price_item = QtWidgets.QTableWidgetItem(str(unit_price))
        price_item.setFlags(price_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.tableWidget_OrderLines.setItem(row, 4, price_item)

        self.update_line_total(row, unit_price)

        self.tableWidget_OrderLines.blockSignals(False)

    def is_row_modified(self, new_row, row_index):
        try:
            original = self.original_data[row_index]
        except IndexError:
            return True  # New row that didn’t exist before

        for key in self.headers:
            if key == "id":
                continue  # Skip id in comparison
            new_value = str(new_row.get(key, "")).strip()
            original_value = str(original.get(key, "")).strip()
            if new_value != original_value:
                return True
        return False

    def update_line_total(self, row, unit_price=None):
        quantity_item = self.tableWidget_OrderLines.item(row, 3)
        price_item = self.tableWidget_OrderLines.item(row, 4)

        try:
            quantity = int(quantity_item.text()) if quantity_item else 0
            unit_price = unit_price if unit_price is not None else float(price_item.text()) if price_item else 0.0
            total = quantity * unit_price
        except ValueError:
            total = 0.0

        self.tableWidget_OrderLines.setItem(row, 5, QtWidgets.QTableWidgetItem(f"{total:.2f}"))

    def get_current_data(self):
        data = []
        for row in range(self.tableWidget_OrderLines.rowCount()):
            row_data = {}
            for col, key in enumerate(self.headers):
                item = self.tableWidget_OrderLines.item(row, col)
                row_data[key] = item.text().strip() if item else ""

            row_data["order_number"] = self.order_number
            data.append(row_data)
        return data

    def save_changes(self):
        url = "/order-lines/"
        current_data = self.get_current_data()

        for i, row_data in enumerate(current_data):
            if not row_data.get("item_code") or not row_data.get("quantity"):
                continue

            is_new = not row_data.get("id")
            is_modified = is_new or self.is_row_modified(row_data, i)

            if not is_modified:
                continue  # Skip unchanged rows

            payload = row_data.copy()
            line_id = payload.pop("id", None)

            print(payload)

            if line_id:
                response = self.api_client.put(f"{url}{line_id}", json=payload)
            else:
                response = self.api_client.post(url, json=payload)

            if response.status_code not in (200, 201):
                QtWidgets.QMessageBox.warning(self, "Save Error", f"Failed to save line: {response.text}")

        self.load_data()
        self.original_data = self.get_current_data()


    def delete_selected_row(self):
        selected = self.tableWidget_OrderLines.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "Delete Error", "No row selected to delete.")
            return

        id_item = self.tableWidget_OrderLines.item(selected, 0)  # 'id' está en la columna 0
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
                response = self.api_client.delete(f"/order-lines/{line_id}")
                if response.status_code not in (200, 204):
                    QtWidgets.QMessageBox.warning(self, "Delete Error", f"Failed to delete: {response.text}")

        self.tableWidget_OrderLines.removeRow(selected)
