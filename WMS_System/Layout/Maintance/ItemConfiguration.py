from PyQt5 import QtWidgets, uic
from Layout.UI_PY.UI_ItemConfigurations import Ui_Form  # Asegúrate de que la ruta sea correcta

class ItemConfigurationWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, item_name=None, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.item_name = item_name
        self.setWindowTitle(f"Item Configurations for {self.item_name}")
        self.config_blocks = [self.groupBox]  # Lista para manejar todos los bloques dinámicos

        # Aquí puedes cargar las configuraciones actuales del ítem desde la API
        # y agregarlas dinámicamente si hay más de una

    def add_configuration_block(self):
        # Clonar la UI del groupBox
        new_block = self._clone_config_block()
        self.verticalLayout.addWidget(new_block)
        self.config_blocks.append(new_block)



    def _clone_config_block(self):
        clone_group = QtWidgets.QGroupBox("New Configuration")
        layout = QtWidgets.QGridLayout(clone_group)

        # 🧩 Frame 1: Basic Info
        frame1 = QtWidgets.QFrame()
        frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        frame1_layout = QtWidgets.QGridLayout(frame1)
        frame1_layout.addWidget(QtWidgets.QLabel("Config Code:"), 0, 0)
        frame1_layout.addWidget(QtWidgets.QLineEdit(), 0, 1)
        frame1_layout.addWidget(QtWidgets.QCheckBox("Default Config"), 1, 0)
        frame1_layout.addWidget(QtWidgets.QCheckBox("Cubiscaned"), 2, 0)
        layout.addWidget(frame1, 0, 0, 1, 1)

        # 🧩 Frame 2: Cases Info
        frame2 = QtWidgets.QFrame()
        frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        frame2_layout = QtWidgets.QGridLayout(frame2)
        frame2_layout.addWidget(QtWidgets.QLabel("Cases per Pallet:"), 0, 0)
        frame2_layout.addWidget(QtWidgets.QLineEdit(), 0, 1)
        frame2_layout.addWidget(QtWidgets.QLabel("Pieces per Case:"), 1, 0)
        frame2_layout.addWidget(QtWidgets.QLineEdit(), 1, 1)
        frame2_layout.addWidget(QtWidgets.QLabel("Inners per Piece:"), 2, 0)
        frame2_layout.addWidget(QtWidgets.QLineEdit(), 2, 1)
        layout.addWidget(frame2, 0, 1, 1, 1)

        # 🧩 Frames 3–6: Repeated structures
        for col in range(4):
            frame = QtWidgets.QFrame()
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame_layout = QtWidgets.QGridLayout(frame)

            for row in range(4):
                frame_layout.addWidget(QtWidgets.QLabel("TextLabel"), row, 0)
                frame_layout.addWidget(QtWidgets.QSpinBox(), row, 1)
                frame_layout.addWidget(QtWidgets.QComboBox(), row, 2)

            layout.addWidget(frame, 1, col, 1, 1)

        return clone_group


    def validate_default_checkboxes(self):
        defaults = 0
        for block in self.config_blocks:
            checkbox = block.findChild(QtWidgets.QCheckBox, "checkBox")  # o usa objectName dinámico
            if checkbox and checkbox.isChecked():
                defaults += 1

        if defaults > 1:
            QtWidgets.QMessageBox.warning(self, "Error", "Cannot have more than one Default Configuration.")
            return False
        return True
