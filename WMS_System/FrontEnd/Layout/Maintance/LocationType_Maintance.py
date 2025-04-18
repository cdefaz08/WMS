from PyQt5 import QtWidgets
from Layout.UI_PY.LocationTypeMaintance_ui import Ui_Form

class LocationType_Maintance(QtWidgets.QWidget):
    def __init__(self,api_client = None, locationTypeData=None, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.api_client = api_client

        self.original_data = {}

        if locationTypeData:
            self.load_locationType_data(locationTypeData)

    def normalize_data(self, data: dict) -> dict:
        normalized = {}
        for key, value in data.items():
            if isinstance(value, str):
                normalized[key] = value.strip().upper()
            else:
                normalized[key] = value
        return normalized

    def load_locationType_data(self, locationTypeData):
        # Normalizamos los datos y los guardamos como originales
        self.original_data = self.normalize_data(locationTypeData.copy())
        print("Original saved:", self.original_data)

        # LineEdits
        self.ui.location_type.setText(locationTypeData.get("location_type", ""))
        self.ui.description.setText(locationTypeData.get("description", ""))

        # CheckBoxes (valores "Y" o "N")
        self.ui.sto_pall_flag.setChecked(locationTypeData.get("sto_pall_flag") == "Y")
        self.ui.sto_pall_con_flag.setChecked(locationTypeData.get("sto_pall_con_flag") == "Y")
        self.ui.sto_cont_flag.setChecked(locationTypeData.get("sto_cont_flag") == "Y")
        self.ui.sto_cart_flag.setChecked(locationTypeData.get("sto_cart_flag") == "Y")
        self.ui.mix_item_flag.setChecked(locationTypeData.get("mix_item_flag") == "Y")
        self.ui.mix_cfg_flag.setChecked(locationTypeData.get("mix_cfg_flag") == "Y")
        self.ui.mix_trackingdate_flag.setChecked(locationTypeData.get("mix_trackingdate_flag") == "Y")
        self.ui.pick_pallet_flag.setChecked(locationTypeData.get("pick_pallet_flag") == "Y")
        self.ui.pick_cart_flag.setChecked(locationTypeData.get("pick_cart_flag") == "Y")
        self.ui.pick_piece_flag.setChecked(locationTypeData.get("pick_piece_flag") == "Y")
        self.ui.merge_flag.setChecked(locationTypeData.get("merge_flag") == "Y")
        self.ui.merge_cfg_code.setChecked(locationTypeData.get("merge_cfg_code") == "Y")
        self.ui.merge_trackingdate.setChecked(locationTypeData.get("merge_trackingdate") == "Y")
        self.ui.merge_receiving_date.setChecked(locationTypeData.get("merge_receiving_date") == "Y")
        self.ui.mix_receivingdate_flag.setChecked(locationTypeData.get("mix_receivingdate_flag") == "Y")
        self.ui.trash_pall.setChecked(locationTypeData.get("trash_pall") == "Y")
        self.ui.merge_inventory_type.setChecked(locationTypeData.get("merge_inventory_type") == "Y")

    def get_current_data(self):
        return {
            "location_type": self.ui.location_type.text().strip().upper(),
            "description": self.ui.description.text().strip().upper(),
            "sto_pall_flag": "Y" if self.ui.sto_pall_flag.isChecked() else "N",
            "sto_pall_con_flag": "Y" if self.ui.sto_pall_con_flag.isChecked() else "N",
            "sto_cont_flag": "Y" if self.ui.sto_cont_flag.isChecked() else "N",
            "sto_cart_flag": "Y" if self.ui.sto_cart_flag.isChecked() else "N",
            "mix_item_flag": "Y" if self.ui.mix_item_flag.isChecked() else "N",
            "mix_cfg_flag": "Y" if self.ui.mix_cfg_flag.isChecked() else "N",
            "mix_trackingdate_flag": "Y" if self.ui.mix_trackingdate_flag.isChecked() else "N",
            "pick_pallet_flag": "Y" if self.ui.pick_pallet_flag.isChecked() else "N",
            "pick_cart_flag": "Y" if self.ui.pick_cart_flag.isChecked() else "N",
            "pick_piece_flag": "Y" if self.ui.pick_piece_flag.isChecked() else "N",
            "merge_flag": "Y" if self.ui.merge_flag.isChecked() else "N",
            "merge_cfg_code": "Y" if self.ui.merge_cfg_code.isChecked() else "N",
            "merge_trackingdate": "Y" if self.ui.merge_trackingdate.isChecked() else "N",
            "merge_receiving_date": "Y" if self.ui.merge_receiving_date.isChecked() else "N",
            "mix_receivingdate_flag": "Y" if self.ui.mix_receivingdate_flag.isChecked() else "N",
            "trash_pall": "Y" if self.ui.trash_pall.isChecked() else "N",
            "merge_inventory_type": "Y" if self.ui.merge_inventory_type.isChecked() else "N"
        }


    def get_updated_fields(self):
        current_data = {
            "location_type": self.ui.location_type.text().strip().upper(),
            "description": self.ui.description.text().strip().upper(),
            "sto_pall_flag": "Y" if self.ui.sto_pall_flag.isChecked() else "N",
            "sto_pall_con_flag": "Y" if self.ui.sto_pall_con_flag.isChecked() else "N",
            "sto_cont_flag": "Y" if self.ui.sto_cont_flag.isChecked() else "N",
            "sto_cart_flag": "Y" if self.ui.sto_cart_flag.isChecked() else "N",
            "mix_item_flag": "Y" if self.ui.mix_item_flag.isChecked() else "N",
            "mix_cfg_flag": "Y" if self.ui.mix_cfg_flag.isChecked() else "N",
            "mix_trackingdate_flag": "Y" if self.ui.mix_trackingdate_flag.isChecked() else "N",
            "pick_pallet_flag": "Y" if self.ui.pick_pallet_flag.isChecked() else "N",
            "pick_cart_flag": "Y" if self.ui.pick_cart_flag.isChecked() else "N",
            "pick_piece_flag": "Y" if self.ui.pick_piece_flag.isChecked() else "N",
            "merge_flag": "Y" if self.ui.merge_flag.isChecked() else "N",
            "merge_cfg_code": "Y" if self.ui.merge_cfg_code.isChecked() else "N",
            "merge_trackingdate": "Y" if self.ui.merge_trackingdate.isChecked() else "N",
            "merge_receiving_date": "Y" if self.ui.merge_receiving_date.isChecked() else "N",
            "mix_receivingdate_flag": "Y" if self.ui.mix_receivingdate_flag.isChecked() else "N",
            "trash_pall": "Y" if self.ui.trash_pall.isChecked() else "N",
            "merge_inventory_type": "Y" if self.ui.merge_inventory_type.isChecked() else "N"
        }

        # Normaliza current_data para comparar correctamente
        normalized_current = self.normalize_data(current_data)

        # Comparar con los datos originales
        updated = {}
        for key, value in normalized_current.items():
            if self.original_data.get(key) != value:
                updated[key] = value

        return updated

    def save_changes(self):
        updated_data = self.get_updated_fields()

        if not updated_data:
            QtWidgets.QMessageBox.information(self, "No Changes", "No changes were made to update.")
            return

        try:
            url = f"/location-types/{self.ui.location_type.text()}"
            response = self.api_client.put(url, json=updated_data)

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Location type updated successfully!")
                self.original_data = self.normalize_data(self.get_current_data())
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update.\n{response.text}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
