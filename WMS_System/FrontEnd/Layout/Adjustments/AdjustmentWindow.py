from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_AdjustmentWindow import Ui_AdjustmentWindow

class AdjustmentWindow(QtWidgets.QWidget):
    def __init__(self, adjustments_data=None, api_client=None,location_name=None, location_type_rules=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AdjustmentWindow()
        self.ui.setupUi(self)
        self.ui.tree_widget.setAlternatingRowColors(True)
        self.ui.tree_widget.setRootIsDecorated(True)
        self.ui.tree_widget.setHeaderLabels(["PALLET ID", "ITEM CODE", "QTY"])
        self.ui.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tree_widget.setColumnWidth(0, 100)
        self.ui.tree_widget.setColumnWidth(1, 200)
        self.ui.tree_widget.setColumnWidth(2, 60)

        self.location_name = location_name
        self.location_type_rules = location_type_rules

        self.api_client = api_client
        self.adjustments_data = adjustments_data or []

        # Create persistent detail fields once
        self.label_item_code = QtWidgets.QLabel("ITEM CODE:")
        self.input_item_code = QtWidgets.QLineEdit()
        self.input_item_code.setReadOnly(True)

        self.label_qty = QtWidgets.QLabel("QTY:")
        self.input_qty = QtWidgets.QLineEdit()
        self.input_qty.setReadOnly(True)

        self.ui.formLayout.addRow(self.label_item_code, self.input_item_code)
        self.ui.formLayout.addRow(self.label_qty, self.input_qty)

        self.ui.tree_widget.itemClicked.connect(self.on_item_selected)
        self.populate_tree()

    def populate_tree(self):
        self.ui.tree_widget.clear()
        pallets = {}

        for entry in self.adjustments_data:
            pallet_id = entry.get("pallet_id")

            if not pallet_id:
                row = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
                row.setText(0, "")
                row.setText(1, entry["item_id"])
                row.setText(2, str(entry["pieces_on_hand"]))
                row.setData(0, QtCore.Qt.UserRole, entry)
            else:
                if pallet_id not in pallets:
                    parent_item = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
                    parent_item.setText(0, pallet_id)
                    pallets[pallet_id] = parent_item

                child_item = QtWidgets.QTreeWidgetItem()
                child_item.setText(1, entry["item_id"])
                child_item.setText(2, str(entry["pieces_on_hand"]))
                child_item.setData(0, QtCore.Qt.UserRole, entry)

                pallets[pallet_id].addChild(child_item)

    def on_item_selected(self, item, column):
        self.input_item_code.setText(item.text(1))  # ITEM CODE column
        self.input_qty.setText(item.text(2))         # QTY column
