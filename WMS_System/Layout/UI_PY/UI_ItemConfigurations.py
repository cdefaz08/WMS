from PyQt5 import QtWidgets, QtCore

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # ---------------------------
        # GROUPBOX ORIGINAL
        # ---------------------------
        self.groupBox = QtWidgets.QGroupBox("Item Configuration")
        self.groupBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.vboxGroup = QtWidgets.QVBoxLayout(self.groupBox)

        # --- Top Layout
        topLayout = QtWidgets.QGridLayout()
        topLayout.addWidget(QtWidgets.QLabel("Config Code:"), 0, 0)
        self.input_config = QtWidgets.QLineEdit()
        self.input_config.setMinimumWidth(200)
        topLayout.addWidget(self.input_config, 0, 1)

        self.checkbox_default = QtWidgets.QCheckBox("Default Config")
        self.checkbox_cubiscan = QtWidgets.QCheckBox("Cubiscaned")
        topLayout.addWidget(self.checkbox_default, 1, 0)
        topLayout.addWidget(self.checkbox_cubiscan, 2, 0)

        topLayout.addWidget(QtWidgets.QLabel("Cases per Pallet:"), 0, 2)
        self.input_cases = QtWidgets.QLineEdit()
        topLayout.addWidget(self.input_cases, 0, 3)
        topLayout.addWidget(QtWidgets.QLabel("Pieces per Case:"), 1, 2)
        self.input_pieces = QtWidgets.QLineEdit()
        topLayout.addWidget(self.input_pieces, 1, 3)
        topLayout.addWidget(QtWidgets.QLabel("Inners per Piece:"), 2, 2)
        self.input_inners = QtWidgets.QLineEdit()
        topLayout.addWidget(self.input_inners, 2, 3)

        self.vboxGroup.addLayout(topLayout)

        # --- Grid Layout Section
        grid = QtWidgets.QGridLayout()
        group_titles = ["Pallet", "Case", "Piece", "Inner"]
        value_labels = ["Weight", "Height", "Width", "Depth"]

        col = 0
        for i, group_title in enumerate(group_titles):
            column_layout = QtWidgets.QVBoxLayout()
            title = QtWidgets.QLabel(f"<b>{group_title}</b>")
            title.setAlignment(QtCore.Qt.AlignCenter)
            column_layout.addWidget(title)

            for label_text in value_labels:
                column_layout.addWidget(QtWidgets.QLabel(label_text))

                spin = QtWidgets.QSpinBox()
                spin.setMinimumHeight(25)
                column_layout.addWidget(spin)

                combo = QtWidgets.QComboBox()
                combo.setMinimumHeight(25)
                combo.setObjectName(f"{group_title.lower()}_{label_text.lower()}_uom")  # Ej: pallet_weight_uom

            column_widget = QtWidgets.QWidget()
            column_widget.setLayout(column_layout)
            column_widget.setMinimumWidth(160)
            column_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

            grid.addWidget(column_widget, 0, col)
            col += 1

            if i < len(group_titles) - 1:
                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.VLine)
                line.setFrameShadow(QtWidgets.QFrame.Sunken)
                grid.addWidget(line, 0, col)
                col += 1

        self.vboxGroup.addLayout(grid)

        # ----------------------------
        # FINALIZE
        # ----------------------------
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Item Configurations"))
