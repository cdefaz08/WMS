from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtCore import QDate
from Layout.UI_PY.purchase_order_maint_ui import PurchaseOrderMaintUI
from functools import partial

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
            column_keys = [
                "line_number", "upc", "item_code", "description", "qty_ordered", 
                "qty_expected", "qty_received", "uom", "unit_price", "line_total", "id"
            ]

            for col_idx, key in enumerate(column_keys):
                # UOM será un QComboBox
                if key == "uom":
                    combo = QtWidgets.QComboBox()
                    combo.addItems(["Pallets", "Carton", "Pieces"])
                    index = combo.findText(line.get("uom", "Pieces"))
                    if index >= 0:
                        combo.setCurrentIndex(index)

                    # 👉 Obtener configuración del item
                    item_id = line.get("item_id")
                    config = {}
                    try:
                        if item_id:
                            response = self.api_client.get(f"/item-config/item-maintance/default/{item_id}")
                            if response.status_code == 200:
                                config = response.json()
                    except Exception as e:
                        print(f"⚠️ Error fetching config: {e}")

                    combo.setProperty("item_config", config)

                    # 👉 Guardar total_pieces desde qty_ordered + uom
                    try:
                        ordered = float(line.get("qty_ordered", 0))
                    except:
                        ordered = 0.0

                    pieces = ordered
                    if config:
                        per_case = config.get("pieces_per_case", 1)
                        per_pallet = config.get("boxes_per_pallet", 1)

                        if line.get("uom") == "Carton":
                            pieces = ordered * per_case
                        elif line.get("uom") == "Pallets":
                            pieces = ordered * per_case * per_pallet

                    combo.setProperty("total_pieces", pieces)

                    # 👉 Conectar para recalcular al cambiar
                    combo.currentIndexChanged.connect(partial(self.update_qty_ordered_based_on_uom, row_idx))
                    self.receipt_table.setCellWidget(row_idx, col_idx, combo)
                    continue

                # Todas las otras columnas
                cell_value = str(line.get(key, ""))
                item = QtWidgets.QTableWidgetItem(cell_value)

                if key == "item_code":
                    item.setData(QtCore.Qt.UserRole, line.get("item_id", None))
                if key == "line_number":
                    item.setData(QtCore.Qt.UserRole + 1, line.get("id"))

                self.receipt_table.setItem(row_idx, col_idx, item)

            # 👉 Al final de la fila, actualizar cantidad según el UOM cargado
        self.connect_signals_once()

            #self.update_qty_ordered_based_on_uom(row_idx)   

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

        # 1. Recolectar valores actuales del formulario
        current_values = {
            "po_number": self.input_po_number.text().strip(),
            "vendor_id": self.input_vendor.currentData(),
            "expected_date": self.input_expected_date.date().toString("yyyy-MM-dd"),
            "ship_date": self.input_ship_date.date().toString("yyyy-MM-dd"),
            "order_date": self.input_order_date.date().toString("yyyy-MM-dd"),
            "status": self.input_status.currentText(),
            "created_by": self.input_created_by.text().strip(),
        }

        for idx, field in enumerate(self.custom_fields, start=1):
            current_values[f"custom_{idx}"] = field.text().strip()

        for tab_index, prefix in [(0, "ship_"), (1, "bill_")]:
            form_layout = self.tabs.widget(0).layout().itemAt(tab_index).widget().layout()
            for i in range(form_layout.rowCount()):
                label = form_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget().text()
                field_widget = form_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()

                if "City" in label:
                    container = field_widget.layout()
                    for sub_key, widget in zip(["city", "state", "zip_code"], [container.itemAt(j).widget() for j in range(3)]):
                        current_values[f"{prefix}{sub_key}"] = widget.text().strip()
                else:
                    key = f"{prefix}{label.lower().replace(' ', '_').replace(':', '')}"
                    current_values[key] = field_widget.text().strip()

        # 2. Si es UPDATE, detectar cambios reales
        updated_fields = {}

        if self.po_data and self.po_data.get("id"):
            for key, new_val in current_values.items():
                old_val = str(self.po_data.get(key, "") or "").strip()
                if str(new_val).strip() != old_val:
                    updated_fields[key] = new_val

            if updated_fields:
                po_id = self.po_data["id"]
                response = self.api_client.put(f"/purchase-orders/{po_id}", json=updated_fields)
                if response.status_code == 200:
                    po_updated = True
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update PO: {response.text}")
                    return
        else:
            # Es una nueva PO
            if not current_values["vendor_id"]:
                QtWidgets.QMessageBox.critical(self, "Missing Vendor", "Please select a vendor before saving.")
                return

            response = self.api_client.post("/purchase-orders/", json=current_values)
            if response.status_code in (200, 201):
                self.po_data = response.json()
                po_created = True
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create PO: {response.text}")
                return

        # 3. Guardar líneas
        lines_updated = self.save_order_lines()

        # 4. Resultado final
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

            if not self.is_line_modified(row_data, i):
                continue  # ✅ Línea sin cambios

            if i >= len(self.original_lines):
                original = {}  # Es una nueva línea, sin original
            else:
                original = self.original_lines[i]
            payload = {}

            for key, new_val in row_data.items():
                if key in ["line_id", "po_number"]:
                    continue

                old_val = original.get(key)

                # Comparación segura numérica o textual
                try:
                    if float(new_val) == float(old_val):
                        continue
                except:
                    if str(new_val).strip() == str(old_val).strip():
                        continue

                # Si cambió, lo incluimos
                payload[key] = new_val

            # Obligatorio siempre
            payload["purchase_order_id"] = self.po_data["id"]

            # 🔄 Conversión de tipos solo si está presente
            try:
                if "item_id" in payload:
                    payload["item_id"] = int(payload["item_id"])
                if "qty_ordered" in payload:
                    payload["qty_ordered"] = int(float(payload["qty_ordered"]))
                if "qty_expected" in payload:
                    payload["qty_expected"] = int(payload["qty_expected"])
                if "qty_received" in payload:
                    payload["qty_received"] = int(payload["qty_received"])
                if "unit_price" in payload:
                    payload["unit_price"] = float(payload["unit_price"])
                if "line_total" in payload:
                    payload["line_total"] = float(payload["line_total"])
                if "total_pieces" in payload:
                    payload["total_pieces"] = float(payload["total_pieces"])
            except Exception as e:
                print(f"❌ Error converting data for line {i + 1}: {e}")
                continue


            line_id = row_data.get("line_id")
            if line_id:
                print(f"📝 Updating line ID {line_id} → payload: {payload}")
                response = self.api_client.put(f"/purchase-order-lines/{line_id}", json=payload)
            else:
                print(f"➕ Creating new line → payload: {payload}")
                response = self.api_client.post(url, json=payload)

            if response.status_code not in (200, 201):
                QtWidgets.QMessageBox.warning(
                    self,
                    "Line Save Error",
                    f"Failed to save line {i + 1}:\n{response.text}"
                )
            else:
                changes_made = True

        return changes_made



    def is_line_modified(self, new_row, index):
        try:
            original = self.original_lines[index]
        except IndexError:
            return True  # Nueva fila (no hay original para comparar)

        EXCLUDE_KEYS = {"po_number", "total_price", "line_id"}

        for key in new_row:
            if key in EXCLUDE_KEYS:
                continue

            new_val = new_row.get(key, "")
            old_val = original.get(key, "")

            try:
                if float(new_val) == float(old_val):
                    continue
            except:
                if str(new_val).strip() == str(old_val).strip():
                    continue

            print(f"🟠 Cambio detectado en '{key}': {new_val} ≠ {old_val}")
            return True

        return False


    def add_order_line_row(self, data=None):
        row = self.receipt_table.rowCount()
        self.receipt_table.blockSignals(True)  # ⛔️ Pausar señales
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

        self.receipt_table.blockSignals(False)  # ✅ Volver a permitir señales
    
    def connect_signals_once(self):
        try:
            self.receipt_table.itemChanged.disconnect()
        except TypeError:
            pass  # no estaba conectado

        self.receipt_table.itemChanged.connect(self.handle_orderline_item_change)

    def handle_orderline_item_change(self, item):
        if not item:
            return

        row = item.row()
        col = item.column()
        key = self.receipt_table.horizontalHeaderItem(col).text().lower().replace(" ", "_")

        if key == "ordered":
            combo = self.receipt_table.cellWidget(row, 7)
            if combo:
                try:
                    qty = float(item.text())
                except:
                    qty = 0.0

                uom = combo.currentText()
                config = combo.property("item_config") or {}
                print("Config:", config)
                pieces_per_case = config.get("pieces_per_case", 1)
                boxes_per_pallet = config.get("boxes_per_pallet", 1)

                # 🔁 Convertir a total_pieces según UOM actual
                if uom == "Pieces":
                    qty = round(qty)  # 🔒 redondeamos cantidad visual escrita por el usuario
                    total_pieces = qty
                elif uom == "Carton":
                    total_pieces = qty * pieces_per_case
                elif uom == "Pallets":
                    # ❗ NO redondees si se permite media tarima
                    total_pieces = qty * pieces_per_case * boxes_per_pallet
                else:
                    total_pieces = qty

                combo.setProperty("total_pieces", total_pieces)
                print(f"[✏️] line change: row={row}, UOM={uom}, total_pieces={total_pieces}")
                self.update_orderline_total_price(row)

        elif key == "upc":
            self.receipt_table.blockSignals(True)
            self.handle_upc_change(item, row)
            self.receipt_table.blockSignals(False)

        


    def handle_upc_change(self, item, row):
        upc_value = item.text().strip()

        if not upc_value:
            return  # ⚠️ Si está vacío, no hacer nada

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
        item_id = product["id"]

        # 👉 Obtener configuración por defecto del item
        config_response = self.api_client.get(f"/item-config/item-maintance/default/{item_id}")
        if config_response.status_code != 200:
            QtWidgets.QMessageBox.warning(self, "Warning", "No default configuration found for this item.")
            config = {}
        else:
            config = config_response.json()

        # Mostrar item_code en columna 2
        item_code = QtWidgets.QTableWidgetItem(product.get("item_id", ""))
        item_code.setFlags(item_code.flags() & ~QtCore.Qt.ItemIsEditable)
        item_code.setData(QtCore.Qt.UserRole, item_id)  # Guarda el item_id
        self.receipt_table.setItem(row, 2, item_code)

        # Descripción en columna 3
        self.receipt_table.setItem(row, 3, QtWidgets.QTableWidgetItem(product.get("description", "")))

        # Precio en columna 8
        self.receipt_table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(product.get("price", 0.0))))

        # UOM como dropdown en columna 7
        combo = QtWidgets.QComboBox()
        combo.addItems(["Pallets", "Carton", "Pieces"])
        combo.setProperty("item_config", config)  # 🔁 Guarda config
        print(combo.property("item_config"))
        combo.currentIndexChanged.connect(lambda _, r=row: self.update_qty_ordered_based_on_uom(r))
        self.receipt_table.setCellWidget(row, 7, combo)

        # Calcular y actualizar qty_ordered (columna 4)
        self.update_qty_ordered_based_on_uom(row)

        # Calcular total
        self.update_orderline_total_price(row)

    def update_qty_ordered_based_on_uom(self, row):
        combo = self.receipt_table.cellWidget(row, 7)
        if not combo:
            return

        uom = combo.currentText()
        config = combo.property("item_config") or {}

        pieces_per_case = config.get("pieces_per_case", 1)
        boxes_per_pallet = config.get("boxes_per_pallet", 1)

        # ✅ Solo leer el total_pieces, no recalcularlo
        total_pieces = combo.property("total_pieces")
        if total_pieces is None:
            try:
                total_pieces = float(self.receipt_table.item(row, 4).text())
            except:
                total_pieces = 0.0
            combo.setProperty("total_pieces", total_pieces)

        # 🔁 Convertir a la unidad actual solo para mostrar
        if uom == "Pieces":
            new_qty = total_pieces / 1
            new_qty = round(new_qty)  # 🔒 enteros
        elif uom == "Carton" and pieces_per_case:
            new_qty = total_pieces / pieces_per_case
            new_qty = new_qty  # 🔒 enteros
        elif uom == "Pallets" and pieces_per_case and boxes_per_pallet:
            new_qty = total_pieces / (pieces_per_case * boxes_per_pallet)
            # ✅ pallets pueden tener decimales, no se redondea
        else:
            new_qty = total_pieces

        # Mostrar visualmente la cantidad convertida
        ordered_item = self.receipt_table.item(row, 4)
        if ordered_item:
            ordered_item.setText(f"{new_qty:.2f}")





    def update_orderline_total_price(self, row):
        try:
            combo = self.receipt_table.cellWidget(row, 7)  # UOM ComboBox
            price_item = self.receipt_table.item(row, 8)

            if not combo or not price_item:
                raise ValueError("Missing cells")

            unit_price = float(price_item.text())
            total_pieces = combo.property("total_pieces")

            if total_pieces is None:
                raise ValueError("Missing total_pieces")

            total = total_pieces * unit_price
            print(f"[💰] Calculating total for row {row}: {total_pieces} * {unit_price} = {total:.2f}")

            self.receipt_table.setItem(row, 9, QtWidgets.QTableWidgetItem(f"{total:.2f}"))

        except (ValueError, TypeError, AttributeError) as e:
            print(f"⚠️ Error calculating total at row {row}: {e}")
            self.receipt_table.setItem(row, 9, QtWidgets.QTableWidgetItem("0.00"))


    def get_order_lines_data(self):
        data = []
        for row in range(self.receipt_table.rowCount()):
            line_id_item = self.receipt_table.item(row, 0)
            line_id = line_id_item.data(QtCore.Qt.UserRole + 1) if line_id_item else None
            item_code_item = self.receipt_table.item(row, 2)
            item_id = item_code_item.data(QtCore.Qt.UserRole) if item_code_item else None
            combo = self.receipt_table.cellWidget(row, 7)
            total_pieces = combo.property("total_pieces") if combo else 0

            row_data = {
                "line_id": line_id,
                "purchase_order_id": self.po_data["id"],
                "line_number": self.get_cell_text(row, 0),
                "upc": self.get_cell_text(row, 1),
                "item_id": item_id,
                "item_code": item_code_item.text() if item_code_item else "",
                "description": self.get_cell_text(row, 3),
                "qty_ordered": self.get_cell_text(row, 4),
                "qty_expected": self.get_cell_text(row, 5),
                "qty_received": self.get_cell_text(row, 6),
                "uom": combo.currentText() if combo else self.get_cell_text(row, 7),
                "unit_price": self.get_cell_text(row, 8),
                "line_total": self.get_cell_text(row, 9),
                "total_pieces": total_pieces,

                # Opcionales:
                "lot_number": "",
                "expiration_date": QDate.currentDate().toString("yyyy-MM-dd"),
                "location_received": "",
                "comments": "",
                "custom_1": "",
                "custom_2": "",
                "custom_3": "",
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
