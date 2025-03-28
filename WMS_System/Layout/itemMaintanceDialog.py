from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
import requests
from UI_PY.ItemMaintance import Ui_UpdateItemCode

class ItemMaintanceDialog(QtWidgets.QDialog,Ui_UpdateItemCode):
    item_updated = pyqtSignal()
    def __init__(self, item_data = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.comboBox_active.addItems(["Yes", "No"])

        if item_data:
            self.load_item_class_dropdown()
            self.load_item_data(item_data)

        self.original_data = item_data.copy()




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

    def get_updated_fields(self):
        updated = {}

        def check(field_name, widget, convert=str):
            current_value = convert(widget.text()).strip()
            original_value = str(self.original_data.get(field_name, "")).strip()
            if current_value != original_value:
                updated[field_name] = current_value

        check("item_id", self.lineEdit_ItemCode)
        check("description", self.lineEdit_description)
        check("upc", self.lineEdit_UPC)
        check("price", self.lineEdit_Price)
        check("alt_item_id1", self.lineEdit_alt_item_id_1)
        check("alt_item_id2", self.lineEdit_alt_item_id_2)
        check("default_cfg", self.lineEdit_default_cfg)
        check("color", self.lineEdit_Color)
        check("size", self.lineEdit_Size)
        check("brand", self.lineEdit_Brand)
        check("style", self.lineEdit_Style)
        check("description2", self.lineEdit_Description2)
        check("custom1", self.lineEdit_Custom1)
        check("custom2", self.lineEdit_Custom2)
        check("custom3", self.lineEdit_Custom3)
        check("custom4", self.lineEdit_Custom4)
        check("custom5", self.lineEdit_Custom5)
        check("custom6", self.lineEdit_Custom6)

        # ComboBox item_class
        current_class = self.comboBox_item_class.currentText().strip()
        if current_class != str(self.original_data.get("item_class", "")).strip():
            updated["item_class"] = current_class

        # ComboBox is_offer
        current_offer = self.comboBox_active.currentText().strip()
        original_offer = "Yes" if self.original_data.get("is_offer") else "No"
        if current_offer != original_offer:
            updated["is_offer"] = True if current_offer == "Yes" else False

        return updated

    def save_changes(self):
        updated_fields = self.get_updated_fields()
        if not updated_fields:
            QtWidgets.QMessageBox.information(self, "No changes", "No fields were modified.")
            return

        item_id = self.original_data["id"]
        try:
            response = requests.put(f"http://localhost:8000/items/{item_id}", json=updated_fields)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Item updated successfully.")
                if hasattr(self, 'subwindow'):
                    self.subwindow.close()
                self.accept()
                self.item_updated.emit()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update item: {response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to server")


