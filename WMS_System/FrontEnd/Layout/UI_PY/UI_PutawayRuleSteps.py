from PyQt5 import QtWidgets, QtCore


class PutawayStepsMaintWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Putaway Steps Maintenance")

        self.layout = QtWidgets.QVBoxLayout(self)

        # Create header row layout
        header_layout = QtWidgets.QHBoxLayout()
        self.add_section_label(header_layout, "Qualification", 4)
        self.add_section_label(header_layout, "Location", 4)
        self.add_section_label(header_layout, "Optimisation", 2)
        self.layout.addLayout(header_layout)

        # Create the table
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "SEQ #", "Min %", "Max %", "UOM", "Loc Type From",
            "Putaway To", "Loc Type To", "Putaway Group",
            "Sort Expression", "Max Loc Check"
        ])
        self.layout.addWidget(self.table)

    def add_section_label(self, layout, text, column_span):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-weight: bold; background-color: #d0e0ff; border: 1px solid #aaa;")
        label.setAlignment(QtCore.Qt.AlignCenter)

        # Set a fixed width to align with table columns
        total_table_width = 180*6 + 200 + 3*70  # Estimated from your column widths
        section_width = int(total_table_width * (column_span / 10))  # 10 columns total
        label.setFixedWidth(section_width)
        label.setFixedHeight(25)

        layout.addWidget(label)


    def _spinbox(self, value=0, min_val=0, max_val=1000, width=70):
        spin = QtWidgets.QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(value)
        spin.setFixedWidth(width)
        return spin

    def _doublespin(self, value=0.0, min_val=0.0, max_val=1000.0, width=70):
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(value)
        spin.setFixedWidth(width)
        return spin

    def _combobox(self, items, width=70):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setFixedWidth(width)
        return combo

    def _lineedit(self, text="", width=70):
        line = QtWidgets.QLineEdit(text)
        line.setFixedWidth(width)
        return line

