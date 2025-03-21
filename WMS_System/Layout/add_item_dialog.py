from PyQt5 import QtWidgets, uic

class AddItemDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("../UI/add_item.ui", self)  # Load your .ui file

        # Reference UI Elements
        self.lineEdit_ItemCode = self.findChild(QtWidgets.QLineEdit, 'lineEdit_ItemCode')
        self.lineEdit_Price = self.findChild(QtWidgets.QLineEdit, 'lineEdit_Price')
        self.lineEdit_Active = self.findChild(QtWidgets.QLineEdit, 'lineEdit_Active')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')

        # Connect the buttons
        self.buttonBox.accepted.connect(self.submit_item)
        self.buttonBox.rejected.connect(self.reject)

    def submit_item(self):
        """Submit new item data."""
        item_code = self.lineEdit_ItemCode.text().strip()
        price = self.lineEdit_Price.text().strip()
        active_status = self.lineEdit_Active.text().strip()

        if not item_code or not price:
            QtWidgets.QMessageBox.warning(self, "Error", "Item Code and Price are required!")
            return

        self.item_data = {
            "item_id": item_code,
            "price": price,
            "active": active_status if active_status else "1"  # Default to active
        }

        self.accept()  # Close the dialog and return data

    def get_item_data(self):
        """Return the item data collected from the dialog."""
        return self.item_data
