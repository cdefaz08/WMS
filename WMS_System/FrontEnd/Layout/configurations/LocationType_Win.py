from PyQt5 import QtWidgets, uic, QtCore 
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class LocationTypes(QtWidgets.QWidget):
    def __init__(self,api_client = None,parent = None):
        super().__init__(parent)
        uic.loadUi("UI/locationTypes.ui", self)
        self.api_client = api_client
        self.tableViewLocationTypes = self.findChild(QtWidgets.QTableView , "tableViewLocationTypes")
        self.tableViewLocationTypes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableViewLocationTypes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewLocationTypes.verticalHeader().setVisible(False)
        self.load_location_types()

    def load_location_types(self):
        try:
            response = self.api_client.get(f"/location-types")
            if response.status_code == 200:
                data = response.json()

                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(["Location Type", "Description"])

                for item in data:
                    location_type = QStandardItem(item.get("location_type", ""))
                    description = QStandardItem(item.get("description", ""))
                    model.appendRow([location_type, description])

                self.tableViewLocationTypes.setModel(model)
                self.tableViewLocationTypes.resizeColumnsToContents()
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "API response failed")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
        
        self.tableViewLocationTypes.horizontalHeader().setStretchLastSection(True)

    def get_selected_item_id(self):
        if not self.tableViewLocationTypes:
            return None

        selection_model = self.tableViewLocationTypes.selectionModel()
        if not selection_model:
            return None

        indexes = selection_model.selectedIndexes()
        if not indexes:
            return None

        model = self.tableViewLocationTypes.model()
        row = indexes[0].row()

        return model.index(row, 0).data(QtCore.Qt.DisplayRole)


    