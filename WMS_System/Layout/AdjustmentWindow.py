# adjustment_window.py
from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_AdjustmentWindow import Ui_AdjustmentWindow

class AdjustmentWindow(QtWidgets.QWidget):
    def __init__(self, adjustments_data=None, api_client=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AdjustmentWindow()
        self.ui.setupUi(self)
        self.api_client = api_client
        self.adjustments_data = adjustments_data or []

        self.ui.treeView.clicked.connect(self.on_item_selected)
        self.populate_tree()

    def populate_tree(self):
        pallets = {}
        for item in self.adjustments_data:
            pallet_id = item.get("pallet_id", "Unknown")
            if pallet_id not in pallets:
                pallets[pallet_id] = QtWidgets.QTreeWidgetItem([pallet_id])
                self.ui.tree_widget.addTopLevelItem(pallets[pallet_id])
            item_node = QtWidgets.QTreeWidgetItem([
                item.get("item_code", ""),
                str(item.get("onhand_qty", ""))
            ])
            item_node.setData(0, QtCore.Qt.UserRole, item)
            pallets[pallet_id].addChild(item_node)

    def on_item_selected(self, item, column):
        data = item.data(0, QtCore.Qt.UserRole)
        if not data:
            # It's a pallet node, try to find details for that pallet
            pallet_id = item.text(0)
            for d in self.adjustments_data:
                if d.get("pallet_id") == pallet_id:
                    data = d
                    break
        if data:
            self.update_details(data)

    def update_details(self, data):
        for label, widget in self.ui.detail_fields.items():
            key = label.strip(":").lower().replace(" / ", "_").replace(" ", "_")
            widget.setText(str(data.get(key, "")))
