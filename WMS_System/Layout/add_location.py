from PyQt5 import QtWidgets
import requests
from Layout.UI_PY.AddLocation import Ui_AddLocation  # Ajusta si tu path es distinto
from config import API_BASE_URL

class AddLocationDialog(QtWidgets.QWidget, Ui_AddLocation):
    def __init__(self,api_client = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client

        self.saved = False 

        self.setWindowTitle("Create New Location")
        self.load_location_classes()


    def load_location_classes(self):
        try:
            putaway = self.api_client.get(f"/classes/putaway").json()
            restock = self.api_client.get(f"/classes/restock").json()
            pick = self.api_client.get(f"/classes/pick").json()
            location_type = self.api_client.get(f"/location-types").json()
            proximities = self.api_client.get(f"/proximities").json()

            self.comboBox_PutawayClass.clear()
            self.comboBox_RestockClass.clear()
            self.comboBox_PickClass.clear()
            self.comboBox_LocationType.clear()

            for c in putaway:
                self.comboBox_PutawayClass.addItem(c["class_name"])

            for c in restock:
                self.comboBox_RestockClass.addItem(c["class_name"])

            for c in pick:
                self.comboBox_PickClass.addItem(c["class_name"])

            for lt in location_type:
                self.comboBox_LocationType.addItem(lt["location_type"])
                
            for p in proximities:
                self.comboBox_PrxIN.addItem(p["proximity"])
                self.comboBox_PrxOUT.addItem(p["proximity"])

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not connect to server: {e}")

    def save_new_location(self):
        def set_if_not_empty(field_dict, key, line_edit, cast_type=str):
            value = line_edit.text().strip()
            if value:
                try:
                    field_dict[key] = cast_type(value)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", f"{key} must be a {cast_type.__name__}")

        location_id = self.lineEdit_Location.text().strip()

        data = {
            "location_id": location_id,
            "location_type": self.comboBox_LocationType.currentText(),
            "scan_location": self.lineEdit_ScanLocation.text().strip(),
            "black_hole_flag": "Y" if self.checkBox_BlackHoleFlag.isChecked() else "N",
            "has_assign_flag": "Y" if self.checkBox_HasAssignedFlag.isChecked() else "N",
            "has_contents_flag": "Y" if self.checkBox_HasContentFlag.isChecked() else "N",
            "has_pending_flag": "Y" if self.checkBox_HasPendingFlag.isChecked() else "N",
            "putaway_class": self.comboBox_PutawayClass.currentText(),
            "pick_class": self.comboBox_PickClass.currentText(),
            "rstk_class": self.comboBox_RestockClass.currentText(),
            "blocked_code": self.comboBox_BlockCode.currentText().strip(),
            "proximity_in": self.comboBox_PrxIN.currentText().strip(),
            "proximity_out": self.comboBox_PrxOUT.currentText().strip(),
            "aisle": self.lineEdit_Aisel.text().strip(),
            "bay": self.lineEdit_Bay.text().strip(),
            "loc_level": self.lineEdit_Level.text().strip(),
            "slot": self.lineEdit_Slot.text().strip(),
            "pnd_location_id1": self.lineEdit_PnDIN.text().strip(),
            "pnd_location_id2": self.lineEdit_PnDOUT.text().strip(),
            "uom_max_weight": self.comboBox_WeightUOM.currentText().strip(),
            "uom_max_height": self.comboBox_HeightUOM.currentText().strip(),
            "uom_max_width": self.comboBox_WidthUOM.currentText().strip(),
            "uom_max_depth": self.comboBox_DepthUOM.currentText().strip(),
            "uom_carton_cap": "",  # si tienes este valor, puedes mapearlo desde UI también
        }

        # Campos numéricos con validación
        set_if_not_empty(data, "palle_cap", self.lineEdit_PallCap, int)
        set_if_not_empty(data, "carton_cap", self.lineEdit_CartCap, int)
        set_if_not_empty(data, "max_weight", self.lineEdit_MaxWwightValue, float)
        set_if_not_empty(data, "max_height", self.lineEdit_MaxHeightValue, float)
        set_if_not_empty(data, "max_width", self.lineEdit_MaxWidthValue, float)
        set_if_not_empty(data, "max_depth", self.lineEdit_MaxDepthValue, float)


        try:
            response = self.api_client.post(f"/locations/", json=data)
            if response.status_code == 200:
                self.saved = True
                QtWidgets.QMessageBox.information(self, "Success", "Location created successfully.")
                mdi = self.parent()
                while mdi and not isinstance(mdi, QtWidgets.QMdiSubWindow):
                    mdi = mdi.parent()
                if mdi:
                    mdi.close()
                else:
                    self.close()  
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to create location:\n{response.text}")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Connection Error", f"Could not connect to server:\n{e}")



    def closeEvent(self, event):
        if getattr(self, "saved", False):  # ✅ Ya fue guardado, no mostrar advertencia
            event.accept()
            return

        # Lista de campos de texto a revisar
        fields = [
            self.lineEdit_Location,
            self.lineEdit_ScanLocation,
            self.lineEdit_Aisel,
            self.lineEdit_Bay,
            self.lineEdit_Level,
            self.lineEdit_Slot,
            self.lineEdit_PnDIN,
            self.lineEdit_PnDOUT,
            self.lineEdit_PallCap,
            self.lineEdit_CartCap,
            self.lineEdit_MaxHeightValue,
            self.lineEdit_MaxDepthValue,
            self.lineEdit_MaxWidthValue,
            self.lineEdit_MaxWwightValue,
        ]

        has_unsaved_input = any(field.text().strip() for field in fields)

        if has_unsaved_input:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved data. Are you sure you want to close?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.No:
                event.ignore()
                return

        event.accept()


