from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QGroupBox, QHeaderView, QSpacerItem, QSizePolicy, QFormLayout
)
from PyQt5.QtCore import Qt


class RetailSaleUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Retail Sale")


        # Layout principal dividido en 2 columnas
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # Columna izquierda: formulario, totales, botones
        self.left_panel = QVBoxLayout()
        self.setup_sale_info()
        self.setup_summary()
        self.main_layout.addLayout(self.left_panel, 2)

        # Columna derecha: tabla de ítems y campo de escaneo
        self.right_panel = QVBoxLayout()
        self.setup_table_area()
        self.main_layout.addLayout(self.right_panel, 3)  # más espacio para la tabla

    def setup_sale_info(self):
        group = QGroupBox("Customer Sale Info")
        layout = QFormLayout()

        self.input_sale_number = QLabel("(Auto)")
        self.input_date = QLabel("(Auto)")
        self.input_user = QLabel("(Current User)")

        self.input_customer_name = QLineEdit()
        self.input_contact = QLineEdit()

        self.combo_payment = QComboBox()
        self.combo_payment.addItems(["Cash", "Credit Card", "Debit", "Mobile Payment"])

        layout.addRow("Sale #:", self.input_sale_number)
        layout.addRow("Date:", self.input_date)
        layout.addRow("User:", self.input_user)
        layout.addRow("Customer Name:", self.input_customer_name)
        layout.addRow("Contact:", self.input_contact)
        layout.addRow("Payment Method:", self.combo_payment)

        group.setLayout(layout)
        self.left_panel.addWidget(group)


    def setup_table_area(self):
        self.input_upc_scanner = QLineEdit()
        self.input_upc_scanner.setPlaceholderText("Scan or enter UPC and press Enter")
        self.input_upc_scanner.setClearButtonEnabled(True)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "UPC", "Code", "Desc", "Qty", "Price", "Disc", "Total"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.right_panel.addWidget(self.input_upc_scanner)
        self.right_panel.addWidget(self.table)

        # Botones debajo si quieres
        btns = QHBoxLayout()
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_remove_item = QPushButton("🗑️ Remove Selected")
        btns.addWidget(self.btn_add_item)
        btns.addWidget(self.btn_remove_item)
        self.right_panel.addLayout(btns)


    def setup_summary(self):
        layout = QHBoxLayout()

        # Grupo Totales
        totals_group = QGroupBox("Totals")
        form = QFormLayout()

        self.input_subtotal = QLabel("0.00")
        self.input_discount_total = QLabel("0.00")
        self.input_tax = QLabel("0.00")
        self.input_total = QLabel("<b>0.00</b>")
        self.input_received = QLineEdit()
        self.input_change = QLabel("0.00")

        form.addRow("Subtotal:", self.input_subtotal)
        form.addRow("Discount:", self.input_discount_total)
        form.addRow("Tax:", self.input_tax)
        form.addRow("Total:", self.input_total)
        form.addRow("Amount Received:", self.input_received)
        form.addRow("Change Due:", self.input_change)

        totals_group.setLayout(form)
        layout.addWidget(totals_group, 2)

        # Botones
        button_box = QVBoxLayout()
        self.btn_confirm = QPushButton("✅ Confirm Sale")
        self.btn_print = QPushButton("🖨️ Print Receipt")
        self.btn_cancel = QPushButton("❌ Cancel")
        for btn in [self.btn_confirm, self.btn_print, self.btn_cancel]:
            btn.setMinimumHeight(40)
            button_box.addWidget(btn)
        button_box.addStretch()

        layout.addLayout(button_box, 1)

        self.left_panel.addLayout(layout)
