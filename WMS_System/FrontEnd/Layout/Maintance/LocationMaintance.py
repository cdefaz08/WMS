from PyQt5 import QtWidgets
from Layout.UI_PY.LocationMaintance import Ui_LocationMaintance
import requests
from functools import partial

class LocationMaintance(Ui_LocationMaintance):
    def __init__(self,api_client = None, location_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.loadLocationClasesDropdown()
        self.load_uom_dropdowns() 
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


        self.original_data = location_data.copy() if location_data else {}
        if location_data:
            self.loadLocationData(location_data)

    def force_uppercase(self, field, text):
        upper = text.upper()
        if text != upper:
            cursor_pos = field.cursorPosition()
            field.setText(upper)
            field.setCursorPosition(cursor_pos)


    def loadLocationClasesDropdown(self):
        try:
            putaway_classes = self.api_client.get(f"/classes/putaway").json()
            restock_classes = self.api_client.get(f"/classes/restock").json()
            pick_classes = self.api_client.get(f"/classes/pick").json()
            location_type = self.api_client.get(f"/location-types").json()
            proximities = self.api_client.get(f"/proximities").json()


            self.comboBox_PutawayClass.clear()
            self.comboBox_RestockClass.clear()
            self.comboBox_PickClass.clear()
            self.comboBox_LocationType.clear()
            self.comboBox_ProxIN.clear()
            self.comboBox_ProxOUT.clear()

            for c in putaway_classes:
                self.comboBox_PutawayClass.addItem(c["class_name"], c["id"])

            for c in restock_classes:
                self.comboBox_RestockClass.addItem(c["class_name"], c["id"])

            for c in pick_classes:
                self.comboBox_PickClass.addItem(c["class_name"], c["id"])

            for lt in location_type:
                self.comboBox_LocationType.addItem(lt["location_type"])

            for p in proximities:
                self.comboBox_ProxIN.addItem(p["proximity"])
                self.comboBox_ProxOUT.addItem(p["proximity"])

        except Exception as e:
            print(f"Error loading dropdowns: {e}")

    def loadLocationData(self, location):
        self.lineEdit_Location.setText(location.get("location_id", ""))
        self.comboBox_LocationType.setCurrentText(location.get("location_type", ""))
        self.comboBox_PutawayClass.setCurrentText(location.get("putaway_class", ""))
        self.comboBox_PickClass.setCurrentText(location.get("pick_class", ""))
        self.comboBox_RestockClass.setCurrentText(location.get("rstk_class", ""))


        self.lineEdit_ScanLocation.setText(location.get("scan_location", ""))
        self.lineEdit_Aisle.setText(location.get("aisle", ""))
        self.lineEdit_Bay.setText(location.get("bay", ""))
        self.lineEdit_Level.setText(location.get("loc_level", ""))
        self.lineEdit_Slot.setText(location.get("slot", ""))

        self.comboBox_BlockCode.setCurrentText(location.get("blocked_code", ""))
        self.comboBox_ProxIN.setCurrentText(location.get("proximiti_in", ""))
        self.comboBox_ProxOUT.setCurrentText(location.get("proximiti_out", ""))

        self.lineEdit_PnD1.setText(location.get("pnd_location_id1", ""))
        self.lineEdit_PnD2.setText(location.get("pnd_location_id2", ""))

        self.lineEdit_PalletCap.setText(str(location.get("palle_cap", "")))
        self.lineEdit_CartonCap.setText(str(location.get("carton_cap", "")))

        self.lineEdit_MaxHeight.setText(str(location.get("max_height", "")))
        self.lineEdit_MaxDepth.setText(str(location.get("max_depth", "")))
        self.lineEdit_MaxWidth.setText(str(location.get("max_width", "")))
        self.lineEdit_MaxWeight.setText(str(location.get("max_weight", "")))

        self.comboBox_HeightUOM.setCurrentText(location.get("uom_max_height", ""))
        self.comboBox_DepthUOM.setCurrentText(location.get("uom_max_depth", ""))
        self.comboBox_WidthUOM.setCurrentText(location.get("uom_max_width", ""))
        self.comboBox_WeightUOM.setCurrentText(location.get("uom_max_weight", ""))

        def to_bool(value):
            return str(value).strip().upper() in ["Y", "YES", "TRUE", "1"]

        self.checkBox_BlackHole.setChecked(to_bool(location.get("black_hole_flag")))

        self.lineEdit_PalletsQty.setText(str(location.get("pallet_qty_act", "")))
        self.lineEdit_CartonsQty.setText(str(location.get("carton_qty_act", "")))

        self.lineEdit_LastTouched.setText(location.get("last_touch", ""))
        self.comboBox_HeightUOM.setCurrentText(location.get("uom_max_height", ""))
        self.comboBox_DepthUOM.setCurrentText(location.get("uom_max_depth", ""))
        self.comboBox_WidthUOM.setCurrentText(location.get("uom_max_width", ""))
        self.comboBox_WeightUOM.setCurrentText(location.get("uom_max_weight", ""))

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

    def get_updated_fields(self):
        updated = {}

        def check(field, widget, type_cast=str):
            current_raw = widget.text().strip()
            original_raw = self.original_data.get(field, "")

            current = str(current_raw)
            original = str(original_raw)

            if current != original:
                if not current: return
                try:
                    updated[field] = type_cast(current_raw)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Error", f"{field} must be a {type_cast.__name__}")


        # LineEdits
        check("location_id", self.lineEdit_Location)
        check("scan_location", self.lineEdit_ScanLocation)
        check("aisle", self.lineEdit_Aisle)
        check("bay", self.lineEdit_Bay)
        check("loc_level", self.lineEdit_Level)
        check("slot", self.lineEdit_Slot)
        check("pnd_location_id1", self.lineEdit_PnD1)
        check("pnd_location_id2", self.lineEdit_PnD2)

        check("palle_cap", self.lineEdit_PalletCap, int)
        check("carton_cap", self.lineEdit_CartonCap, int)
        check("max_height", self.lineEdit_MaxHeight, float)
        check("max_depth", self.lineEdit_MaxDepth, float)
        check("max_width", self.lineEdit_MaxWidth, float)
        check("max_weight", self.lineEdit_MaxWeight, float)
        check("pallet_qty_act", self.lineEdit_PalletsQty, int)
        check("carton_qty_act", self.lineEdit_CartonsQty, int)

        check("last_touch", self.lineEdit_LastTouched)

        # Combos
        combos = {
            "location_type": self.comboBox_LocationType,
            "putaway_class": self.comboBox_PutawayClass,
            "pick_class": self.comboBox_PickClass,
            "rstk_class": self.comboBox_RestockClass,
            "blocked_code": self.comboBox_BlockCode,
            "proximiti_in": self.comboBox_ProxIN,
            "proximiti_out": self.comboBox_ProxOUT,
            "uom_max_height": self.comboBox_HeightUOM,
            "uom_max_depth": self.comboBox_DepthUOM,
            "uom_max_width": self.comboBox_WidthUOM,
            "uom_max_weight": self.comboBox_WeightUOM,
        }

        for field, combo in combos.items():
            current = combo.currentText().strip()
            original = str(self.original_data.get(field, "")).strip()
            if current != original:
                updated[field] = current


        # Black hole flag only (others are managed by system)
        def check_flag(field, checkbox):
            current = "Y" if checkbox.isChecked() else "N"
            original = str(self.original_data.get(field, "N")).strip().upper()
            if current != original:
                updated[field] = current

        check_flag("black_hole_flag", self.checkBox_BlackHole)

        return updated

    def save_changes(self):
        updated_fields = self.get_updated_fields()
        if not updated_fields:
            QtWidgets.QMessageBox.information(self, "No changes", "No fields were modified.")
            return

        location_id = self.original_data.get("location_id")
        try:
            response = self.api_client.put(f"/locations/{location_id}", json=updated_fields)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Location updated successfully.")
                self.original_data = self.original_data | updated_fields
                self.loadLocationData(self.original_data)  # <-- Force UI reload here ✅
            if hasattr(self, "parent_subwindow") and self.parent_subwindow:
                self.parent_subwindow.close()
            else:
                self.close() 
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update location: {response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")

        print(f"Updated fields for Location ID {location_id}: {updated_fields}")

    def closeEvent(self, event):
        updated_fields = self.get_updated_fields()
        if updated_fields:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you really want to close?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                event.ignore()
                return
        event.accept()

