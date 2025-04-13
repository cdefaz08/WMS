from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_AdjustmentWindow import Ui_AdjustmentWindow
import requests
from datetime import datetime

class AdjustmentWindow(QtWidgets.QWidget):
    def __init__(self, adjustments_data=None, api_client=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AdjustmentWindow()
        self.ui.setupUi(self)
        self.ui.tree_widget.setAlternatingRowColors(True)
        self.ui.tree_widget.setRootIsDecorated(True)
        self.ui.tree_widget.setHeaderLabels(["PALLET ID", "ITEM CODE", "QTY"])
        self.ui.tree_widget.setColumnWidth(0, 100)
        self.ui.tree_widget.setColumnWidth(1, 200)
        self.ui.tree_widget.setColumnWidth(2, 60)

        self.api_client = api_client
        self.adjustments_data = adjustments_data or []

        self.ui.tree_widget.itemClicked.connect(self.on_item_selected)
        self.populate_tree()

    def populate_tree(self):
        self.ui.tree_widget.clear()
        pallets = {}

        for entry in self.adjustments_data:
            pallet_id = entry.get("pallet_id")

            if not pallet_id:
                # 👇 Create a single-level row directly when there's no pallet
                row = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
                row.setText(0, "")  # No Pallet ID
                row.setText(1, entry["item_id"])
                row.setText(2, str(entry["pieces_on_hand"]))
                row.setData(0, QtCore.Qt.UserRole, entry)
            else:
                # 👇 Use the regular parent-child tree structure for pallets
                if pallet_id not in pallets:
                    parent_item = QtWidgets.QTreeWidgetItem(self.ui.tree_widget)
                    parent_item.setText(0, pallet_id)
                    pallets[pallet_id] = parent_item

                child_item = QtWidgets.QTreeWidgetItem()
                child_item.setText(1, entry["item_id"])
                child_item.setText(2, str(entry["pieces_on_hand"]))
                child_item.setData(0, QtCore.Qt.UserRole, entry)

                pallets[pallet_id].addChild(child_item)

        #self.ui.tree_widget.expandAll()




    def on_item_selected(self, item, column):
        # Clear existing form layout
        while self.ui.formLayout.count():
            child = self.ui.formLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Fill details form
        for i in range(item.columnCount()):
            header = self.ui.tree_widget.headerItem().text(i)
            value = item.text(i)
            if value:
                label = QtWidgets.QLabel(header + ":")
                field = QtWidgets.QLineEdit(value)
                field.setReadOnly(True)
                self.ui.formLayout.addRow(label, field)


