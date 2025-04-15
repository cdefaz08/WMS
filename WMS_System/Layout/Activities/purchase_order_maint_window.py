from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import QDate
from Layout.UI_PY.purchase_order_maint_ui import PurchaseOrderMaintUI

class PurchaseOrderMaintWindow(PurchaseOrderMaintUI):
    def __init__(self, api_client=None, po_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.po_data = po_data
        if self.po_data:
            po_id = self.po_data.get("id")
            try:
                lines_response = self.api_client.get(f"/purchase-order-lines/by-po/{po_id}")
                if lines_response.status_code == 200:
                    self.po_data["po_lines"] = lines_response.json()
                else:
                    self.po_data["po_lines"] = []
            except Exception as e:
                self.po_data["po_lines"] = []
                
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

        po_lines = self.po_data.get("po_lines", [])
        self.original_lines = po_lines.copy()
        self.receipt_table.setRowCount(len(po_lines))
        for row_idx, line in enumerate(po_lines):
            column_keys = ["line_number", 
                        "upc", "item_code", "description", "qty_ordered", 
                        "qty_expected", "qty_received", "uom", "unit_price", 
                        "total_price", "id"]
            
            for col_idx, key in enumerate(column_keys):
                cell_value = str(line.get(key, ""))
                item = QtWidgets.QTableWidgetItem(cell_value)

                # En la columna 2 (item_code), guarda el item_id como UserRole
                if key == "item_code":
                    item.setData(QtCore.Qt.UserRole, line.get("item_id", None))  # Guarda el ID real

                if key == "line_number":
                    item.setData(QtCore.Qt.UserRole + 1, line.get("id"))  # guarda el line_id aquí
                
                self.receipt_table.setItem(row_idx, col_idx, item)
                
                
            

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
        po_updated = False
        po_created = False

        # 1. Recolectar todos los datos del PO (tanto para update como create)
        payload = {
            "po_number": self.input_po_number.text().strip(),
            "vendor_id": self.input_vendor.currentData(), 
            "expected_date": self.input_expected_date.date().toString("yyyy-MM-dd"),
            "ship_date": self.input_ship_date.date().toString("yyyy-MM-dd"),
            "order_date": self.input_order_date.date().toString("yyyy-MM-dd"),
            "status": self.input_status.currentText(),
            "created_by": self.input_created_by.text().strip(),
        }

        # Campos custom
        for idx, field in enumerate(self.custom_fields, start=1):
            payload[f"custom_{idx}"] = field.text().strip()

        # Dirección de envío y facturación
        for tab_index, prefix in [(0, "ship_"), (1, "bill_")]:
            form_layout = self.tabs.widget(0).layout().itemAt(tab_index).widget().layout()
            for i in range(form_layout.rowCount()):
                label = form_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget().text()
                field_widget = form_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()

                if "City" in label:
                    container = field_widget.layout()
                    for sub_key, widget in zip(["city", "state", "zip_code"], [container.itemAt(j).widget() for j in range(3)]):
                        payload[f"{prefix}{sub_key}"] = widget.text().strip()
                else:
                    key = f"{prefix}{label.lower().replace(' ', '_').replace(':', '')}"
                    payload[key] = field_widget.text().strip()

        # 2. Decidir si creamos o actualizamos
        if self.po_data and self.po_data.get("id"):
            po_id = self.po_data["id"]
            response = self.api_client.put(f"/purchase-orders/{po_id}", json=payload)
            if response.status_code == 200:
                po_updated = True
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update PO: {response.text}")
                return
        else:
            if not payload["vendor_id"]:
                QtWidgets.QMessageBox.critical(self, "Missing Vendor", "Please select a vendor before saving.")
                return

            response = self.api_client.post("/purchase-orders/", json=payload)
            if response.status_code in (200, 201):
                self.po_data = response.json()
                po_created = True
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create PO: {response.text}")
                return

        # 3. Guardar líneas (necesitamos el ID)
        lines_updated = self.save_order_lines()

        # 4. Mostrar resultado
        if po_created and lines_updated:
            QMessageBox.information(self, "Success", "Purchase Order created with lines.")
        elif po_updated and lines_updated:
            QMessageBox.information(self, "Success", "Purchase Order and Lines updated.")
        elif po_created:
            QMessageBox.information(self, "Success", "Purchase Order created.")
        elif po_updated:
            QMessageBox.information(self, "Success", "Purchase Order updated.")
        elif lines_updated:
            QMessageBox.information(self, "Success", "Purchase Order Lines updated.")
        else:
            QMessageBox.information(self, "No Changes", "No changes detected.")



    def save_order_lines(self):
        if not self.po_data:
            return False

        url = "/purchase-order-lines/"
        current_data = self.get_order_lines_data()
        changes_made = False

        for i, row_data in enumerate(current_data):
            if not row_data.get("item_id") or not row_data.get("qty_ordered"):
                continue

            payload = row_data.copy()
            payload["purchase_order_id"] = self.po_data["id"]

            try:
                payload["item_id"] = int(payload["item_id"])
                payload["qty_ordered"] = int(payload["qty_ordered"])
                payload["qty_expected"] = int(payload["qty_expected"])
                payload["qty_received"] = int(payload["qty_received"])
                payload["unit_price"] = float(payload["unit_price"])
                payload["line_total"] = float(payload["total_price"])
            except Exception as e:
                continue

            payload.setdefault("lot_number", "")
            payload.setdefault("expiration_date", QDate.currentDate().toString("yyyy-MM-dd"))
            payload.setdefault("location_received", "")
            payload.setdefault("comments", "")
            payload.setdefault("custom_1", "")
            payload.setdefault("custom_2", "")
            payload.setdefault("custom_3", "")

            payload.pop("po_number", None)
            payload.pop("total_price", None)

            response = self.api_client.post(url, json=payload)

            if response.status_code not in (200, 201):
                QtWidgets.QMessageBox.warning(self, "Line Save Error", f"Failed to save line {i + 1}:\n{response.text}")
            else:
                changes_made = True

        return changes_made



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
            "line_number": row + 1, "upc": "", "item_id": "",
            "description": "", "quantity_ordered": 0, "quantity_expected": 0, "quantity_received": 0,
            "uom": "Pieces", "unit_price": 0.0, "total_price": 0.0
        }
        values = data or default

        for col, key in enumerate([
            "line_number", "upc", "item_id", "description", "quantity_ordered",
            "quantity_expected", "quantity_received", "uom", "unit_price", "total_price"
        ]):
            if key == "uom":
                combo = QtWidgets.QComboBox()
                combo.addItems(["Pallets", "Carton", "Pieces"])
                
                # Set default value from `values`
                current_uom = values.get("uom", "Pieces")
                index = combo.findText(current_uom)
                if index != -1:
                    combo.setCurrentIndex(index)

                self.receipt_table.setCellWidget(row, col, combo)
                continue  # Skip setting QTableWidgetItem for this column

            item = QtWidgets.QTableWidgetItem(str(values.get(key, "")))
            editable_keys = ["upc", "quantity_received", "quantity_ordered"]
            flags = item.flags()
            item.setFlags(flags | QtCore.Qt.ItemIsEditable if key in editable_keys else flags & ~QtCore.Qt.ItemIsEditable)
            self.receipt_table.setItem(row, col, item)
            if key == "item_id":
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

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

        # Mostrar item_code (ej: "Phone Iphone") en la columna 2, guardar ID como 
        item_code = QtWidgets.QTableWidgetItem(product.get("item_id", ""))
        item_code.setFlags(item_code.flags() & ~QtCore.Qt.ItemIsEditable)
        item_code.setData(QtCore.Qt.UserRole, product["id"])  # ID interno
        self.receipt_table.setItem(row, 2, item_code)


        # Mostrar descripción en la columna 3
        self.receipt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(product.get("description", "")))

        # Precio en la columna 8
        self.receipt_table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(product.get("price", 0.0))))

        self.update_orderline_total_price(row)


    def update_qty_ordered_based_on_uom(self, row):
        combo = self.receipt_table.cellWidget(row, 7)
        uom = combo.currentText() if combo else "Pieces"
        config = combo.property("item_config") or {}

        pieces_per_carton = config.get("pieces_per_carton", 1)
        cartons_per_pallet = config.get("cartons_per_pallet", 1)

        qty = 1  # Default fallback

        if uom == "Pieces":
            qty = 1
        elif uom == "Carton":
            qty = pieces_per_carton
        elif uom == "Pallets":
            qty = cartons_per_pallet * pieces_per_carton

        self.receipt_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(qty)))  # qty_ordered está en columna 4



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
            item_code_item = self.receipt_table.item(row, 2)
            item_id = item_code_item.data(QtCore.Qt.UserRole) if item_code_item else None

            row_data = {
                "po_number": self.input_po_number.text().strip(),
                "line_number": self.get_cell_text(row, 0),
                "upc": self.get_cell_text(row, 1),
                "item_id": item_id,
                "item_code": item_code_item.text() if item_code_item else "",
                "description": self.get_cell_text(row, 3),
                "qty_ordered": self.get_cell_text(row, 4),
                "qty_expected": self.get_cell_text(row, 5),
                "qty_received": self.get_cell_text(row, 6),
                "uom": (
                    self.receipt_table.cellWidget(row, 7).currentText()
                    if self.receipt_table.cellWidget(row, 7)
                    else self.get_cell_text(row, 7)
                ),
                "unit_price": self.get_cell_text(row, 8),
                "total_price": self.get_cell_text(row, 9),
            }
            data.append(row_data)
        return data


    def get_cell_text(self, row, column):
        item = self.receipt_table.item(row, column)
        return item.text().strip() if item else ""


    def delete_selected_order_line(self):
        selected = self.receipt_table.currentRow()
        if selected < 0:
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this line?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        # Obtener el ID si existe
        item = self.receipt_table.item(selected, 0)
        line_id = item.data(QtCore.Qt.UserRole + 1)

        # Eliminar del backend si tiene ID
        if line_id:
            try:
                response = self.api_client.delete(f"/purchase-order-lines/{line_id}")
                if response.status_code not in (200, 204):
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete line from server:\n{response.text}")
                    return
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Exception occurred: {e}")
                return

        # Quitar la fila de la tabla si todo está bien
        self.receipt_table.removeRow(selected)
        QtWidgets.QMessageBox.information(self, "Deleted", "Line deleted successfully.")
