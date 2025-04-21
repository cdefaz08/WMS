from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from Layout.UI_PY.UI_RuleMaintance import Ui_RuleWindow


class RuleMaintance(Ui_RuleWindow):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.original_data_by_table = {}
        self.load_all_tables()

    def get_endpoint(self, table):
        if table == self.putaway_table:
            return "/rules/putaway/"
        elif table == self.restock_table:
            return "/rules/restock/"
        elif table == self.pick_table:
            return "/rules/pick/"

    def load_all_tables(self):
        self.load_table_data(self.putaway_table)
        self.load_table_data(self.restock_table)
        self.load_table_data(self.pick_table)

    def load_table_data(self, table):
        endpoint = self.get_endpoint(table)
        try:
            response = self.api_client.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                self.original_data_by_table[table] = data
                self.populate_table(table, data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rules:\n{str(e)}")

    def populate_table(self, table, data):
        table.setRowCount(0)
        for row_idx, item in enumerate(data):
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, QTableWidgetItem(item["rule_name"]))
            table.setItem(row_idx, 1, QTableWidgetItem(item["description"]))
            table.item(row_idx, 0).setData(1000, item["id"])

    def get_selected_id(self, table):
        selected = table.selectedItems()
        if selected:
            return selected[0].data(1000)
        return None

    def delete_selected_row(self, table):
        row = table.currentRow()
        if row < 0:
            return

        rule_id = self.get_selected_id(table)
        if not rule_id:
            return

        confirm = QMessageBox.question(self, "Delete", f"Delete rule ID {rule_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            endpoint = self.get_endpoint(table)
            try:
                response = self.api_client.delete(f"{endpoint}{rule_id}")
                if response.status_code == 200:
                    table.removeRow(row)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete rule:\n{str(e)}")

    def add_empty_row(self, table):
        row_idx = table.rowCount()
        table.insertRow(row_idx)
        table.setItem(row_idx, 0, QTableWidgetItem(""))  # Rule Name
        table.setItem(row_idx, 1, QTableWidgetItem(""))  # Description



    def save_changes(self, table):
        endpoint = self.get_endpoint(table)
        row_count = table.rowCount()
        original_data = self.original_data_by_table.get(table, [])

        changes_made = False
        for row in range(row_count):
            name_item = table.item(row, 0)
            desc_item = table.item(row, 1)
            rule_id = name_item.data(1000) if name_item else None

            name = name_item.text().strip() if name_item else ""
            desc = desc_item.text().strip() if desc_item else ""

            if not name:
                continue

            payload = {
                "rule_name": name,
                "description": desc
            }

            try:
                if rule_id:
                    # Buscar datos originales
                    original = next((r for r in original_data if r["id"] == rule_id), None)
                    if original:
                        # Comparar y solo actualizar si cambió
                        if (
                            payload["rule_name"] == original["rule_name"]
                            and payload["description"] == original["description"]
                        ):
                            continue  # ❌ No hay cambios

                    # PUT solo si hay cambios
                    response = self.api_client.put(f"{endpoint}{rule_id}", json=payload)
                    changes_made = True

                else:
                    # Crear nuevo si no tiene ID
                    response = self.api_client.post(endpoint, json=payload)
                    if response.status_code == 200:
                        returned = response.json()
                        name_item.setData(1000, returned["id"])
                        changes_made = True

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save rule:\n{str(e)}")

        # ✅ Mensajes finales
        if changes_made:
    # 🔁 Refrescar los datos originales desde la tabla
            updated_data = []
            for row in range(row_count):
                name_item = table.item(row, 0)
                desc_item = table.item(row, 1)
                rule_id = name_item.data(1000) if name_item else None

                if not name_item or not rule_id:
                    continue

                updated_data.append({
                    "id": rule_id,
                    "rule_name": name_item.text().strip(),
                    "description": desc_item.text().strip() if desc_item else ""
                })

            # ✅ Guardar como nuevos datos originales
            self.original_data_by_table[table] = updated_data
            QMessageBox.information(self, "Success", "Changes saved successfully.")
        else:
            QMessageBox.information(self, "No Changes", "No changes detected to save.")


    def get_selected_rule_info(self):
        current_index = self.tab_widget.currentIndex()

        if current_index == 0:  # Putaway
            selected = self.get_selected_id(self.putaway_table)
            return selected, "putaway"
        elif current_index == 1:  # Restock
            selected = self.get_selected_id(self.restock_table)
            return selected, "restock"
        elif current_index == 2:  # Pick
            selected = self.get_selected_id(self.pick_table)
            return selected, "pick"
        return None, None