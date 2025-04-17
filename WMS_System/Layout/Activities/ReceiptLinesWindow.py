from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_ReceiptLines import Ui_Form
from functools import partial
from Utils.reusable_utils import fetch_item_by_upc, calculate_total_pieces,get_default_item_config


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
            raw_data = response.json()
            self.tableWidget_OrderLines.blockSignals(True)
            self.tableWidget_OrderLines.setRowCount(0)

            for row_data in raw_data:
                self.add_row(row_data)

            self.tableWidget_OrderLines.blockSignals(False)

            # ✅ Reconstruir original_data desde la tabla ya poblada
            self.original_data = self.get_current_data()
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
        print(f"🧩 Adding row → ID: {values.get('id')}")
        for col, key in enumerate(self.headers):
            value = values.get(key, "")
            item = QtWidgets.QTableWidgetItem(str(value))

            if key == "id":
                item.setData(QtCore.Qt.UserRole, value)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.tableWidget_OrderLines.setItem(row, col, item)
                continue
                        

            if key == "uom":
                combo = QtWidgets.QComboBox()
                combo.addItems(["Pallets", "Carton", "Pieces"])

                # Set UOM actual
                index = combo.findText(values.get("uom", "Pieces"))
                if index >= 0:
                    combo.setCurrentIndex(index)
                print(f"Setting UOM to {values.get('uom')}")

                # Obtener configuración del ítem
                item_id = values.get("item_id", "")
                config = get_default_item_config(self.api_client, item_id) if item_id else {}
                combo.setProperty("item_config", config)
                print(f"Config for item_id {item_id}: {config}")

                # Calcular total_pieces desde qty y UOM
                try:
                    qty = float(values.get("quantity_ordered", 0))
                except:
                    qty = 0.0

                total_pieces = calculate_total_pieces(qty, combo.currentText(), config)
                combo.setProperty("total_pieces", total_pieces)

                combo.currentIndexChanged.connect(partial(self.update_qty_ordered_based_on_uom, row))
                self.tableWidget_OrderLines.setCellWidget(row, col, combo)
                continue

            if key == "item_code":
                 item.setData(QtCore.Qt.UserRole, values.get("item_id"))  

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
        elif key == "quantity_ordered":
            combo = self.tableWidget_OrderLines.cellWidget(row, self.headers.index("uom"))
            if combo:
                try:
                    qty = float(item.text())
                except:
                    qty = 0.0

                uom = combo.currentText()
                config = combo.property("item_config") or {}


                total_pieces = calculate_total_pieces(qty, uom, config)
                combo.setProperty("total_pieces", total_pieces)

                print(f"[✏️] Changed row={row}, UOM={uom}, total_pieces={total_pieces}")
                print(f"config={config}")
            
            self.update_total_price(row)

    def handle_upc_change(self, item, row):
        upc_value = item.text().strip()

        if not upc_value:
            return

        product, config = fetch_item_by_upc(self.api_client, upc_value)

        if not product:
            QtWidgets.QMessageBox.warning(self, "UPC Not Found", f"No item found with UPC {upc_value}")
            return

        item_code = product.get("item_id", "")
        item_id = product.get("id", "")
        unit_price = product.get("price", 0.0)
        description = product.get("description", "")

        self.tableWidget_OrderLines.blockSignals(True)

        item_code_item = self._non_editable_item(item_code)
        item_code_item.setData(QtCore.Qt.UserRole, item_id)
        self.tableWidget_OrderLines.setItem(row, self.headers.index("item_code"), item_code_item)

        self.tableWidget_OrderLines.setItem(row, self.headers.index("description"), self._non_editable_item(description))
        self.tableWidget_OrderLines.setItem(row, self.headers.index("unit_price"), self._non_editable_item(str(unit_price)))

        # 🧠 Configurar el combo de UOM si existe
        combo = self.tableWidget_OrderLines.cellWidget(row, self.headers.index("uom"))
        if combo:
            combo.setProperty("item_config", config)
            ordered_item = self.tableWidget_OrderLines.item(row, self.headers.index("quantity_ordered"))
            try:
                qty = float(ordered_item.text())
            except:
                qty = 0.0

            total_pieces = calculate_total_pieces(qty, "Pieces", config)
            combo.setProperty("total_pieces", total_pieces)
            print(f"Total pieces set to {total_pieces} for row {row}")

        # Actualizar cantidad ordenada
        self.update_qty_ordered_based_on_uom(row)
        self.update_total_price(row)

        pieces = calculate_total_pieces(qty, combo.currentText(), config)
        combo.setProperty("total_pieces", pieces)
        self.tableWidget_OrderLines.blockSignals(False)

    def _non_editable_item(self, value):
        item = QtWidgets.QTableWidgetItem(str(value))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        return item

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
                combo = self.tableWidget_OrderLines.cellWidget(row, col)
                item = self.tableWidget_OrderLines.item(row, col)

                # 🆔 Get line ID from hidden column
                if key == "id":
                    row_data["id"] = item.data(QtCore.Qt.UserRole) if item else None
                    continue

                # 📦 Get UOM from combo box
                if key == "uom":
                    if combo and isinstance(combo, QtWidgets.QComboBox):
                        row_data[key] = combo.currentText()
                    else:
                        row_data[key] = ""
                    continue

                # 🔁 Default case: read QTableWidgetItem text
                row_data[key] = item.text().strip() if item else ""

                # 📌 Get item_id from UserRole if on item_code column
                if key == "item_code":
                    item_id = item.data(QtCore.Qt.UserRole) if item else None
                    row_data["item_id"] = item_id

            # 📋 Set receipt_number for each line
            row_data["receipt_number"] = self.receipt_number
            data.append(row_data)

            print(f"✅ Row {row} → Captured ID in get_current_data: ID: {row_data.get('id')}, UOM: {row_data.get('uom')}")

        return data


    def is_row_modified(self, new_row, row_index):
        if row_index >= len(self.original_data):
            print(f"🆕 Nueva fila (index {row_index}) ➜ marcada como modificada.")
            return True

        original = self.original_data[row_index]

        for key in self.headers:
            if key == "id":
                continue

            new_value = str(new_row.get(key, "")).strip()
            original_value = str(original.get(key, "")).strip()

            if key == "uom":
                print(f"[DEBUG] UOM -> new: '{new_value}' | original: '{original_value}'")

            # Si ambos vacíos, no hacer nada
            if new_value.casefold() != original_value.casefold():
                print(f"📝 Cambio detectado en '{key}': '{original_value}' → '{new_value}'")
                return True

            # Comparar numéricamente si es posible
            try:
                if float(new_value) != float(original_value):
                    print(f"🔢 Cambio detectado en '{key}': '{original_value}' → '{new_value}'")
                    return True
                else:
                    continue
            except ValueError:
                # Si no son números, comparar como texto
                if new_value != original_value:
                    print(f"📝 Cambio detectado en '{key}': '{original_value}' → '{new_value}'")
                    return True

        return False  # ✅ No se detectaron diferencias


    def save_changes(self):
        url = "/receipt-lines/"
        current_data = self.get_current_data()
        print(f"current data:{current_data} ")

        for i, row_data in enumerate(current_data):
            if not row_data.get("item_code") or not row_data.get("quantity_received"):
                continue

            is_new = not row_data.get("id")
            is_modified = is_new or self.is_row_modified(row_data, i)

            if not is_modified:
                continue

            # Don't pop, just read the id separately
            payload = row_data.copy()
            line_id = row_data.get("id")  # Use this to decide between POST and PUT

            print(f"📝 Sending payload to API → row={i}, is_new={is_new}, id={line_id}")
            print("Payload:", payload)

            if line_id:
                response = self.api_client.put(f"{url}{line_id}", json=payload)
            else:
                response = self.api_client.post(url, json=payload)

            if response.status_code in (200, 201):
                return True
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"❌ Failed to save line {i+1}: {response.text}")
                return False

        self.load_data()

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


    def update_qty_ordered_based_on_uom(self, row):
        combo = self.tableWidget_OrderLines.cellWidget(row, self.headers.index("uom"))
        if not combo:
            return

        uom = combo.currentText()
        config = combo.property("item_config") or {}

        pieces_per_case = config.get("pieces_per_case", 1)
        boxes_per_pallet = config.get("boxes_per_pallet", 1)

        # 👇 Leer cantidad actual en pantalla (quantity_ordered) si total_pieces no está seteado
        total_pieces = combo.property("total_pieces")
        if total_pieces is None or total_pieces == 0:
            try:
                ordered_item = self.tableWidget_OrderLines.item(row, self.headers.index("quantity_ordered"))
                qty = float(ordered_item.text())
            except:
                qty = 0.0

            total_pieces = calculate_total_pieces(qty, uom, config)
            combo.setProperty("total_pieces", total_pieces)

        # 🔁 Convertir total_pieces a la unidad actual
        if uom == "Pieces":
            qty_converted = round(total_pieces)
        elif uom == "Carton" and pieces_per_case:
            qty_converted = total_pieces / pieces_per_case
        elif uom == "Pallets" and pieces_per_case and boxes_per_pallet:
            qty_converted = total_pieces / (pieces_per_case * boxes_per_pallet)
        else:
            qty_converted = total_pieces

        # Actualizar cantidad ordenada en la tabla
        self.tableWidget_OrderLines.setItem(
            row,
            self.headers.index("quantity_ordered"),
            QtWidgets.QTableWidgetItem(f"{qty_converted:.2f}")
        )

