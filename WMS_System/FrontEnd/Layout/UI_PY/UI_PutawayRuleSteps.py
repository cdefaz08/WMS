from PyQt5 import QtWidgets, QtCore


class PutawayStepsMaintWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Putaway Steps Maintenance")

        self.layout = QtWidgets.QVBoxLayout(self)


# Create header row layout
        header_layout = QtWidgets.QHBoxLayout()

        self.add_section_label(header_layout, "Qualification", 457)
        self.add_section_label(header_layout, "Location", 480)
        self.add_section_label(header_layout, "Optimisation", 349)

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
        self.table.setColumnWidth(0, 72)
        self.table.setColumnWidth(1, 75)
        self.table.setColumnWidth(2, 75)
        self.table.setColumnWidth(3, 75)
        self.table.setColumnWidth(4, 160)
        self.table.setColumnWidth(5, 180)
        self.table.setColumnWidth(6, 155)
        self.table.setColumnWidth(7, 155)
        self.table.setColumnWidth(8, 199)
        self.table.setColumnWidth(9, 150)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

    def add_section_label(self, layout, text, fixed_width):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-weight: bold; background-color: #dee0ff; border: 1px solid #aaa;")
        label.setAlignment(QtCore.Qt.AlignCenter)

        label.setFixedWidth(fixed_width)
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

