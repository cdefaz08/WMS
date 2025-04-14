from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

class PurchaseOrderMaintUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Purchase Order Maintenance")
        self.setMinimumSize(900, 700)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Main form
        form_layout = QtWidgets.QFormLayout()
        self.input_po_number = QtWidgets.QLineEdit()
        self.input_vendor = QtWidgets.QComboBox()
        self.input_order_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.input_order_date.setDate(QDate.currentDate())
        self.input_expected_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.input_expected_date.setDate(QDate.currentDate())
        self.input_ship_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.input_ship_date.setDate(QDate.currentDate())
        self.input_status = QtWidgets.QComboBox()
        self.input_status.addItems(["Open", "Received", "Cancelled", "Shipped"])
        self.input_created_by = QtWidgets.QLineEdit()
        self.input_created_by.setReadOnly(True)

        form_layout.addRow("PO Number:", self.input_po_number)
        form_layout.addRow("Vendor:", self.input_vendor)
        form_layout.addRow("Order Date:", self.input_order_date)
        form_layout.addRow("Expected Date:", self.input_expected_date)
        form_layout.addRow("Ship Date:", self.input_ship_date)
        form_layout.addRow("Status:", self.input_status)
        form_layout.addRow("Created By:", self.input_created_by)

        # Tabs
        self.tabs = QtWidgets.QTabWidget()

        # Address tab
        self.tab_address = QtWidgets.QWidget()
        address_layout = QtWidgets.QHBoxLayout(self.tab_address)
        address_layout.addWidget(self._address_group("Ship From Company"))
        address_layout.addWidget(self._address_group("Bill To Company"))
        self.tabs.addTab(self.tab_address, "Adress")

        # Custom tab
        self.tab_custom = QtWidgets.QWidget()
        custom_layout = QtWidgets.QFormLayout(self.tab_custom)
        self.custom_fields = []
        for i in range(1, 6):
            custom_input = QtWidgets.QLineEdit()
            self.custom_fields.append(custom_input)
            custom_layout.addRow(f"Custom {i}:", custom_input)
        self.tabs.addTab(self.tab_custom, "Custom")

        # Receipt Lines tab
        self.tab_receipt_lines = QtWidgets.QWidget()
        receipt_layout = QtWidgets.QVBoxLayout(self.tab_receipt_lines)
        self.receipt_table = QtWidgets.QTableWidget()
        self.receipt_table.setColumnCount(10)
        self.receipt_table.setHorizontalHeaderLabels([
            "LINE NUMBER", "UPC", "ITEM CODE", "DESCRIPTION", "QTY ORDERED",
            "QTY EXPECTED", "QTY RECEIVED", "UOM", "UNIT PRICE", "TOTAL PRICE"
        ])
        self.receipt_table.horizontalHeader().setStretchLastSection(True)
        receipt_layout.addWidget(self.receipt_table)
        self.tabs.addTab(self.tab_receipt_lines, "Receipt Lines")

        # Combine layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.tabs)


    def _address_group(self, title):
        group = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QFormLayout(group)

        fields = [
            "Company Name", "Address", "City / State / Zip Code",
            "Country", "Contact Name", "Contact Phone", "Tax ID"
        ]
        for field in fields:
            if "City / State / Zip" in field:
                city = QtWidgets.QLineEdit()
                state = QtWidgets.QLineEdit()
                zip_code = QtWidgets.QLineEdit()
                container = QtWidgets.QHBoxLayout()
                container.addWidget(city)
                container.addWidget(state)
                container.addWidget(zip_code)
                layout.addRow(field + ":", self._wrap(container))
            else:
                layout.addRow(field + ":", QtWidgets.QLineEdit())
        return group

    def _wrap(self, layout):
        w = QtWidgets.QWidget()
        w.setLayout(layout)
        return w
