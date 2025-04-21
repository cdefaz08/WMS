from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from Layout.UI_PY.UI_PurchaseOrderSearch import PurchaseOrderSearchUI

class PurchaseOrderSearchWindow(PurchaseOrderSearchUI):
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client  # debe tener headers con el token
        self.marker_date = QDate(2000, 1, 1)

        self.input_start_date.setSpecialValueText("No filter")
        self.input_start_date.setDate(self.marker_date)
        self.input_end_date.setSpecialValueText("No filter")
        self.input_end_date.setDate(self.marker_date)
        
        self.input_po_number.returnPressed.connect(self.search_po)
        self.input_vendor.returnPressed.connect(self.search_po)

        self.btn_search.clicked.connect(self.search_po)
        self.btn_reset.clicked.connect(self.reset_fields)

    def search_po(self):
        try:
            params = {
                "po_number": self.input_po_number.text(),
                "vendor": self.input_vendor.text(),
                "status": self.input_status.currentText()
            }

            # Only include if user changed it from the marker value
            if self.input_start_date.date() != self.marker_date:
                params["start_date"] = self.input_start_date.date().toString("yyyy-MM-dd")

            if self.input_end_date.date() != self.marker_date:
                params["end_date"] = self.input_end_date.date().toString("yyyy-MM-dd")

            # Limpiar parámetros vacíos
            params = {k: v for k, v in params.items() if v}

            response = self.api_client.get("/purchase-orders/search", params=params)
            if response.status_code == 200:
                data = response.json()
                print(data)
                self.populate_table(data)
            else:
                QMessageBox.critical(self, "Error", f"Error: {response.status_code}\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def reset_fields(self):
        self.input_po_number.clear()
        self.input_vendor.clear()
        self.input_status.setCurrentIndex(0)
        self.input_start_date.setDate(self.marker_date)
        self.input_end_date.setDate(self.marker_date)
        self.table.setRowCount(0)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(row.get("id", ""))))  # ID oculto
            self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(row.get("po_number", "")))
            self.table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(row.get("vendor_code", "")))
            self.table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(row.get("order_date", "")))
            self.table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(row.get("status", "")))
            self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(row.get("created_by", "")))
            self.table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(row.get("comments", "")))
        
        self.table.setColumnHidden(0, True)

    def get_selected_po_id(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            return int(self.table.item(selected_row, 0).text())
        return None

    def delete_selected_po(self):
        po_id = self.get_selected_po_id()
        if po_id is None:
            QMessageBox.warning(self, "No Selection", "Please select a Purchase Order to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete the selected Purchase Order?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                response = self.api_client.delete(f"/purchase-orders/{po_id}")
                if response.status_code == 200:
                    QMessageBox.information(self, "Deleted", "Purchase Order deleted successfully.")
                    self.search_po()  # Refresh table
                else:
                    QMessageBox.critical(self, "Error", f"Failed to delete PO.\n{response.status_code}: {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")