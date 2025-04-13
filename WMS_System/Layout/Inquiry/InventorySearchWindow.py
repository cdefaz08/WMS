from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.UI_InventorySearch import Ui_InventorySearch

class InventorySearchWindow(QtWidgets.QDialog, Ui_InventorySearch):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client


        self.pushButton_Search.clicked.connect(self.search_inventory)
        self.tableView_aContents.verticalHeader().setVisible(False)
        self.tableView_aContents.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_aContents.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def search_inventory(self):
        # Collect filter inputs
        filters = {
            "location_id": self.lineEdit_Location.text().strip(),
            "pallet_id": self.lineEdit_Pallet.text().strip(),
            "item_code": self.lineEdit_ItemCode.text().strip(),
            "receipt_info": self.lineEdit_Receipt.text().strip(),
            "receipt_release_num": self.lineEdit_Realese.text().strip(),
        }

        # Remove empty filters
        filters = {key: value for key, value in filters.items() if value}

        try:
            response = self.api_client.get("/a-contents/", params=filters)
            if response.status_code == 200:
                data = response.json()
                self.Records.setText(f"Records: {len(data)}")
                self.populate_table(data)  # ✅ Always call even if data is []
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to fetch inventory.")
                self.populate_table([])  # ✅ Still call to reset/clear table view
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not connect to server.\n{e}")
            self.populate_table([])  # ✅ Ensure table headers still render


    def populate_table(self, data):
        header_mapping = {
            "id": "id",
            "Location": "location_id",
            "Pallet": "pallet_id",
            "Item Code": "item_id",
            "Pieces On Hand": "pieces_on_hand",
            "Receipt": "receipt_info",
            "Release": "receipt_release_num",
            "Date Last Touched": "date_time_last_touched",
            "User Last Touched": "user_last_touched",
        }

        headers = list(header_mapping.keys())

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row in data:
            items = []
            for label in headers:
                key = header_mapping[label]
                value = row.get(key, "")
                if value is None:
                    value = ""
                items.append(QStandardItem(str(value)))
            model.appendRow(items)

        self.tableView_aContents.setModel(model)
        self.Records.setText(f"Records found: <b>{len(data)}</b>")

        # Hide ID column
        self.tableView_aContents.setColumnHidden(0, True)

        # Column widths
        self.tableView_aContents.setColumnWidth(1, 120)
        self.tableView_aContents.setColumnWidth(2, 120)
        self.tableView_aContents.setColumnWidth(3, 150)
        self.tableView_aContents.setColumnWidth(4, 150)
        self.tableView_aContents.setColumnWidth(5, 200)
        self.tableView_aContents.setColumnWidth(6, 150)
        self.tableView_aContents.setColumnWidth(7, 210)
        self.tableView_aContents.setColumnWidth(8, 210)

    def get_selected_location_id(self):
        selected_indexes = self.tableView_aContents.selectionModel().selectedRows()
        if selected_indexes:
            # Row index
            selected_row = selected_indexes[0].row()
            # Column 1 is location_id based on your headers list
            model = self.tableView_aContents.model()
            location_index = model.index(selected_row, 1)
            location_id = model.data(location_index)
            return location_id
        return None