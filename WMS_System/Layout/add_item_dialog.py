from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from config import API_BASE_URL
import requests

class AddItemDialog(QtWidgets.QWidget):
    def __init__(self,api_client = None, parent= None):
        super().__init__()
        uic.loadUi("UI/add_item.ui", self)  # Load your .ui file
        self.api_client = api_client
        self.item_data = None

        # Reference UI Elements
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

        self.comboBox_active.addItems(["Yes","No"])
        self.lineEdit_Price.setValidator(QDoubleValidator(0.0, 99999.99, 2))

        
        self.populate_item_classes()




    def populate_item_classes(self):
        try:
            response = requests.get(f"{API_BASE_URL}/item-classes/")
            if response.status_code == 200:
                item_classes = response.json()
                self.comboBox_item_class.clear()

                for ic in item_classes:
                    name = ic["item_class"]           # visible name (item_class_id)
                    item_id = ic["id"]                # internal id
                    self.comboBox_item_class.addItem(name, item_id)

            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load item classes.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"API Error:\n{e}")



    def submit_item(self):
        """Submit new item data."""
        item_code = self.lineEdit_ItemCode.text().strip()
        description = self.lineEdit_description.text().strip()
        price_text = self.lineEdit_Price.text().strip()
        active_status = self.comboBox_active.currentText()
        color = self.lineEdit_Color.text().strip()
        size = self.lineEdit_Size.text().strip()
        upc = self.lineEdit_UPC.text().strip()
        item_class = self.comboBox_item_class.currentText()
        default_cfg = self.lineEdit_default_cfg.text().strip()
        alt_itemid1 = self.lineEdit_alt_item_id_1.text().strip()
        alt_itemid2 = self.lineEdit_alt_item_id_2.text().strip()
        brand = self.lineEdit_Brand.text().strip()
        style = self.lineEdit_Style.text().strip()
        description2 = self.lineEdit_Description2.text().strip()
        custum1 = self.lineEdit_Custom1.text().strip()
        custum2 = self.lineEdit_Custom2.text().strip()
        custum3 = self.lineEdit_Custom3.text().strip()
        custum4 = self.lineEdit_Custom4.text().strip()
        custum5 = self.lineEdit_Custom5.text().strip()
        custum6 = self.lineEdit_Custom6.text().strip()

        if not item_code or not price_text:
            QtWidgets.QMessageBox.warning(self, "Error", "Item Code and Price are required!")
            return

        try:
            price = float(price_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the price.")
            return

        self.item_data = {
            "item_id": item_code,
            "description": description,
            "color": color,
            "size": size,
            "price": price,
            "upc": int(upc) if upc.isdigit() else 0,
            "item_class": item_class,
            "is_offer": active_status.strip().lower() == "yes",
            "default_cfg": default_cfg,
            "alt_item_id1": int(alt_itemid1) if alt_itemid1.isdigit() else None,
            "alt_item_id2": int(alt_itemid2) if alt_itemid2.isdigit() else None,
            "brand": brand,
            "style": style,
            "description2": description2,
            "custum1": custum1,
            "custum2": custum2,
            "custum3": custum3,
            "custum4": custum4,
            "custum5": custum5,
            "custum6": custum6
        }


    def createItem(self):
        self.submit_item()
        if self.item_data:
            try:
                response = requests.post(f"{API_BASE_URL}/items/", json=self.item_data)
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "New item added successfully!")
                    # Intenta cerrar el subwindow si existe
                    mdi = self.parent()
                    while mdi and not isinstance(mdi, QtWidgets.QMdiSubWindow):
                        mdi = mdi.parent()
                    if mdi:
                        mdi.close()
                    else:
                        self.close()  
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to add item.\n{response.text}")
            except requests.exceptions.RequestException:
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")



    def get_item_data(self):
        """Return the item data collected from the dialog."""
        return self.item_data
    