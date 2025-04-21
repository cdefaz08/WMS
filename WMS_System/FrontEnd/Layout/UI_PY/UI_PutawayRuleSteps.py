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
        self.add_sample_row()

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

    def add_sample_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setCellWidget(row, 0, self._spinbox(1, 1, 1000))
        self.table.setCellWidget(row, 1, self._doublespin(0, 1000))
        self.table.setCellWidget(row, 2, self._doublespin(0, 1000))
        self.table.setCellWidget(row, 3, self._combobox(["Pallet", "Case", "Piece"]))
        self.table.setCellWidget(row, 4, self._combobox(["(Ignore)"], 180))
        self.table.setCellWidget(row, 5, self._combobox(["Empty Locations", "Consolidating Item", "Mixing Items"], 180))
        self.table.setCellWidget(row, 6, self._combobox(["(Ignore)"], 180))
        self.table.setCellWidget(row, 7, self._combobox(["(Ignore)"], 180))
        self.table.setCellWidget(row, 8, self._lineedit("CubeCapUsedA", 200))
        self.table.setCellWidget(row, 9, self._spinbox(0, 100, 180))
        self.table.setColumnWidth(0, 70) # Set width for SEQ #
        self.table.setColumnWidth(1, 85) # Set width for Min %
        self.table.setColumnWidth(2, 85) # Set width for Max %
        self.table.setColumnWidth(3, 125) # Set width for UOM
        self.table.setColumnWidth(4, 180) # Set width for Loc Type From
        self.table.setColumnWidth(5, 180) # Set width for Putaway To
        self.table.setColumnWidth(6, 183) # Set width for Loc Type To
        self.table.setColumnWidth(7, 180) # Set width for Putaway Group
        self.table.setColumnWidth(8, 190) # Set width for Sort Expression
        self.table.setColumnWidth(9, 120) # Set width for Max Loc Check

    def _spinbox(self, min_val, max_val, width=70):
        spin = QtWidgets.QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setFixedWidth(width)
        return spin

    def _doublespin(self, min_val, max_val, width=70):
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(min_val, max_val)
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = PutawayStepsMaintWindow()
    window.resize(1200, 400)
    window.show()
    sys.exit(app.exec_())
