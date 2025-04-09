import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidgetItem, QComboBox, QMainWindow
)
from PyQt5 import QtWidgets
from Layout.UI_PY.order_type_ui import Ui_OrderTypes  # El nombre de la clase puede variar según tu .ui
from config import API_BASE_URL

class OrderTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_OrderTypes()  # Asegúrate de que el nombre coincida con el generado por pyuic5
        self.ui.setupUi(self)
        self.load_data()



    def load_data(self):
        try:
            response = requests.get(f"{API_BASE_URL}/order_types/")
            if response.status_code == 200:
                order_types = response.json()
                self.populate_table(order_types)
            else:
                print("Error loading data:", response.status_code)
        except Exception as e:
            print("Connection error:", e)

    def populate_table(self, order_types):
        table = self.ui.tableWidgetOrderTypes
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Order Type", "Description", "Document Form", "Label Form"])
        table.setColumnHidden(0, True)  # Ocultar la columna de ID
        table.setRowCount(len(order_types))
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(1, 120)  # Order Type
        table.setColumnWidth(2, 250)  # Description
        table.setColumnWidth(3, 150)  # Document Form
        table.setColumnWidth(4, 150)  # Label Form

        for row_idx, item in enumerate(order_types):
            table.setItem(row_idx, 0, QTableWidgetItem(str(item.get("id", ""))))  # ID oculto
            # Column 1 - Order Type
            table.setItem(row_idx, 1, QTableWidgetItem(item.get("order_type", "")))

            # Column 2 - Description
            table.setItem(row_idx, 2, QTableWidgetItem(item.get("description", "")))

            # Column 3 - Document Form (ComboBox)
            doc_combo = QComboBox()
            doc_combo.addItems(["GENERIC", "DROPSHIPMENTS", "AMAZON", "CUSTOM"])
            doc_combo.setCurrentText(item.get("document_form", "GENERIC"))
            table.setCellWidget(row_idx, 3, doc_combo)

            # Column 4- Label Form (ComboBox)
            label_combo = QComboBox()
            label_combo.addItems(["Wal70", "BBB POOL", "AMAZON", "CUSTOM"])
            label_combo.setCurrentText(item.get("label_form", "GENERIC"))  # solo si lo tienes
            table.setCellWidget(row_idx, 4, label_combo)

    def add_new_row(self):
        table = self.ui.tableWidgetOrderTypes
        row_position = table.rowCount()
        table.insertRow(row_position)

        table.setItem(row_position, 1, QTableWidgetItem(""))  # Order Type
        table.setItem(row_position, 2, QTableWidgetItem(""))  # Description

        doc_combo = QComboBox()
        doc_combo.addItems(["GENERIC", "DROPSHIPMENTS", "AMAZON", "CUSTOM"])
        table.setCellWidget(row_position, 3, doc_combo)

        label_combo = QComboBox()
        label_combo.addItems(["Wal70", "BBB POOL", "AMAZON", "CUSTOM"])
        table.setCellWidget(row_position, 4, label_combo)

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
                    # New
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
        self.load_data()

    def delete_selected_row(self):
        table = self.ui.tableWidgetOrderTypes
        selected_row = table.currentRow()

        if selected_row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a row to delete.")
            return

        id_item = table.item(selected_row, 0)

        # Si la fila no tiene ID (es nueva), solo la quitamos localmente
        if not id_item or not id_item.text().strip():
            table.removeRow(selected_row)
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
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Could not delete the Order Type.")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not delete:\n{str(e)}")




