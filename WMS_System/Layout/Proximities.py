from PyQt5 import QtWidgets
from Layout.UI_PY.ui_proximities import Ui_Form  # Change Ui_Dialog to your actual class name in the .py file
from config import API_BASE_URL
import requests

class ProximityWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tableWidgetProximities.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidgetProximities.verticalHeader().setVisible(False)

        self.load_data()

    def load_data(self):
        try:
            response = requests.get(f"{API_BASE_URL}/proximities")
            if response.status_code == 200:
                data = response.json()
            else:
                data = []
        except Exception:
            data = []

        self.fill_table(self.ui.tableWidgetProximities, data)

    def fill_table(self, table_widget, data):
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["ID", "Proximity", "Movers"])

        for row_index, item in enumerate(data):
            table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item["id"])))
            table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item["proximity"]))
            table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(item["movers"])))

            table_widget.setColumnHidden(0, True)

            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def add_new_row(self):
        table = self.ui.tableWidgetProximities
        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(""))  # ID (hidden)
        table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(""))  # Proximity
        table.setItem(row_position, 2, QtWidgets.QTableWidgetItem("0"))  # Movers

    def save_changes(self):
        table = self.ui.tableWidgetProximities
        for row in range(table.rowCount()):
            id_item = table.item(row, 0)
            proximity = table.item(row, 1).text() if table.item(row, 1) else ""
            movers = int(table.item(row, 2).text()) if table.item(row, 2) else 0

            data = {
                "proximity": proximity,
                "movers": movers
            }

            try:
                if not id_item or not id_item.text().strip():
                    response = requests.post(f"{API_BASE_URL}/proximities", json=data)
                    if response.status_code in (200, 201):
                        new_id = response.json().get("id")
                        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(new_id)))
                else:
                    proximity_id = id_item.text().strip()
                    requests.put(f"{API_BASE_URL}/proximities/{proximity_id}", json=data)
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))

        self.load_data()

    def has_unsaved_changes(self):
        try:
            response = requests.get(f"{API_BASE_URL}/proximities")
            if response.status_code != 200:
                return False

            original_data = {str(item["id"]): item for item in response.json()}

            table = self.ui.tableWidgetProximities
            for row in range(table.rowCount()):
                id_item = table.item(row, 0)
                proximity = table.item(row, 1).text() if table.item(row, 1) else ""
                movers = table.item(row, 2).text() if table.item(row, 2) else "0"

                if not id_item or not id_item.text().strip():
                    return True  # New unsaved row

                id_str = id_item.text().strip()
                if id_str in original_data:
                    original = original_data[id_str]
                    if (
                        original["proximity"] != proximity
                        or str(original["movers"]) != movers
                    ):
                        return True  # Row was modified
        except Exception:
            return False

        return False  # All rows match the original


    def delete_selected_row(self):
        table = self.ui.tableWidgetProximities
        selected_row = table.currentRow()

        if selected_row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a row to delete.")
            return

        id_item = table.item(selected_row, 0)

        # If it's a new row (not yet saved), just remove it locally
        if not id_item or not id_item.text().strip():
            table.removeRow(selected_row)
            return

        proximity_id = id_item.text().strip()

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this proximity?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        try:
            response = requests.delete(f"{API_BASE_URL}/proximities/{proximity_id}")
            if response.status_code in (200, 204):
                table.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Deleted", "Proximity deleted successfully.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Could not delete the proximity.")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not delete:\n{str(e)}")


    def closeEvent(self, event):
        if self.has_unsaved_changes():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to close without saving?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                event.ignore()
                return
        event.accept()