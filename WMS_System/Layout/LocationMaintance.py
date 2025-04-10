from PyQt5 import QtWidgets
from Layout.UI_PY.LocationMaintance import Ui_LocationMaintance
import requests
from config import API_BASE_URL

class LocationMaintance(QtWidgets.QWidget, Ui_LocationMaintance):
    def __init__(self,api_client = None, location_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loadLocationClasesDropdown()
        self.api_client = api_client

        self.original_data = location_data.copy() if location_data else {}
        if location_data:
            self.loadLocationData(location_data)

    def loadLocationClasesDropdown(self):
        try:
            putaway_classes = requests.get(f"{API_BASE_URL}/classes/putaway").json()
            restock_classes = requests.get(f"{API_BASE_URL}/classes/restock").json()
            pick_classes = requests.get(f"{API_BASE_URL}/classes/pick").json()
            location_type = requests.get(f"{API_BASE_URL}/location-types").json()
            proximities = requests.get(f"{API_BASE_URL}/proximities").json()


            self.comboBox_PutawayClass.clear()
            self.comboBox_RestockClass.clear()
            self.comboBox_PickClass.clear()
            self.comboBox_LocationType.clear()
            self.comboBox_PrxIN.clear()
            self.comboBox_PrxOUT.clear()

            for c in putaway_classes:
                self.comboBox_PutawayClass.addItem(c["class_name"], c["id"])

            for c in restock_classes:
                self.comboBox_RestockClass.addItem(c["class_name"], c["id"])

            for c in pick_classes:
                self.comboBox_PickClass.addItem(c["class_name"], c["id"])

            for lt in location_type:
                self.comboBox_LocationType.addItem(lt["location_type"])

            for p in proximities:
                self.comboBox_PrxIN.addItem(p["proximity"])
                self.comboBox_PrxOUT.addItem(p["proximity"])

        except Exception as e:
            print(f"Error loading dropdowns: {e}")

    def loadLocationData(self, location):
        self.lineEdit_Location.setText(location.get("location_id", ""))
        self.comboBox_LocationType.setCurrentText(location.get("location_type", ""))
        self.comboBox_PutawayClass.setCurrentText(location.get("putaway_class", ""))
        self.comboBox_PickClass.setCurrentText(location.get("pick_class", ""))
        self.comboBox_RestockClass.setCurrentText(location.get("rstk_class", ""))


        self.lineEdit_ScanLocation.setText(location.get("scan_location", ""))
        self.lineEdit_Aisel.setText(location.get("aisle", ""))
        self.lineEdit_Bay.setText(location.get("bay", ""))
        self.lineEdit_Level.setText(location.get("loc_level", ""))
        self.lineEdit_Slot.setText(location.get("slot", ""))

        self.comboBox_BlockCode.setCurrentText(location.get("blocked_code", ""))
        self.comboBox_PrxIN.setCurrentText(location.get("proximiti_in", ""))
        self.comboBox_PrxOUT.setCurrentText(location.get("proximiti_out", ""))

        self.lineEdit_PnDIN.setText(location.get("pnd_location_id1", ""))
        self.lineEdit_PnDOUT.setText(location.get("pnd_location_id2", ""))

        self.lineEdit_PallCap.setText(str(location.get("palle_cap", "")))
        self.lineEdit_CartCap.setText(str(location.get("carton_cap", "")))

        self.lineEdit_MaxHeightValue.setText(str(location.get("max_height", "")))
        self.lineEdit_MaxDepthValue.setText(str(location.get("max_depth", "")))
        self.lineEdit_MaxWidthValue.setText(str(location.get("max_width", "")))
        self.lineEdit_MaxWwightValue.setText(str(location.get("max_weight", "")))

        self.comboBox_HeightUOM.setCurrentText(location.get("uom_max_height", ""))
        self.comboBox_DepthUOM.setCurrentText(location.get("uom_max_depth", ""))
        self.comboBox_WidthUOM.setCurrentText(location.get("uom_max_width", ""))
        self.comboBox_WeightUOM.setCurrentText(location.get("uom_max_weight", ""))

        def to_bool(value):
            return str(value).strip().upper() in ["Y", "YES", "TRUE", "1"]

        self.checkBox_BlackHoleFlag.setChecked(to_bool(location.get("black_hole_flag")))

        self.lineEdit_ActivePalletsQTY.setText(str(location.get("pallet_qty_act", "")))
        self.lineEdit_ActiveCartonsQTY.setText(str(location.get("carton_qty_act", "")))

        self.lineEdit_LastTouch.setText(location.get("last_touch", ""))

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
        check("aisle", self.lineEdit_Aisel)
        check("bay", self.lineEdit_Bay)
        check("loc_level", self.lineEdit_Level)
        check("slot", self.lineEdit_Slot)
        check("pnd_location_id1", self.lineEdit_PnDIN)
        check("pnd_location_id2", self.lineEdit_PnDOUT)

        check("palle_cap", self.lineEdit_PallCap, int)
        check("carton_cap", self.lineEdit_CartCap, int)
        check("max_height", self.lineEdit_MaxHeightValue, float)
        check("max_depth", self.lineEdit_MaxDepthValue, float)
        check("max_width", self.lineEdit_MaxWidthValue, float)
        check("max_weight", self.lineEdit_MaxWwightValue, float)
        check("pallet_qty_act", self.lineEdit_ActivePalletsQTY, int)
        check("carton_qty_act", self.lineEdit_ActiveCartonsQTY, int)

        check("last_touch", self.lineEdit_LastTouch)

        # Combos
        combos = {
            "location_type": self.comboBox_LocationType,
            "putaway_class": self.comboBox_PutawayClass,
            "pick_class": self.comboBox_PickClass,
            "rstk_class": self.comboBox_RestockClass,
            "blocked_code": self.comboBox_BlockCode,
            "proximiti_in": self.comboBox_PrxIN,
            "proximiti_out": self.comboBox_PrxOUT,
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

        check_flag("black_hole_flag", self.checkBox_BlackHoleFlag)

        return updated

    def save_changes(self):
        updated_fields = self.get_updated_fields()
        if not updated_fields:
            QtWidgets.QMessageBox.information(self, "No changes", "No fields were modified.")
            return

        location_id = self.original_data.get("location_id")
        try:
            response = requests.put(f"{API_BASE_URL}/locations/{location_id}", json=updated_fields)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Location updated successfully.")
                self.original_data = self.original_data | updated_fields 
                if hasattr(self, "parent_subwindow") and self.parent_subwindow:
                    self.parent_subwindow.close()
                else:
                    self.close()
            else:
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

