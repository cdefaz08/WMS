from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5 import QtCore
from Layout.UI_PY.UI_GroupMaintance import GroupMaintanceUI


class GroupMaintanceWindow(GroupMaintanceUI):
    def __init__(self, api_client=None, parent = None):
        super().__init__()
        self.api_client = api_client
        self.load_all_groups()

    def load_all_groups(self):
        self.load_group_data("Groups/putaway-groups", self.putaway_tab)
        self.load_group_data("Groups/restock-groups", self.restock_tab)
        self.load_group_data("Groups/pick-groups", self.pick_tab)

    def load_group_data(self, endpoint, tab):
        try:
            response = self.api_client.get(f"/{endpoint}/")
            if response.status_code == 200:
                data = response.json()
                tab.original_data = data
                table = tab.table
                table.setRowCount(0)
                table.setColumnWidth(0, 180)
                table.setColumnWidth(1, 300)
                table.verticalHeader().setVisible(False)

                for row in data:
                    row_idx = table.rowCount()
                    table.insertRow(row_idx)

                    item_name = QTableWidgetItem(row.get("group_name", ""))
                    item_desc = QTableWidgetItem(row.get("description", ""))
                    item_name.setData(QtCore.Qt.UserRole, row["id"])

                    table.setItem(row_idx, 0, item_name)
                    table.setItem(row_idx, 1, item_desc)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load {endpoint}:\n{str(e)}")


    def get_current_data_from_tab(self, tab):
        table = tab.table
        data = []
        for row in range(table.rowCount()):
            item_name = table.item(row, 0)
            item_desc = table.item(row, 1)

            group_id = item_name.data(QtCore.Qt.UserRole)

            data.append({
                "id": group_id,
                "group_name": item_name.text().strip() if item_name else "",
                "description": item_desc.text().strip() if item_desc else ""
            })
        return data

    def is_row_modified(self, current_row, original_row):
        return (
            current_row.get("group_name", "") != original_row.get("group_name", "") or
            current_row.get("description", "") != original_row.get("description", "")
        )

    def delete_selected_group(self):
        tab_index = self.tabs.currentIndex()
        endpoint_map = {0: "Groups/putaway-groups", 1: "Groups/restock-groups", 2: "Groups/pick-groups"}
        current_tab = self.tabs.currentWidget()
        table = current_tab.table
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Delete", "Select a row to delete.")
            return

        group_id = table.item(row, 0).data(QtCore.Qt.UserRole)
        confirm = QMessageBox.question(self, "Delete", "Are you sure?", QMessageBox.Yes | QMessageBox.No)

        if confirm != QMessageBox.Yes:
            return

        endpoint = endpoint_map[tab_index]
        try:
            response = self.api_client.delete(f"/{endpoint}/{group_id}")
            if response.status_code == 200:
                table.removeRow(row)
                QMessageBox.information(self, "Deleted", "Group deleted.")
            else:
                QMessageBox.warning(self, "Error", f"Could not delete:\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Request failed:\n{str(e)}")


    def get_selected_group_info(self):
        tab_index = self.tabs.currentIndex()
        tab = self.tabs.currentWidget()
        table = tab.table
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a group row first.")
            return None, None

        group_name_item = table.item(row, 0)
        if not group_name_item:
            return None, None

        group_name = group_name_item.text()
        group_type = {0: "putaway", 1: "restock", 2: "pick"}.get(tab_index)

        return group_name, group_type



    def save_current_tab_changes(self):
        tab_index = self.tabs.currentIndex()
        tab = self.tabs.currentWidget()
        endpoint_map = {
            0: "Groups/putaway-groups",
            1: "Groups/restock-groups",
            2: "Groups/pick-groups"
        }
        endpoint = endpoint_map.get(tab_index)

        current_data = self.get_current_data_from_tab(tab)
        modified_rows = []
        new_rows = []

        for row in current_data:
            if row["id"] is None:
                # Fila nueva
                if row["group_name"]:  # Solo guardar si tiene nombre
                    new_rows.append(row)
            else:
                original = next((r for r in tab.original_data if r["id"] == row["id"]), None)
                if original and self.is_row_modified(row, original):
                    modified_rows.append(row)

        if not modified_rows and not new_rows:
            QMessageBox.information(self, "Save", "No changes to save.")
            return

        success = True

        # Guardar filas nuevas (POST)
        for row in new_rows:
            print(f"Creating new group: {row['group_name']}, {row['description']}")
            try:
                response = self.api_client.post(
                    f"/{endpoint}/",
                    json={"group_name": row["group_name"], "description": row["description"]}
                )
                if response.status_code != 200:
                    success = False
                    QMessageBox.warning(self, "Error", f"Failed to create group '{row['group_name']}'")
            except Exception as e:
                success = False
                QMessageBox.critical(self, "Error", f"Exception creating group:\n{str(e)}")

        # Guardar filas modificadas (PUT)
        for row in modified_rows:
            try:
                response = self.api_client.put(
                    f"/{endpoint}/{row['id']}",
                    json={"group_name": row["group_name"], "description": row["description"]}
                )
                if response.status_code != 200:
                    success = False
                    QMessageBox.warning(self, "Error", f"Failed to update group ID {row['id']}")
            except Exception as e:
                success = False
                QMessageBox.critical(self, "Error", f"Exception updating group ID {row['id']}:\n{str(e)}")

        if success:
            QMessageBox.information(self, "Saved", "Changes saved successfully.")
            self.load_group_data(endpoint, tab)  # Recargar datos y refrescar original_data


    def add_new_row_to_current_tab(self):
        current_tab = self.tabs.currentWidget()
        table = current_tab.table

        row_position = table.rowCount()
        table.insertRow(row_position)

        item_name = QTableWidgetItem("")
        item_desc = QTableWidgetItem("")

        # No asignamos ID todavía (nuevo registro)
        item_name.setData(QtCore.Qt.UserRole, None)

        table.setItem(row_position, 0, item_name)
        table.setItem(row_position, 1, item_desc)

        # Opcional: mover selección al nuevo
        table.setCurrentCell(row_position, 0)

