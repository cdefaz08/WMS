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

        # --- Fetch pallets at the location ---
        try:
            pallets_response = self.api_client.get(f"/pallets/by-location/{self.location_name}")
            pallets_data = pallets_response.json() if pallets_response.status_code == 200 else []
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to fetch pallets:\n{str(e)}")
            pallets_data = []

        # --- Create Pallet parent items ---
        for pallet in pallets_data:
            pallet_id = pallet.get("pallet_id")
            parent_item = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
            parent_item.setText(0, pallet_id)
            parent_item.setText(1, "")  # No item code at pallet level
            parent_item.setText(2, "")  # No qty at pallet level
            parent_item.setData(0, QtCore.Qt.UserRole, {"pallet_id": pallet_id})
            pallets[pallet_id] = parent_item

        # --- Add Contents ---
        for entry in self.adjustments_data:
            pallet_id = entry.get("pallet_id")
            if pallet_id and pallet_id in pallets:
                # This pallet already created, add as child
                child_item = QtWidgets.QTreeWidgetItem()
                child_item.setText(1, entry.get("item_id", ""))
                child_item.setText(2, str(entry.get("pieces_on_hand", 0)))
                child_item.setData(0, QtCore.Qt.UserRole, entry)
                pallets[pallet_id].addChild(child_item)
            else:
                # No pallet_id (loose content directly in location)
                row = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
                row.setText(0, "")
                row.setText(1, entry.get("item_id", ""))
                row.setText(2, str(entry.get("pieces_on_hand", 0)))
                row.setData(0, QtCore.Qt.UserRole, entry)

    def on_item_selected(self, item, column):
        self.input_item_code.setText(item.text(1))  # ITEM CODE column
        self.input_qty.setText(item.text(2))         # QTY column


    def get_selected_pallet_id(self):
        selected_item = self.ui.tree_widget.currentItem()
        if selected_item:
            return selected_item.text(0)  # Assuming first column is PALLET ID
        return None