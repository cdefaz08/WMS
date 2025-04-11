from PyQt5 import QtWidgets, uic, QtCore
from Layout.UI_PY.UI_ItemConfigurations import Ui_Form  # Asegúrate de que la ruta sea correcta

class ItemConfigurationWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, item_name=None, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.item_name = item_name
        self.setWindowTitle(f"Item Configurations for {self.item_name}")
        self.config_blocks = [self.groupBox]  # Lista para manejar todos los bloques dinámicos
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.scrollAreaWidgetContents.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)



        # Aquí puedes cargar las configuraciones actuales del ítem desde la API
        # y agregarlas dinámicamente si hay más de una

    def add_configuration_block(self):
        # Clonar la UI del groupBox
        new_block = self._clone_config_block()
        self.verticalLayout.addWidget(new_block)
        self.config_blocks.append(new_block)

    def _clone_config_block(self):
        clone = QtWidgets.QGroupBox("New Configuration")
        clone.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        clone_layout = QtWidgets.QVBoxLayout(clone)

        # Sección superior
        topLayout = QtWidgets.QGridLayout()
        topLayout.addWidget(QtWidgets.QLabel("Config Code:"), 0, 0)
        topLayout.addWidget(QtWidgets.QLineEdit(), 0, 1)
        topLayout.addWidget(QtWidgets.QCheckBox("Default Config"), 1, 0)
        topLayout.addWidget(QtWidgets.QCheckBox("Cubiscaned"), 2, 0)
        topLayout.addWidget(QtWidgets.QLabel("Cases per Pallet:"), 0, 2)
        topLayout.addWidget(QtWidgets.QLineEdit(), 0, 3)
        topLayout.addWidget(QtWidgets.QLabel("Pieces per Case:"), 1, 2)
        topLayout.addWidget(QtWidgets.QLineEdit(), 1, 3)
        topLayout.addWidget(QtWidgets.QLabel("Inners per Piece:"), 2, 2)
        topLayout.addWidget(QtWidgets.QLineEdit(), 2, 3)

        clone_layout.addLayout(topLayout)

        # Grid para Pallet, Case, Piece, Inner
        main_grid = QtWidgets.QGridLayout()
        group_titles = ["Pallet", "Case", "Piece", "Inner"]
        value_labels = ["Weight", "Height", "Width", "Depth"]

        col = 0
        for i, group_title in enumerate(group_titles):
            column_layout = QtWidgets.QVBoxLayout()

            # Título del grupo
            title = QtWidgets.QLabel(f"<b>{group_title}</b>")
            title.setAlignment(QtCore.Qt.AlignCenter)
            column_layout.addWidget(title)

            # Campos por grupo
            for value_label in value_labels:
                label = QtWidgets.QLabel(value_label)
                spin = QtWidgets.QSpinBox()
                spin.setMinimumHeight(25)
                combo = QtWidgets.QComboBox()
                combo.setMinimumHeight(25)

                column_layout.addWidget(label)
                column_layout.addWidget(spin)
                column_layout.addWidget(combo)

            # Contenedor de columna
            container = QtWidgets.QWidget()
            container.setLayout(column_layout)
            container.setMinimumWidth(160)
            container.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)

            main_grid.addWidget(container, 0, col)
            col += 1

            # Línea vertical excepto al final
            if i != len(group_titles) - 1:
                vline = QtWidgets.QFrame()
                vline.setFrameShape(QtWidgets.QFrame.VLine)
                vline.setFrameShadow(QtWidgets.QFrame.Sunken)
                main_grid.addWidget(vline, 0, col)
                col += 1

        clone_layout.addLayout(main_grid)

        # 🧩 Asegura altura mínima basada en su contenido
        clone.setMinimumHeight(clone.sizeHint().height())

        return clone



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
