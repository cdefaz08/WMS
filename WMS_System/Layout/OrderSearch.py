from PyQt5 import QtWidgets, QtCore
import requests
from config import API_BASE_URL
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.UI_OrderSearch import Ui_OrderSearch
from datetime import datetime

class OrderSearchWindow(QtWidgets.QDialog, Ui_OrderSearch):
    def __init__(self,api_client = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client

        self.pushButton_Search.clicked.connect(self.search_orders)
        self.tableViewOrders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableViewOrders.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewOrders.verticalHeader().setVisible(False)

        # Format and clear date fields
        for date_edit in [
            self.dateEdit_OrderDateFrom,
            self.dateEdit_OrderDateTo,
            self.dateEdit_ShipDateFrom,
            self.dateEdit_ShipDateTo
        ]:
            date_edit.setDisplayFormat("MM/dd/yy")
            date_edit.setSpecialValueText("")
            date_edit.setDate(QtCore.QDate(2000, 1, 1))

    def search_orders(self):
        filters = {
            "order_number": self.lineEdit_Order.text().strip(),
            "customer_name": self.lineEdit_CustomerName.text().strip(),
            "status": self.lineEdit_Status.text().strip(),
            "created_by": self.lineEdit_CreatedBy.text().strip(),
            "document_form": self.lineEdit_DocForm.text().strip(),
            "label_form": self.lineEdit_LabelFrom.text().strip(),
            "order_type": self.comboBox_OrderType.currentText().strip()
        }

        order_from = self.dateEdit_OrderDateFrom.date().toPyDate()
        order_to = self.dateEdit_OrderDateTo.date().toPyDate()
        ship_from = self.dateEdit_ShipDateFrom.date().toPyDate()
        ship_to = self.dateEdit_ShipDateTo.date().toPyDate()

        default_date = QtCore.QDate(2000, 1, 1).toPyDate()
        order_from = None if order_from == default_date else order_from
        order_to = None if order_to == default_date else order_to
        ship_from = None if ship_from == default_date else ship_from
        ship_to = None if ship_to == default_date else ship_to

        try:
            response = requests.get(f"{API_BASE_URL}/orders")
            if response.status_code == 200:
                orders = response.json()
                filtered = []

                for order in orders:
                    match = True

                    for key, val in filters.items():
                        if val and val.lower() not in str(order.get(key, "")).lower():
                            match = False
                            break

                    order_date_str = order.get("order_date", "")
                    ship_date_str = order.get("ship_date", "")

                    order_date = QtCore.QDate.fromString(order_date_str, QtCore.Qt.ISODate).toPyDate() if order_date_str else None
                    ship_date = QtCore.QDate.fromString(ship_date_str, QtCore.Qt.ISODate).toPyDate() if ship_date_str else None

                    if order_from and order_date and order_date < order_from:
                        match = False
                    if order_to and order_date and order_date > order_to:
                        match = False
                    if ship_from and ship_date and ship_date < ship_from:
                        match = False
                    if ship_to and ship_date and ship_date > ship_to:
                        match = False

                    if match:
                        filtered.append(order)

                self.populate_table(filtered)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to fetch orders.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to server.")

    def populate_table(self, orders):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Order #", "Customer", "Order Date", "Ship Date", "Status",
            "Total", "Created By", "Comments", "Label Form", "Document Form", "Order Type"
        ])

        for order in orders:
            order_date = order.get("order_date", "")
            ship_date = order.get("ship_date", "")

            formatted_order_date = datetime.fromisoformat(order_date).strftime("%m/%d/%y") if order_date else ""
            formatted_ship_date = datetime.fromisoformat(ship_date).strftime("%m/%d/%y") if ship_date else ""

            row = [
                QStandardItem(order.get("order_number", "")),
                QStandardItem(order.get("customer_name", "")),
                QStandardItem(formatted_order_date),
                QStandardItem(formatted_ship_date),
                QStandardItem(order.get("status", "")),
                QStandardItem(str(order.get("total_amount", ""))),
                QStandardItem(str(order.get("created_by", ""))),
                QStandardItem(order.get("comments", "")),
                QStandardItem(order.get("label_form", "")),
                QStandardItem(order.get("document_form", "")),
                QStandardItem(order.get("order_type", "")),
                QStandardItem(str(order.get("id", "")))  # 👈 This is the order_id for internal use
            ]
            model.appendRow(row)

        self.tableViewOrders.setModel(model)
        self.Records.setText(f"Records found: <b>{len(orders)}</b>")
        self.tableViewOrders.setColumnWidth(0, 100)  # Order #
        self.tableViewOrders.setColumnWidth(1, 140)  # Customer
        self.tableViewOrders.setColumnWidth(2, 130)   # Order Date
        self.tableViewOrders.setColumnWidth(3, 130)   # Ship Date
        self.tableViewOrders.setColumnWidth(4, 80)   # Status
        self.tableViewOrders.setColumnWidth(5, 70)   # Total
        self.tableViewOrders.setColumnWidth(6, 120)   # Created By
        self.tableViewOrders.setColumnWidth(7, 120)  # Comments
        self.tableViewOrders.setColumnWidth(8, 130)  # Label Form
        self.tableViewOrders.setColumnWidth(9, 130)  # Document Form
        self.tableViewOrders.setColumnWidth(10, 120) # Order Type       
        self.tableViewOrders.horizontalHeader().setStretchLastSection(False)
        self.tableViewOrders.setColumnHidden(11, True)  # Hide the ID column

    def get_selected_order_id(self):
        if not self.tableViewOrders:
            return None

        selection_model = self.tableViewOrders.selectionModel()
        if not selection_model or not selection_model.hasSelection():
            return None

        indexes = selection_model.selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewOrders.model()
        selected_row = indexes[0].row()
        order_number = model.index(selected_row, 11).data(QtCore.Qt.DisplayRole)  # columna 11 es "Order_id"
        
        return order_number.strip() if order_number else None

