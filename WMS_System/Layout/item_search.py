from PyQt5 import QtWidgets, uic, QtCore 
from add_item_dialog import AddItemDialog
import requests
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ItemSearchWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/item_searchV2.ui", self)

        self.lineEdit_itemCode = self.findChild(QtWidgets.QLineEdit,"lineEdit_itemCode")
        self.lineEdit_UPC = self.findChild(QtWidgets.QLineEdit,"lineEdit_UPC")
        self.lineEdit_alt_item_id1 = self.findChild(QtWidgets.QLineEdit,"lineEdit_alt_item_id1")
        self.lineEdit_alt_item_id2 = self.findChild(QtWidgets.QLineEdit,"lineEdit_alt_item_id2")
        self.lineEdit_item_class = self.findChild(QtWidgets.QLineEdit,"lineEdit_item_class")
        self.lineEdit_Color = self.findChild(QtWidgets.QLineEdit,"lineEdit_Color")
        self.lineEdit_size = self.findChild(QtWidgets.QLineEdit,"lineEdit_size")
        self.lineEdit_Brand = self.findChild(QtWidgets.QLineEdit,"lineEdit_Brand")
        self.pushButton_Search = self.findChild(QtWidgets.QPushButton, 'pushButton_Search')
        self.tableViewItemSearch = self.findChild(QtWidgets.QTableView,"tableViewItemSearch")

        # Connect ENTER key (returnPressed) from all search fields
        self.lineEdit_itemCode.returnPressed.connect(self.search_items)
        self.lineEdit_UPC.returnPressed.connect(self.search_items)
        self.lineEdit_alt_item_id1.returnPressed.connect(self.search_items)
        self.lineEdit_alt_item_id2.returnPressed.connect(self.search_items)
        self.lineEdit_item_class.returnPressed.connect(self.search_items)
        self.lineEdit_Color.returnPressed.connect(self.search_items)
        self.lineEdit_size.returnPressed.connect(self.search_items)
        self.lineEdit_Brand.returnPressed.connect(self.search_items)
        self.lineEdit_UPC.returnPressed.connect(self.search_items)

        self.pushButton_Search.clicked.connect(self.search_items)

        self.tableViewItemSearch.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableViewItemSearch.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    
    def search_items(self):
        # Leer y normalizar los campos de búsqueda
        search_data = {
            "item_id": self.lineEdit_itemCode.text().strip().lower(),
            "upc": self.lineEdit_UPC.text().strip(),
            "alt_item_id1": self.lineEdit_alt_item_id1.text().strip().lower(),
            "alt_item_id2": self.lineEdit_alt_item_id2.text().strip().lower(),
            "item_class": self.lineEdit_item_class.text().strip().lower(),
            "color": self.lineEdit_Color.text().strip().lower(),
            "size": self.lineEdit_size.text().strip().lower(),
            "brand": self.lineEdit_Brand.text().strip().lower()
        }

        try:
            response = requests.get("http://localhost:8000/items/")
            if response.status_code == 200:
                items = response.json()

                # Si todos los campos están vacíos, mostrar todos los ítems
                if not any(search_data.values()):
                    self.populate_table(items)
                    return

                # Si hay filtros, aplicar búsqueda parcial
                filtered = []
                for item in items:
                    match = True
                    for key, value in search_data.items():
                        if value:  # solo filtrar si se escribió algo
                            item_value = str(item.get(key, "")).lower()
                            if value not in item_value:
                                match = False
                                break
                    if match:
                        filtered.append(item)

                self.populate_table(filtered)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to load items")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server")


    def populate_table(self, items):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Item ID", "Description", "UPC", "Price", "Active",
            "Item Class", "Alt Item id1", "Alt Item id2",
            "Default CFG", "Color", "Size", "Brand", "Style"
        ])

        for item in items:
            # Crea el QStandardItem del item_id visible
            item_id_item = QStandardItem(str(item.get("item_id", "")))

            # Guarda el ID real del backend (oculto) en UserRole
            item_id_item.setData(str(item.get("id", "")), QtCore.Qt.UserRole)

            # Resto de columnas visibles
            row = [
                item_id_item,
                QStandardItem(str(item.get("description", ""))),
                QStandardItem(str(item.get("upc", ""))),
                QStandardItem(str(item.get("price", ""))),
                QStandardItem("Yes" if item.get("is_offer") else "No"),
                QStandardItem(str(item.get("item_class", ""))),
                QStandardItem(str(item.get("alt_item_id1", ""))),
                QStandardItem(str(item.get("alt_item_id2", ""))),
                QStandardItem(str(item.get("default_cfg", ""))),
                QStandardItem(str(item.get("color", ""))),
                QStandardItem(str(item.get("size", ""))),
                QStandardItem(str(item.get("brand", ""))),
                QStandardItem(str(item.get("style", ""))),
            ]
            model.appendRow(row)

        self.tableViewItemSearch.setModel(model)


    def open_add_item_dialog(self):
        """Open the Add Item Dialog when the 'Add New' button is clicked."""
        dialog = AddItemDialog()
        if dialog.exec_():  # If accepted
            item_data = dialog.get_item_data()
            self.createItem(item_data)  # ✅ Separate method to handle data insertion


    def createItem(self, item_data):
        """Send the new item to FastAPI and refresh the table."""
        try:
            response = requests.post("http://localhost:8000/items/", json=item_data)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "New item added successfully!")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to add item.")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to the server.")

    def get_selected_item_id(self):
        indexes = self.tableViewItemSearch.selectionModel().selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewItemSearch.model()
        row = indexes[0].row()
        return model.index(row, 0).data(QtCore.Qt.UserRole)



