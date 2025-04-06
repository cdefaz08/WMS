from PyQt5 import QtWidgets, uic
from Layout.UI_PY.LocationMaintance import Ui_LocationMaintance
import requests
from config import API_BASE_URL

class LocationMaintance(QtWidgets.QWidget, Ui_LocationMaintance):
    def __init__(self, location_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.loadLocationClasesDropdown()

        if location_data:
            self.loadLocationData(location_data)

        self.original_data = location_data.copy() if location_data else {}

    def loadLocationClasesDropdown(self):
        try:
            putaway_classes = requests.get(f"{API_BASE_URL}/putaway").json()
            restock_classes = requests.get(f"{API_BASE_URL}/restock").json()
            pick_classes = requests.get(f"{API_BASE_URL}/pick").json()

            self.comboBox_PutawayClass.clear()
            self.comboBox_RestockClass.clear()
            self.comboBox_PickClass.clear()

            for c in putaway_classes:
                self.comboBox_PutawayClass.addItem(c["class_name"], c["id"])

            for c in restock_classes:
                self.comboBox_RestockClass.addItem(c["class_name"], c["id"])

            for c in pick_classes:
                self.comboBox_PickClass.addItem(c["class_name"], c["id"])

        except Exception as e:
            print(f"Error loading dropdowns: {e}")

    def loadLocationData(self, location):
        self.lineEdit_Location.setText(location.get("location", ""))
        self.comboBox_LocationType.setCurrentText(location.get("location_type", ""))

        # Dropdowns: select by class_name
        self.comboBox_PutawayClass.setCurrentText(location.get("putaway_class", ""))
        self.comboBox_PickClass.setCurrentText(location.get("pick_class", ""))
        self.comboBox_RestockClass.setCurrentText(location.get("restock_class", ""))

        self.lineEdit_ScanLocation.setText(location.get("scan_location", ""))
        self.lineEdit_Aisel.setText(location.get("aisle", ""))
        self.lineEdit_Bay.setText(location.get("bay", ""))
        self.lineEdit_Level.setText(location.get("level", ""))
        self.lineEdit_Slot.setText(location.get("slot", ""))

        self.comboBox_BlockCode.setCurrentText(location.get("block_code", ""))
        self.comboBox_PrxIN.setCurrentText(location.get("proximity_in", ""))
        self.comboBox_PrxOUT.setCurrentText(location.get("proximity_out", ""))

        self.lineEdit_PnDIN.setText(location.get("pnd_location_1", ""))
        self.lineEdit_PnDOUT.setText(location.get("pnd_location_2", ""))

        self.lineEdit_PallCap.setText(str(location.get("pallet_capacity", "")))
        self.lineEdit_CartCap.setText(str(location.get("carton_capacity", "")))

        self.lineEdit_MaxHeightValue.setText(str(location.get("max_height", "")))
        self.lineEdit_MaxDepthValue.setText(str(location.get("max_depth", "")))
        self.lineEdit_MaxWidthValue.setText(str(location.get("max_width", "")))
        self.lineEdit_MaxWwightValue.setText(str(location.get("max_weight", "")))

        self.comboBox_HeightUOM.setCurrentText(location.get("height_uom", ""))
        self.comboBox_DepthUOM.setCurrentText(location.get("depth_uom", ""))
        self.comboBox_WidthUOM.setCurrentText(location.get("width_uom", ""))
        self.comboBox_WeightUOM.setCurrentText(location.get("weight_uom", ""))

        self.checkBox_BlackHoleFlag.setChecked(location.get("black_hole_flag", False))
        self.checkBox_HasAssignedFlag.setChecked(location.get("has_assigned_flag", False))
        self.checkBox_HasContentFlag.setChecked(location.get("has_content_flag", False))
        self.checkBox_HasPendingFlag.setChecked(location.get("has_pending_flag", False))

        self.lineEdit_ActivePalletsQTY.setText(str(location.get("active_pallets_qty", "")))
        self.lineEdit_ActiveCartonsQTY.setText(str(location.get("active_cartons_qty", "")))

        self.lineEdit_LastTouch.setText(location.get("last_touch", ""))



    def get_updated_fields(self):
        updated = {}

        def check(field, widget, type_cast=str):
            current = widget.text().strip()
            original = str(self.original_data.get(field, "")).strip()
            if current != original:
                if not current: return
                try:
                    updated[field] = type_cast(current)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Error", f"{field} must be a {type_cast.__name__}")

        check("location", self.lineEdit_Location)
        check("scan_location", self.lineEdit_ScanLocation)
        check("aisle", self.lineEdit_Aisel)
        check("bay", self.lineEdit_Bay)
        check("level", self.lineEdit_Level)
        check("slot", self.lineEdit_Slot)
        check("pnd_location_1", self.lineEdit_PnDIN)
        check("pnd_location_2", self.lineEdit_PnDOUT)

        check("pallet_capacity", self.lineEdit_PallCap, int)
        check("carton_capacity", self.lineEdit_CartCap, int)

        check("max_height", self.lineEdit_MaxHeightValue, float)
        check("max_depth", self.lineEdit_MaxDepthValue, float)
        check("max_width", self.lineEdit_MaxWidthValue, float)
        check("max_weight", self.lineEdit_MaxWwightValue, float)

        check("last_touch", self.lineEdit_LastTouch)

        # Combos
        if self.comboBox_LocationType.currentText() != self.original_data.get("location_type", ""):
            updated["location_type"] = self.comboBox_LocationType.currentText()

        if self.comboBox_PutawayClass.currentText() != self.original_data.get("putaway_class", ""):
            updated["putaway_class"] = self.comboBox_PutawayClass.currentText()

        if self.comboBox_PickClass.currentText() != self.original_data.get("pick_class", ""):
            updated["pick_class"] = self.comboBox_PickClass.currentText()

        if self.comboBox_RestockClass.currentText() != self.original_data.get("restock_class", ""):
            updated["restock_class"] = self.comboBox_RestockClass.currentText()

        if self.comboBox_BlockCode.currentText() != self.original_data.get("block_code", ""):
            updated["block_code"] = self.comboBox_BlockCode.currentText()

        if self.comboBox_PrxIN.currentText() != self.original_data.get("proximity_in", ""):
            updated["proximity_in"] = self.comboBox_PrxIN.currentText()

        if self.comboBox_PrxOUT.currentText() != self.original_data.get("proximity_out", ""):
            updated["proximity_out"] = self.comboBox_PrxOUT.currentText()

        if self.comboBox_HeightUOM.currentText() != self.original_data.get("height_uom", ""):
            updated["height_uom"] = self.comboBox_HeightUOM.currentText()

        if self.comboBox_DepthUOM.currentText() != self.original_data.get("depth_uom", ""):
            updated["depth_uom"] = self.comboBox_DepthUOM.currentText()

        if self.comboBox_WidthUOM.currentText() != self.original_data.get("width_uom", ""):
            updated["width_uom"] = self.comboBox_WidthUOM.currentText()

        if self.comboBox_WeightUOM.currentText() != self.original_data.get("weight_uom", ""):
            updated["weight_uom"] = self.comboBox_WeightUOM.currentText()

        # Checkboxes
        def check_flag(field, checkbox):
            current = checkbox.isChecked()
            original = self.original_data.get(field, False)
            if current != original:
                updated[field] = current

        check_flag("black_hole_flag", self.checkBox_BlackHoleFlag)
        check_flag("has_assigned_flag", self.checkBox_HasAssignedFlag)
        check_flag("has_content_flag", self.checkBox_HasContentFlag)
        check_flag("has_pending_flag", self.checkBox_HasPendingFlag)

        return updated



    def save_changes(self):
        updated_fields = self.get_updated_fields()
        if not updated_fields:
            QtWidgets.QMessageBox.information(self, "No changes", "No fields were modified.")
            return

        location_id = self.original_data.get("id")
        try:
            response = requests.put(f"{API_BASE_URL}/locations/{location_id}", json=updated_fields)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Location updated successfully.")
                self.accept()  # or self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update location: {response.text}")
        except requests.exceptions.RequestException:
            QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")

        print(f"Updated fields for Location ID {location_id}: {updated_fields}")
