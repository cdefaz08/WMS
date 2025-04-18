from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QComboBox, QTableWidgetItem, QMessageBox, QPushButton


class GroupClassTableWindow(QWidget):
    def __init__(self, api_client, group_name, group_type, group_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.group_name = group_name
        self.group_type = group_type
        self.group_data = group_data or []
        self.class_options = []
        self.original_data = []
        self.endpoint = f"group-classes/{self.group_type}"

        self.setWindowTitle(f"{group_type.capitalize()} Classes for Group: {group_name}")
        self.resize(800, 400)

        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Class", "Priority", "Min %", "Max %"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        layout.addWidget(self.table)



        self.load_class_dropdown_data()

    def load_class_dropdown_data(self):
        try:
            response = self.api_client.get(f"/classes/{self.group_type}")
            if response.status_code == 200:
                self.class_options = response.json()
                if self.group_data:
                    self.load_group_data_into_table()
                else:
                    self.add_empty_row()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load class list:\n{str(e)}")

    def add_empty_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        combo = QComboBox()
        for class_data in self.class_options:
            combo.addItem(class_data["class_name"])
        combo.setProperty("group_name", self.group_name)
        combo.setProperty("row_id", None)  # None for new rows
        self.table.setCellWidget(row, 0, combo)

        self.table.setItem(row, 1, QTableWidgetItem("0"))      # Priority
        self.table.setItem(row, 2, QTableWidgetItem("0.0"))    # Min %
        self.table.setItem(row, 3, QTableWidgetItem("100.0"))  # Max %

    def load_group_data_into_table(self):
        for row_data in self.group_data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            combo = QComboBox()
            for class_data in self.class_options:
                combo.addItem(class_data["class_name"])
            combo.setCurrentText(row_data["class_name"])
            combo.setProperty("group_name", row_data["group_name"])
            combo.setProperty("row_id", row_data["id"])
            self.table.setCellWidget(row, 0, combo)

            self.table.setItem(row, 1, QTableWidgetItem(str(row_data["priority"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data["min_percent"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(row_data["max_percent"])))

        self.original_data = self.get_current_data()

    def get_current_data(self):
        data = []
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 0)
            priority = self.table.item(row, 1)
            min_percent = self.table.item(row, 2)
            max_percent = self.table.item(row, 3)

            item = {
                "id": combo.property("row_id"),
                "group_name": combo.property("group_name"),
                "class_name": combo.currentText(),
                "priority": int(priority.text()) if priority else 0,
                "min_percent": float(min_percent.text()) if min_percent else 0.0,
                "max_percent": float(max_percent.text()) if max_percent else 0.0
            }
            data.append(item)
        return data

    def is_row_modified(self, new_row, original_row):
        return any(
            new_row.get(k) != original_row.get(k)
            for k in ["class_name", "priority", "min_percent", "max_percent"]
        )

    def save_changes(self):
        current_data = self.get_current_data()
        to_create = []
        to_update = []

        for row in current_data:
            if row["id"] is None:
                to_create.append(row)
            else:
                original = next((r for r in self.original_data if r["id"] == row["id"]), None)
                if original and self.is_row_modified(row, original):
                    to_update.append(row)

        success = True

        for row in to_create:
            try:
                response = self.api_client.post(f"/{self.endpoint}/", json=row)
                if response.status_code != 200:
                    success = False
                    QMessageBox.warning(self, "Error", f"Failed to create class '{row['class_name']}'")
            except Exception as e:
                success = False
                QMessageBox.critical(self, "Error", f"Error creating class:\n{str(e)}")

        for row in to_update:
            try:
                response = self.api_client.put(f"/{self.endpoint}/{row['id']}", json=row)
                if response.status_code != 200:
                    success = False
                    QMessageBox.warning(self, "Error", f"Failed to update class ID {row['id']}")
            except Exception as e:
                success = False
                QMessageBox.critical(self, "Error", f"Error updating class ID {row['id']}:\n{str(e)}")

        if success:
            QMessageBox.information(self, "Saved", "Changes saved successfully.")
            self.refresh_data()

    def refresh_data(self):
        try:
            response = self.api_client.get(f"/{self.endpoint}/")
            if response.status_code == 200:
                all_data = response.json()
                self.group_data = [d for d in all_data if d["group_name"] == self.group_name]
                self.table.setRowCount(0)
                self.load_group_data_into_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh data:\n{str(e)}")

    def delete_selected_row(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Delete", "Please select a row to delete.")
            return

        combo = self.table.cellWidget(row, 0)
        row_id = combo.property("row_id")

        if row_id:
            confirm = QMessageBox.question(self, "Delete", "Are you sure you want to delete this class?", QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                return
            try:
                response = self.api_client.delete(f"/{self.endpoint}/{row_id}")
                if response.status_code == 200:
                    self.table.removeRow(row)
                    QMessageBox.information(self, "Deleted", "Class deleted successfully.")
                else:
                    QMessageBox.warning(self, "Error", f"Could not delete class:\n{response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete class:\n{str(e)}")
        else:
            self.table.removeRow(row)
