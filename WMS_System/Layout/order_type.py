import requests
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QComboBox
)
from PyQt5 import QtWidgets
from Layout.UI_PY.order_type_ui import Ui_OrderTypes
from config import API_BASE_URL

class OrderTypeWindow(QWidget):
    def __init__(self,api_client = None):
        super().__init__()
        self.ui = Ui_OrderTypes()
        self.ui.setupUi(self)
        self.api_client = api_client

        self.changes_made = False

        self.label_forms = self.fetch_label_forms()
        self.document_forms = self.fetch_document_forms()

        self.ui.tableWidgetOrderTypes.itemChanged.connect(self.mark_changes)
        self.load_data()

    def mark_changes(self):
        self.changes_made = True

    def fetch_label_forms(self):
        try:
            response = requests.get(f"{API_BASE_URL}/label_forms/")
            if response.status_code == 200:
                data = response.json()
                return [item["label_form"] for item in data]
        except Exception as e:
            print("Error fetching label forms:", e)
        return []

    def fetch_document_forms(self):
        try:
            response = requests.get(f"{API_BASE_URL}/document_forms/")
            if response.status_code == 200:
                data = response.json()
                return [item["document_form"] for item in data]
        except Exception as e:
            print("Error fetching document forms:", e)
        return []

    def load_data(self):
        table = self.ui.tableWidgetOrderTypes
        table.blockSignals(True)  # 🔒 Prevent itemChanged from firing during load
        try:
            response = requests.get(f"{API_BASE_URL}/order_types/")
            if response.status_code == 200:
                order_types = response.json()
                self.populate_table(order_types)
        except Exception as e:
            print("Connection error:", e)
        table.blockSignals(False)  # ✅ Re-enable signals after loading

    def populate_table(self, order_types):
        table = self.ui.tableWidgetOrderTypes
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Order Type", "Description", "Document Form", "Label Form"])
        table.setColumnHidden(0, True)
        table.setRowCount(len(order_types))
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(1, 120)
        table.setColumnWidth(2, 250)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 150)

        for row_idx, item in enumerate(order_types):
            table.setItem(row_idx, 0, QTableWidgetItem(str(item.get("id", ""))))
            table.setItem(row_idx, 1, QTableWidgetItem(item.get("order_type", "")))
            table.setItem(row_idx, 2, QTableWidgetItem(item.get("description", "")))

            doc_combo = QComboBox()
            doc_combo.addItems(self.document_forms)
            doc_combo.setCurrentText(item.get("document_form", "GENERIC"))
            doc_combo.currentIndexChanged.connect(self.mark_changes)
            table.setCellWidget(row_idx, 3, doc_combo)

            label_combo = QComboBox()
            label_combo.addItems(self.label_forms)
            label_combo.setCurrentText(item.get("label_form", "GENERIC"))
            label_combo.currentIndexChanged.connect(self.mark_changes)
            table.setCellWidget(row_idx, 4, label_combo)

    def add_new_row(self):
        table = self.ui.tableWidgetOrderTypes
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 1, QTableWidgetItem(""))
        table.setItem(row_position, 2, QTableWidgetItem(""))

        doc_combo = QComboBox()
        doc_combo.addItems(self.document_forms)
        doc_combo.setCurrentText("GENERIC")
        doc_combo.currentIndexChanged.connect(self.mark_changes)
        table.setCellWidget(row_position, 3, doc_combo)

        label_combo = QComboBox()
        label_combo.addItems(self.label_forms)
        label_combo.setCurrentText("GENERIC")
        label_combo.currentIndexChanged.connect(self.mark_changes)
        table.setCellWidget(row_position, 4, label_combo)

        self.changes_made = True

    def save_changes(self):
        table = self.ui.tableWidgetOrderTypes

        for row in range(table.rowCount()):
            id_item = table.item(row, 0)
            order_type = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            description = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            doc_form = table.cellWidget(row, 3).currentText()
            label_form = table.cellWidget(row, 4).currentText()

            data = {
                "order_type": order_type,
                "description": description,
                "document_form": doc_form,
                "label_form": label_form,
            }

            try:
                if not id_item or not id_item.text().strip():
                    response = requests.post(f"{API_BASE_URL}/order_types/", json=data)
                    if response.status_code in (200, 201):
                        new_id = response.json().get("id")
                        table.setItem(row, 0, QTableWidgetItem(str(new_id)))
                else:
                    type_id = id_item.text().strip()
                    requests.put(f"{API_BASE_URL}/order_types/{type_id}", json=data)
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))

        QtWidgets.QMessageBox.information(self, "Saved", "Order types saved successfully.")
        self.changes_made = False
        self.load_data()

    def delete_selected_row(self):
        table = self.ui.tableWidgetOrderTypes
        selected_row = table.currentRow()

        if selected_row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a row to delete.")
            return

        id_item = table.item(selected_row, 0)

        if not id_item or not id_item.text().strip():
            table.removeRow(selected_row)
            self.changes_made = True
            return

        type_id = id_item.text().strip()

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this Order Type?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        try:
            response = requests.delete(f"{API_BASE_URL}/order_types/{type_id}")
            if response.status_code in (200, 204):
                table.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Deleted", "Order Type deleted successfully.")
                self.changes_made = True
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Could not delete the Order Type.")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not delete:\n{str(e)}")

    def closeEvent(self, event):
        if self.changes_made:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to exit?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
