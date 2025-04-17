from Layout.UI_PY.retail_sale_ui import RetailSaleUI  # Ajusta la ruta si es distinta
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox,QCheckBox
from PyQt5.QtCore import Qt

class RetailSaleWindow(RetailSaleUI):
    def __init__(self, api_client=None, user=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user = user or "Demo User"

        # Llenar datos por defecto
        self.input_user.setText(self.user)
        self.input_sale_number.setText("AUTO-GENERATED")
        self.input_date.setText("Today")

        self.input_upc_scanner.returnPressed.connect(self.handle_upc_scan)
        self.input_received.textChanged.connect(self.calculate_change_due)
        self.btn_remove_item.clicked.connect(self.remove_selected_row)
        self.btn_confirm.clicked.connect(self.confirm_sale)
        self.btn_cancel.clicked.connect(self.clear_form)
        self.table.itemChanged.connect(self.handle_item_change)


        # Aquí podrás conectar señales, manejar lógica, etc. más adelante

    def handle_upc_scan(self):
        upc = self.input_upc_scanner.text().strip()
        if not upc:
            return

        # Buscar si ya está en la tabla
        for row in range(self.table.rowCount()):
            existing_upc = self.table.item(row, 0)
            if existing_upc and existing_upc.text() == upc:
                # Incrementar cantidad
                qty_item = self.table.item(row, 3)
                if qty_item:
                    new_qty = int(qty_item.text()) + 1
                    qty_item.setText(str(new_qty))
                    self.update_line_total(row)
                    self.update_totals()
                    self.input_upc_scanner.clear()
                    return

        # No existe, buscar en API
        try:
            response = self.api_client.get(f"/items/upc/{upc}")
            if response.status_code == 200:
                item = response.json()
                self.add_item_to_table(item, upc)
            else:
                QMessageBox.warning(self, "Not Found", "Item not found for UPC.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error looking up item: {e}")

        self.input_upc_scanner.clear()




    def add_item_to_table(self, item, upc):
        self.table.blockSignals(True)
        row = self.table.rowCount()
        self.table.insertRow(row)

        upc_item = make_read_only_item(upc)
        upc_item.setData(Qt.UserRole, item["id"])
        upc_item.setData(Qt.UserRole + 1, item.get("is_taxable", True)) 
        self.table.setItem(row, 0, upc_item)

        # Code y Description
        self.table.setItem(row, 1, make_read_only_item(item.get("item_id", "")))
        self.table.setItem(row, 2, make_read_only_item(item.get("description", "")))

        # Qty, Price, Discount (editables)
        self.table.setItem(row, 3, QTableWidgetItem("1"))
        self.table.setItem(row, 4, QTableWidgetItem(str(item.get("price", 0))))
        self.table.setItem(row, 5, QTableWidgetItem("0"))
        self.table.setItem(row, 6, QTableWidgetItem("0.00"))  # Line Total

        self.update_line_total(row)
        self.update_totals()
        self.calculate_change_due()
        self.table.blockSignals(False) 

    def update_line_total(self, row):
        try:
            qty = float(self.table.item(row, 3).text())
            price = float(self.table.item(row, 4).text())
            discount = float(self.table.item(row, 5).text())
            total = (qty * price) - discount
            self.table.setItem(row, 6, QTableWidgetItem(f"{total:.2f}"))
        except:
            self.table.setItem(row, 6, QTableWidgetItem("0.00"))

    def update_totals(self):
        TAX_RATE = 0.06625
        taxable_total = 0.0
        subtotal = 0.0
        discount_total = 0.0

        for row in range(self.table.rowCount()):
            try:
                qty = float(self.table.item(row, 3).text())
                price = float(self.table.item(row, 4).text())
                discount = float(self.table.item(row, 5).text())

                line_subtotal = qty * price
                subtotal += line_subtotal
                discount_total += discount

                upc_item = self.table.item(row, 0)
                is_taxable = True
                if upc_item:
                    is_taxable = upc_item.data(Qt.UserRole + 1)

                if is_taxable:
                    taxable_total += (line_subtotal - discount)

            except:
                continue

        tax = taxable_total * TAX_RATE
        total = (subtotal - discount_total) + tax

        self.input_subtotal.setText(f"{subtotal:.2f}")
        self.input_discount_total.setText(f"{discount_total:.2f}")
        self.input_tax.setText(f"{tax:.2f}")
        self.input_total.setText(f"{total:.2f}")


    def calculate_change_due(self):
        try:
            received = float(self.input_received.text())
            total = float(self.input_total.text())
            change = received - total
            self.input_change.setText(f"{change:.2f}" if change >= 0 else "0.00")
        except:
            self.input_change.setText("0.00")

    def remove_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.table.removeRow(selected_row)
            self.update_totals()
            self.calculate_change_due()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a row to remove.")

    def confirm_sale(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "No items", "Please add at least one item to proceed.")
            return

        try:
            lines = []
            for row in range(self.table.rowCount()):
                item_id = None
                item_code = self.table.item(row, 1).text()

                # Buscamos el ID (guardado previamente como property en la celda UPC)
                upc_cell = self.table.item(row, 0)
                if upc_cell:
                    item_id = upc_cell.data(Qt.UserRole) 
                description = self.table.item(row, 2).text()
                qty = float(self.table.item(row, 3).text())
                price = float(self.table.item(row, 4).text())
                discount = float(self.table.item(row, 5).text())
                line_total = float(self.table.item(row, 6).text())

                lines.append({
                    "item_id": item_id,
                    "description": description,
                    "quantity": qty,
                    "unit_price": price,
                    "discount": discount,
                    "line_total": line_total,
                    "item_code": item_code  # ✅ reemplaza esto por un ID real si lo tienes
                })

            payload = {
                "customer_name": self.input_customer_name.text(),
                "customer_contact": self.input_contact.text(),
                "payment_method": self.combo_payment.currentText(),
                "subtotal": float(self.input_subtotal.text()),
                "tax": float(self.input_tax.text()),
                "discount_total": float(self.input_discount_total.text()),
                "total": float(self.input_total.text()),
                "amount_received": float(self.input_received.text() or 0),
                "change_due": float(self.input_change.text() or 0),
                "created_by": self.input_user.text(),
                "lines": lines
            }

            response = self.api_client.post("/sales/", json=payload)

            if response.status_code == 200:
                sale_data = response.json()
                sale_number = sale_data.get("sale_number", "N/A")
                QMessageBox.information(
                    self,
                    "Success",
                    f"Sale #{sale_number} registered successfully."
                )

                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", f"Could not register sale: {response.text}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")

    def handle_item_change(self, item):
        print("Cell changed:", item.row(), item.column())  # 👈 DEBUG
        row = item.row()
        col = item.column()

        # Solo recalcular si el cambio fue en las columnas relevantes
        if col in [3, 4, 5]:  # Qty, Price, Discount
            self.update_line_total(row)
            self.update_totals()
            self.calculate_change_due()

    def clear_form(self):
        self.input_customer_name.clear()
        self.input_contact.clear()
        self.combo_payment.setCurrentIndex(0)
        self.input_received.clear()
        self.input_change.setText("0.00")
        self.input_sale_number.setText("AUTO-GENERATED")

        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.table.blockSignals(False)

        self.input_subtotal.setText("0.00")
        self.input_discount_total.setText("0.00")
        self.input_tax.setText("0.00")
        self.input_total.setText("0.00")

def make_read_only_item(text):
    item = QTableWidgetItem(text)
    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    return item