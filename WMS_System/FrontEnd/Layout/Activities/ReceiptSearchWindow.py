from PyQt5 import QtWidgets, QtCore
import requests
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.UI_ReceiptSearch import Ui_ReceiptSearch
from datetime import datetime

class ReceiptSearchWindow(QtWidgets.QDialog, Ui_ReceiptSearch):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client

        self.pushButton_Search.clicked.connect(self.search_receipts)
        # Conectar Enter en todos los lineEdit
        self.lineEdit_Receip_num.returnPressed.connect(self.search_receipts)
        self.lineEdit_Realease_num.returnPressed.connect(self.search_receipts)
        self.lineEdit_VendorName.returnPressed.connect(self.search_receipts)
        self.lineEdit_InvoiceNum.returnPressed.connect(self.search_receipts)
        self.lineEdit_PO.returnPressed.connect(self.search_receipts)
        self.lineEdit_Status.returnPressed.connect(self.search_receipts)
        self.lineEdit_CreatedBy.returnPressed.connect(self.search_receipts)

        self.tableViewReceipts.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewReceipts.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewReceipts.verticalHeader().setVisible(False)

        # Setup date fields
        for date_edit in [
            self.dateEdit_ExpectedDateFrom,
            self.dateEdit_ExpectedDateTo,
            self.dateEdit_ReceivedDateFrom,
            self.dateEdit_ShipDateTo
        ]:
            date_edit.setDisplayFormat("MM/dd/yy")
            date_edit.setSpecialValueText("")
            current_year = QtCore.QDate.currentDate().year()
            date_edit.setDate(QtCore.QDate(current_year, 1, 1))
            date_edit.setCalendarPopup(True)

    def search_receipts(self):
        filters = {
            "receipt_number": self.lineEdit_Receip_num.text().strip(),
            "release_num": self.lineEdit_Realease_num.text().strip(),
            "vendor_name": self.lineEdit_VendorName.text().strip(),
            "invoice_num": self.lineEdit_InvoiceNum.text().strip(),
            "po_id": self.lineEdit_PO.text().strip(),
            "status": self.lineEdit_Status.text().strip(),
            "created_by": self.lineEdit_CreatedBy.text().strip()
        }

        expected_from = self.dateEdit_ExpectedDateFrom.date().toPyDate()
        expected_to = self.dateEdit_ExpectedDateTo.date().toPyDate()
        received_from = self.dateEdit_ReceivedDateFrom.date().toPyDate()
        received_to = self.dateEdit_ShipDateTo.date().toPyDate()

        # Limpiar fechas si no fueron modificadas
        current_year = QtCore.QDate.currentDate().year()
        default_date = QtCore.QDate(current_year, 1, 1).toPyDate()
        expected_from = None if expected_from == default_date else expected_from
        expected_to = None if expected_to == default_date else expected_to
        received_from = None if received_from == default_date else received_from
        received_to = None if received_to == default_date else received_to

        try:
            filters.update({
                "expected_from": expected_from.isoformat() if expected_from else None,
                "expected_to": expected_to.isoformat() if expected_to else None,
                "received_from": received_from.isoformat() if received_from else None,
                "received_to": received_to.isoformat() if received_to else None,
            })

            clean_filters = {k: v for k, v in filters.items() if v}
            response = self.api_client.get("/receipts", params=clean_filters)
            if response.status_code == 200:
                receipts = response.json()
                filtered = []

                for receipt in receipts:
                    match = True

                    for key, val in filters.items():
                        if val and val.lower() not in str(receipt.get(key, "")).lower():
                            match = False
                            break

                    exp_date = receipt.get("date_expected", "")
                    rec_date = receipt.get("date_received", "")

                    expected_date = QtCore.QDate.fromString(exp_date, QtCore.Qt.ISODate).toPyDate() if exp_date else None
                    received_date = QtCore.QDate.fromString(rec_date, QtCore.Qt.ISODate).toPyDate() if rec_date else None

                    if expected_from and expected_date and expected_date < expected_from:
                        match = False
                    if expected_to and expected_date and expected_date > expected_to:
                        match = False
                    if received_from and received_date and received_date < received_from:
                        match = False
                    if received_to and received_date and received_date > received_to:
                        match = False

                    if match:
                        filtered.append(receipt)

                self.populate_table(filtered)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to fetch receipts.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to server.")

    def populate_table(self, receipts):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Receipt #", "Vendor", "Invoice", "Release", "PO", "Expected", "Received",
            "Status", "Created By", "Label Form", "Document Form", "ID"
        ])

        for receipt in receipts:
            exp = receipt.get("date_expected", "")
            rec = receipt.get("date_received", "")

            formatted_exp = datetime.fromisoformat(exp).strftime("%m/%d/%y") if exp else ""
            formatted_rec = datetime.fromisoformat(rec).strftime("%m/%d/%y") if rec else ""

            row = [
                QStandardItem(receipt.get("receipt_number", "")),
                QStandardItem(receipt.get("vendor_name", "")),
                QStandardItem(receipt.get("invoice_num", "")),
                QStandardItem(receipt.get("release_num", "")),
                QStandardItem(str(receipt.get("po_id", ""))),
                QStandardItem(formatted_exp),
                QStandardItem(formatted_rec),
                QStandardItem(receipt.get("status", "")),
                QStandardItem(str(receipt.get("created_by", ""))),
                QStandardItem(receipt.get("label_form", "")),
                QStandardItem(receipt.get("document_form", "")),
                QStandardItem(str(receipt.get("id", "")))  # hidden id
            ]
            model.appendRow(row)

        self.tableViewReceipts.setModel(model)
        self.Records.setText(f"Records found: <b>{len(receipts)}</b>")
        self.tableViewReceipts.setColumnWidth(0, 110)
        self.tableViewReceipts.setColumnWidth(1, 130)
        self.tableViewReceipts.setColumnWidth(2, 100)
        self.tableViewReceipts.setColumnWidth(3, 100)
        self.tableViewReceipts.setColumnWidth(4, 70)
        self.tableViewReceipts.setColumnWidth(5, 100)
        self.tableViewReceipts.setColumnWidth(6, 100)
        self.tableViewReceipts.setColumnWidth(7, 90)
        self.tableViewReceipts.setColumnWidth(8, 100)
        self.tableViewReceipts.setColumnWidth(9, 110)
        self.tableViewReceipts.setColumnWidth(10, 110)
        self.tableViewReceipts.horizontalHeader().setStretchLastSection(False)
        self.tableViewReceipts.setColumnHidden(11, True)

    def get_selected_receipt_id(self):
        if not self.tableViewReceipts:
            return None

        selection_model = self.tableViewReceipts.selectionModel()
        if not selection_model or not selection_model.hasSelection():
            return None

        indexes = selection_model.selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewReceipts.model()
        selected_row = indexes[0].row()
        receipt_id = model.index(selected_row, 11).data(QtCore.Qt.DisplayRole)

        return receipt_id.strip() if receipt_id else None

    def delete_selected_receipt(self):
        selected_row = self.tableViewReceipts.currentIndex().row()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a receipt to delete.")
            return

        model = self.tableViewReceipts.model()
        receipt_number_index = model.index(selected_row, 0)  # Columna 0 = receipt_number
        receipt_number = model.data(receipt_number_index)

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete receipt {receipt_number}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                response = self.api_client.get(f"/receipts/number/{receipt_number}")
                if response.status_code != 200:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Could not load receipt data: {response.text}")
                    return

                receipt_data = response.json()
                receipt_id = receipt_data.get("id")

                if not receipt_id:
                    QtWidgets.QMessageBox.warning(self, "Error", "Receipt ID not found.")
                    return

                delete_response = self.api_client.delete(f"/receipts/{receipt_id}")
                if delete_response.status_code in (200, 204):
                    QtWidgets.QMessageBox.information(self, "Success", "Receipt deleted successfully.")
                    self.search_receipts()  # Refresca la tabla
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete receipt: {delete_response.text}")
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.critical(self, "Network Error", str(e))
