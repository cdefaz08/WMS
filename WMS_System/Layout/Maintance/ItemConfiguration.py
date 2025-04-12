from PyQt5 import QtWidgets, QtCore, QtGui

class ItemConfigurationWindow(QtWidgets.QWidget):
    def __init__(self, item_config=None, item_name=None, api_client=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Item Configurations for {item_name}")
        self.api_client = api_client
        self.item_name = item_name

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.scrollArea)

        self.config_blocks = []

        if item_config:
            for config in item_config:
                self.load_config_block(config)
        else:
            # ✅ Si no hay configuraciones, creamos un bloque nuevo vacío
            self.add_configuration_block()

    def load_config_block(self, config_data):
        group_box = self._clone_config_block()
        group_box.config_id = config_data.get("id", None)

        # Inputs superiores
        group_box.findChild(QtWidgets.QLineEdit, "input_config").setText(config_data.get("configuration_name", ""))
        group_box.findChild(QtWidgets.QLineEdit, "input_cases").setText(str(config_data.get("boxes_per_pallet", "")))
        group_box.findChild(QtWidgets.QLineEdit, "input_pieces").setText(str(config_data.get("pieces_per_case", "")))
        group_box.findChild(QtWidgets.QLineEdit, "input_inners").setText(str(config_data.get("inners_per_piece", "")))

        for checkbox in group_box.findChildren(QtWidgets.QCheckBox):
            if checkbox.text().lower() == "default config":
                checkbox.setChecked(config_data.get("is_default", False))
            elif checkbox.text().lower() == "cubiscaned":
                checkbox.setChecked(config_data.get("cubiscaned", False))

        # Campos de medida
        mapping = {
            "pallet": ["pallet_weight", "pallet_height", "pallet_width", "pallet_length"],
            "case": ["case_weight", "case_height", "case_width", "case_length"],
            "piece": ["piece_weight", "piece_height", "piece_width", "piece_length"],
            "inner": ["inner_weight", "inner_height", "inner_width", "inner_length"],
        }

        sections = ["Pallet", "Case", "Piece", "Inner"]
        units_weight = ["LB", "KG", "G"]
        units_size = ["IN", "CM", "M"]

        spins = group_box.findChildren(QtWidgets.QSpinBox)
        combos = group_box.findChildren(QtWidgets.QComboBox)

        idx = 0
        for section in sections:
            for i, field in enumerate(mapping[section.lower()]):
                value = config_data.get(field, 0)
                spins[idx].setValue(int(value))
                combos[idx].clear()
                combos[idx].addItems(units_weight if i == 0 else units_size)
                combos[idx].setCurrentText(config_data.get("unit_of_measure", units_weight[0] if i == 0 else units_size[0]))
                idx += 1

        self.verticalLayout.addWidget(group_box)
        self.config_blocks.append(group_box)

    def add_configuration_block(self, config_data=None):
        block = self._clone_config_block(config_data)
        self.verticalLayout.addWidget(block)
        self.config_blocks.append(block)


    def _clone_config_block(self,config_data=None):
        group_box = QtWidgets.QGroupBox("New Configuration")
        group_box.setProperty("selected", False)  # Just to track
        group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        layout = QtWidgets.QVBoxLayout(group_box)

        formLayout = QtWidgets.QGridLayout()
        def input(name):
            w = QtWidgets.QLineEdit()
            w.setObjectName(name)
            w.setValidator(QtGui.QIntValidator(0, 999999))
            w.setMaxLength(6)  # Asegúrate de que el límite no sea 2  # 💡 Allow up to 6-digit numbers
            return w
        formLayout.addWidget(QtWidgets.QLabel("Config Code:"), 0, 0)
        formLayout.addWidget(input("input_config"), 0, 1)
        formLayout.addWidget(QtWidgets.QCheckBox("Default Config"), 1, 0)
        formLayout.addWidget(QtWidgets.QCheckBox("Cubiscaned"), 2, 0)
        formLayout.addWidget(QtWidgets.QLabel("Cases per Pallet:"), 0, 2)
        formLayout.addWidget(input("input_cases"), 0, 3)
        formLayout.addWidget(QtWidgets.QLabel("Pieces per Case:"), 1, 2)
        formLayout.addWidget(input("input_pieces"), 1, 3)
        formLayout.addWidget(QtWidgets.QLabel("Inners per Piece:"), 2, 2)
        formLayout.addWidget(input("input_inners"), 2, 3)
        layout.addLayout(formLayout)

        grid = QtWidgets.QGridLayout()
        group_titles = ["Pallet", "Case", "Piece", "Inner"]
        value_labels = ["Weight", "Height", "Width", "Depth"]
        col = 0

        for i, group in enumerate(group_titles):
            column_layout = QtWidgets.QVBoxLayout()
            title = QtWidgets.QLabel(f"<b>{group}</b>")
            title.setAlignment(QtCore.Qt.AlignCenter)
            column_layout.addWidget(title)

            for label in value_labels:
                column_layout.addWidget(QtWidgets.QLabel(label))

                spin = QtWidgets.QSpinBox()
                spin.setMinimum(0)
                spin.setMaximum(999999)  # Aumenta el límite
                spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
                spin.setFocusPolicy(QtCore.Qt.StrongFocus)
                spin.wheelEvent = lambda e: e.ignore()
                spin.setMinimumHeight(25)
                spin.setAlignment(QtCore.Qt.AlignLeft)  # Evita centrar con ceros visibles
                spin.setPrefix("")  # Asegura que no haya prefijos raros
                column_layout.addWidget(spin)

                combo = QtWidgets.QComboBox()
                combo.setMinimumHeight(25)
                combo.setFocusPolicy(QtCore.Qt.StrongFocus)
                combo.wheelEvent = lambda e: e.ignore()  # Desactiva scroll

                if label == "Weight":
                    combo.addItems(["LB", "KG", "G"])
                else:
                    combo.addItems(["IN", "CM", "M"])

                column_layout.addWidget(combo)

            container = QtWidgets.QWidget()
            container.setLayout(column_layout)
            container.setMinimumWidth(160)
            container.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            grid.addWidget(container, 0, col)
            col += 1

            if i < len(group_titles) - 1:
                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.VLine)
                line.setFrameShadow(QtWidgets.QFrame.Sunken)
                grid.addWidget(line, 0, col)
                col += 1
        
        layout.addLayout(grid)
        group_box.mousePressEvent = lambda event, box=group_box: self.select_config_block(box)
        self.update_block_style(group_box, selected=False)
        return group_box
    
    def select_config_block(self, selected_box):
        for block in self.config_blocks:
            is_selected = block == selected_box
            block.setProperty("selected", is_selected)
            self.update_block_style(block, selected=is_selected)

    def update_block_style(self, block, selected):
        if selected:
            block.setStyleSheet("""
                QGroupBox {
                    border: 2px solid #fd7014;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            """)
        else:
            block.setStyleSheet("""
                QGroupBox {
                    border: 1px solid lightgray;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            """)



    def save_all_configurations(self):
        has_default = any(
            block.findChildren(QtWidgets.QCheckBox)[0].isChecked() for block in self.config_blocks
        )

        if not has_default:
            QtWidgets.QMessageBox.warning(self, "Warning", "At least one configuration must be marked as Default.")
            return

        for block in self.config_blocks:
            data = self.extract_data_from_block(block)
            config_id = getattr(block, "config_id", None)

            try:
                if config_id:
                    response = self.api_client.put(f"/item-config/{config_id}", json=data)
                else:
                    response = self.api_client.post(f"/item-config", json=data)

                if response.status_code in (200, 201):
                    QtWidgets.QMessageBox.information(self, "Success", "Configuration saved successfully.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Failed", "Error saving configuration.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))



    def delete_selected_configuration(self):
        selected_block = next((b for b in self.config_blocks if b.property("selected")), None)

        if not selected_block:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a configuration to delete.")
            return

        config_id = getattr(selected_block, "config_id", None)
        if config_id:
            try:
                response = self.api_client.delete(f"/item-config/{config_id}")
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Deleted", "Configuration deleted from server.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete configuration from server.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

        self.verticalLayout.removeWidget(selected_block)
        selected_block.deleteLater()
        self.config_blocks.remove(selected_block)

        # ✅ Asegurar que haya un default si queda al menos un bloque
        if self.config_blocks:
            still_has_default = any(b.findChildren(QtWidgets.QCheckBox)[0].isChecked() for b in self.config_blocks)
            if not still_has_default:
                self.config_blocks[0].findChildren(QtWidgets.QCheckBox)[0].setChecked(True)

    def extract_data_from_block(self, block):
        data = {
            "item_id": self.item_name,
            "configuration_name": block.findChild(QtWidgets.QLineEdit, "input_config").text(),
            "boxes_per_pallet": int(block.findChild(QtWidgets.QLineEdit, "input_cases").text() or 0),
            "pieces_per_case": int(block.findChild(QtWidgets.QLineEdit, "input_pieces").text() or 0),
            "inners_per_piece": int(block.findChild(QtWidgets.QLineEdit, "input_inners").text() or 0),
            "is_default": block.findChildren(QtWidgets.QCheckBox)[0].isChecked(),
            "cubiscaned": block.findChildren(QtWidgets.QCheckBox)[1].isChecked(),
        }

        # Mapear las medidas
        sections = ["pallet", "case", "piece", "inner"]
        metrics = ["weight", "height", "width", "length"]
        spins = block.findChildren(QtWidgets.QSpinBox)
        combos = block.findChildren(QtWidgets.QComboBox)

        i = 0
        for section in sections:
            for metric in metrics:
                data[f"{section}_{metric}"] = spins[i].value()
                # Puedes mapear los combos si quieres guardar unidad
                # data[f"{section}_{metric}_uom"] = combos[i].currentText()
                i += 1

        return data

