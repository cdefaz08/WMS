from PyQt5 import QtWidgets, QtCore
import requests
from config import API_BASE_URL
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Layout.UI_PY.item_search_ui import Ui_ItemSearch

class ItemSearchWindow(QtWidgets.QDialog, Ui_ItemSearch):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


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
        self.tableViewItemSearch.verticalHeader().setVisible(False)
    
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
            response = requests.get(f"{API_BASE_URL}/items/")
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
                QStandardItem(f"$ {item.get('price', 0):,.2f}"),
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
        #self.tableViewItemSearch.resizeColumnsToContents()
        self.Records.setText(f"Records found: <b>{len(items)}</b>")
        self.tableViewItemSearch.setColumnWidth(0, 160)   # Item ID
        self.tableViewItemSearch.setColumnWidth(1, 200)   # Description
        self.tableViewItemSearch.setColumnWidth(2, 120)   # UPC
        self.tableViewItemSearch.setColumnWidth(3, 80)    # Price
        self.tableViewItemSearch.setColumnWidth(4, 80)    # Active
        self.tableViewItemSearch.setColumnWidth(5, 120)   # Item Class
        self.tableViewItemSearch.setColumnWidth(6, 130)   # Alt Item id1
        self.tableViewItemSearch.setColumnWidth(7, 130)   # Alt Item id2
        self.tableViewItemSearch.setColumnWidth(8, 130)   # Default CFG
        self.tableViewItemSearch.setColumnWidth(9, 100)   # Color
        self.tableViewItemSearch.setColumnWidth(10, 60)   # Size
        self.tableViewItemSearch.setColumnWidth(11, 100)  # Brand
        self.tableViewItemSearch.setColumnWidth(12, 100)  # Style
        self.tableViewItemSearch.horizontalHeader().setStretchLastSection(True)


    def clear_filters(self):
        # Limpiar todos los lineEdits
        self.lineEdit_itemCode.clear()
        self.lineEdit_UPC.clear()
        self.lineEdit_alt_item_id1.clear()
        self.lineEdit_alt_item_id2.clear()
        self.lineEdit_item_class.clear()
        self.lineEdit_Color.clear()
        self.lineEdit_size.clear()
        self.lineEdit_Brand.clear()

    def get_selected_item_id(self):
        if not self.tableViewItemSearch:
            return None

        selection_model = self.tableViewItemSearch.selectionModel()
        if not selection_model:
            return None

        indexes = selection_model.selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewItemSearch.model()
        row = indexes[0].row()

        return model.index(row, 0).data(QtCore.Qt.UserRole)

    def delete_selected_item(self):
        item_id = self.get_selected_item_id()
        if not item_id:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item to delete.")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this item?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        try:
            response = requests.delete(f"{API_BASE_URL}/items/{item_id}")
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Deleted", "Item successfully deleted.")
                self.search_items()  # Refresh table
            elif response.status_code == 404:
                QtWidgets.QMessageBox.warning(self, "Error", "Item not found.")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete item.\n{response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")



