from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.UI_InventorySearch import Ui_InventorySearch

class InventorySearchWindow(QtWidgets.QDialog, Ui_InventorySearch):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client

        self.pushButton_Search.clicked.connect(self.search_inventory)

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
        headers = [
            "id", "Location", "Pallet", "Item Code", "Pieces On Hand",
            "Receipt", "Release", "Date Last Touched", "User Last Touched"
        ]

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row in data:
            items = [QStandardItem(str(row.get(h, ""))) for h in headers]
            model.appendRow(items)

        # Set model and record label
        self.tableView_aContents.setModel(model)
        self.Records.setText(f"Records found: <b>{len(data)}</b>")

        # Hide ID column
        self.tableView_aContents.setColumnHidden(0, True)

        # Manually set column widths
        self.tableView_aContents.setColumnWidth(1, 120)  # location_id
        self.tableView_aContents.setColumnWidth(2, 120)  # pallet_id
        self.tableView_aContents.setColumnWidth(3, 150)  # item_code
        self.tableView_aContents.setColumnWidth(4, 150)  # pieces_on_hand
        self.tableView_aContents.setColumnWidth(5, 200)  # receipt_info
        self.tableView_aContents.setColumnWidth(6, 150)  # receipt_release_num
        self.tableView_aContents.setColumnWidth(7, 210)  # date_time_last_touched
        self.tableView_aContents.setColumnWidth(8, 210)  # user_last_touched

        # (Optional) Only if you want to stretch the last column
        # self.tableView_aContents.horizontalHeader().setStretchLastSection(True)
