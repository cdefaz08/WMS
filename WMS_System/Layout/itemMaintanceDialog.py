from PyQt5 import QtWidgets, uic
import requests

class ItemMaintanceDialog(QtWidgets.QDialog):
    def __init__(self, item_data = None, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/ItemMaintance.ui", self)

        self.lineEdit_ItemCode = self.findChild(QtWidgets.QLineEdit, 'lineEdit_ItemCode')
        self.lineEdit_Price = self.findChild(QtWidgets.QLineEdit, 'lineEdit_Price')
        self.comboBox_active = self.findChild(QtWidgets.QComboBox, 'comboBox_active')
        self.lineEdit_description = self.findChild(QtWidgets.QLineEdit, 'lineEdit_description')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        self.comboBox_item_class = self.findChild(QtWidgets.QComboBox,'comboBox_item_class')
        self.lineEdit_UPC = self.findChild(QtWidgets.QLineEdit,'lineEdit_UPC')
        self.lineEdit_alt_item_id_1 = self.findChild(QtWidgets.QLineEdit,'lineEdit_alt_item_id_1')
        self.lineEdit_alt_item_id_2 = self.findChild(QtWidgets.QLineEdit,'lineEdit_alt_item_id_2')
        self.lineEdit_Color = self.findChild(QtWidgets.QLineEdit,'lineEdit_Color')
        self.lineEdit_Size = self.findChild(QtWidgets.QLineEdit,'lineEdit_Size')
        self.lineEdit_Description2 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Description2')
        self.lineEdit_Brand = self.findChild(QtWidgets.QLineEdit,'lineEdit_Brand')
        self.lineEdit_Style = self.findChild(QtWidgets.QLineEdit,'lineEdit_Style')
        self.lineEdit_Custom1 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom1')
        self.lineEdit_Custom2 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom2')
        self.lineEdit_Custom3 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom3')
        self.lineEdit_Custom4 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom4')
        self.lineEdit_Custom5 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom5')
        self.lineEdit_Custom6 = self.findChild(QtWidgets.QLineEdit,'lineEdit_Custom6')
        self.lineEdit_default_cfg = self.findChild(QtWidgets.QLineEdit,'lineEdit_default_cfg')

        self.comboBox_active = self.findChild(QtWidgets.QComboBox, 'comboBox_active')
        self.comboBox_active.addItems(["Yes", "No"])


        self.comboBox_item_class = self.findChild(QtWidgets.QComboBox,'comboBox_item_class')


        if item_data:
            self.load_item_class_dropdown()
            self.load_item_data(item_data)




    def load_item_data(self, item):
        self.lineEdit_ItemCode.setText(item.get("item_id", ""))
        self.lineEdit_description.setText(item.get("description", ""))
        self.lineEdit_UPC.setText(str(item.get("upc", "")))
        self.lineEdit_Price.setText(str(item.get("price", "")))

        is_offer = item.get("is_offer")
        self.comboBox_active.setCurrentText("Yes" if is_offer else "No")

        item_class = item.get("item_class")
        if item_class:
            self.comboBox_item_class.setCurrentText(item_class)

        self.lineEdit_alt_item_id_1.setText(str(item.get("alt_item_id1", "")))
        self.lineEdit_alt_item_id_2.setText(str(item.get("alt_item_id2", "")))

        self.lineEdit_Color.setText(str(item.get("color", "")))
        self.lineEdit_Size.setText(str(item.get("size", "")))
        self.lineEdit_Brand.setText(str(item.get("brand", "")))
        self.lineEdit_Style.setText(str(item.get("style", "")))
        self.lineEdit_Description2.setText(str(item.get("description2", "")))
        self.lineEdit_default_cfg.setText(str(item.get("default_cfg", "")))

        self.lineEdit_Custom1.setText(str(item.get("custom1", "")))
        self.lineEdit_Custom2.setText(str(item.get("custom2", "")))
        self.lineEdit_Custom3.setText(str(item.get("custom3", "")))
        self.lineEdit_Custom4.setText(str(item.get("custom4", "")))
        self.lineEdit_Custom5.setText(str(item.get("custom5", "")))
        self.lineEdit_Custom6.setText(str(item.get("custom6", "")))



    def load_item_class_dropdown(self):
        try:
            response = requests.get("http://localhost:8000/item-classes/")
            if response.status_code == 200:
                item_classes = response.json()
                self.comboBox_item_class.clear()
                for item in item_classes:
                    self.comboBox_item_class.addItem(item["item_class"])
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load item classes.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to server for item classes.")

