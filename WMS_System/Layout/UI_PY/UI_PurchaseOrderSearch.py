from PyQt5 import QtWidgets, QtCore

class PurchaseOrderSearchUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purchase Order Search")
        self.resize(1000, 600)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self)

        # Inputs
        self.input_po_number = QtWidgets.QLineEdit()
        self.input_vendor = QtWidgets.QLineEdit()
        self.input_status = QtWidgets.QComboBox()
        self.input_status.addItems(["", "Open", "Shipped", "Cancelled", "Received"])

        self.input_start_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.input_start_date.setCalendarPopup(True)

        self.input_end_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.input_end_date.setCalendarPopup(True)

        # Form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("PO Number:", self.input_po_number)
        form_layout.addRow("Vendor:", self.input_vendor)
        form_layout.addRow("Status:", self.input_status)
        form_layout.addRow("Start Date:", self.input_start_date)
        form_layout.addRow("End Date:", self.input_end_date)
        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.btn_search = QtWidgets.QPushButton("Search")
        self.btn_reset = QtWidgets.QPushButton("Reset")
        button_layout.addWidget(self.btn_search)
        button_layout.addWidget(self.btn_reset)
        main_layout.addLayout(button_layout)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["PO NUMBER", "VENDOR", "ORDER DATE", "STATUS", "CREATED BY", "COMMENTS"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)
