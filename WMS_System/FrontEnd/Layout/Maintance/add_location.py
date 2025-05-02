from PyQt5 import QtWidgets
import requests
from Layout.UI_PY.AddLocation import Ui_AddLocation  # Ajusta si tu path es distinto
from functools import partial

class AddLocationDialog(Ui_AddLocation):
    def __init__(self, api_client = None ,parent=None):
        super().__init__(parent)
        self.api_client = api_client

        self.saved = False 

        self.uppercase_fields = [
            self.lineEdit_Location,
            self.lineEdit_ScanLocation,
            self.lineEdit_Aisle,
            self.lineEdit_Bay,
            self.lineEdit_Level,
            self.lineEdit_Slot,
            self.lineEdit_PnD1,
            self.lineEdit_PnD2,
        ]

        # Conecta todos al validador de mayúsculas
        for field in self.uppercase_fields:
            field.textChanged.connect(partial(self.force_uppercase, field))

        self.setWindowTitle("Create New Location")
        self.load_location_classes()
        self.load_uom_dropdowns()


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
                self.comboBox_LocationType.addItem(lt["location_type"]), # add a new location and update the UOM for more clarity
                
            for p in proximities:
                self.comboBox_ProxIN.addItem(p["proximity"])
                self.comboBox_ProxOUT.addItem(p["proximity"])

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not connect to server: {e}")

    def force_uppercase(self, field, text):
        upper = text.upper()
        if text != upper:
            cursor_pos = field.cursorPosition()
            field.setText(upper)
            field.setCursorPosition(cursor_pos)


    def load_uom_dropdowns(self):
        uom_options = ["IN", "FEET", "CM"]
        uom_weight_options = ["LBS", "KGS"]

        self.comboBox_HeightUOM.clear()
        self.comboBox_WidthUOM.clear()
        self.comboBox_DepthUOM.clear()
        self.comboBox_WeightUOM.clear()

        self.comboBox_HeightUOM.addItems(uom_options)
        self.comboBox_WidthUOM.addItems(uom_options)
        self.comboBox_DepthUOM.addItems(uom_options)
        self.comboBox_WeightUOM.addItems(uom_weight_options)



    def save_new_location(self):

        def set_if_not_empty(field_dict, key, line_edit, cast_type=str):
            value = line_edit.text().strip()
            if value:
                try:
                    field_dict[key] = cast_type(value)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", f"{key} must be a {cast_type.__name__}")

        location_id = self.lineEdit_Location.text().strip()
        if not location_id:
            QtWidgets.QMessageBox.warning(self, "Missing Field", "Location ID is required.")
            return        

        data = {
            "location_id": location_id,
            "location_type": self.comboBox_LocationType.currentText(),
            "scan_location": self.lineEdit_ScanLocation.text().strip(),
            "black_hole_flag": "Y" if self.checkBox_BlackHole.isChecked() else "N",
            "has_assign_flag": "Y" if self.checkBox_Assigned.isChecked() else "N",
            "has_contents_flag": "Y" if self.checkBox_Content.isChecked() else "N",
            "has_pending_flag": "Y" if self.checkBox_Pending.isChecked() else "N",
            "putaway_class": self.comboBox_PutawayClass.currentText(),
            "pick_class": self.comboBox_PickClass.currentText(),
            "rstk_class": self.comboBox_RestockClass.currentText(),
            "blocked_code": self.comboBox_BlockCode.currentText().strip(),
            "proximity_in": self.comboBox_ProxIN.currentText().strip(),
            "proximity_out": self.comboBox_ProxOUT.currentText().strip(),
            "aisle": self.lineEdit_Aisle.text().strip(),
            "bay": self.lineEdit_Bay.text().strip(),
            "loc_level": self.lineEdit_Level.text().strip(),
            "slot": self.lineEdit_Slot.text().strip(),
            "pnd_location_id1": self.lineEdit_PnD1.text().strip(),
            "pnd_location_id2": self.lineEdit_PnD2.text().strip(),
            "uom_max_weight": self.comboBox_WeightUOM.currentText().strip(),
            "uom_max_height": self.comboBox_HeightUOM.currentText().strip(),
            "uom_max_width": self.comboBox_WidthUOM.currentText().strip(),
            "uom_max_depth": self.comboBox_DepthUOM.currentText().strip(),
            "uom_carton_cap": "",  # si tienes este valor, puedes mapearlo desde UI también
        }

        # Campos numéricos con validación
        set_if_not_empty(data, "palle_cap", self.lineEdit_PalletCap, int)
        set_if_not_empty(data, "carton_cap", self.lineEdit_CartonCap, int)
        set_if_not_empty(data, "max_weight", self.lineEdit_MaxWeight, float)
        set_if_not_empty(data, "max_height", self.lineEdit_MaxHeight, float)
        set_if_not_empty(data, "max_width", self.lineEdit_MaxWidth, float)
        set_if_not_empty(data, "max_depth", self.lineEdit_MaxDepth, float)


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
            self.lineEdit_Aisle,
            self.lineEdit_Bay,
            self.lineEdit_Level,
            self.lineEdit_Slot,
            self.lineEdit_PnD1,
            self.lineEdit_PnD2,
            self.lineEdit_PalletCap,
            self.lineEdit_CartonCap,
            self.lineEdit_MaxHeight,
            self.lineEdit_MaxDepth,
            self.lineEdit_MaxWidth,
            self.lineEdit_MaxWeight,
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


