from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox 
from Layout.UI_PY.LocationTypeMaintance_ui import Ui_Form
import requests
from config import API_BASE_URL

class AddLocationType(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)



    def createLocationType(self):
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



    def save_changes(self):
        updated_data = self.createLocationType()

        if not updated_data:
            QtWidgets.QMessageBox.information(self, "No Changes", "No changes were made to update.")
            return

        try:
            url = f"{API_BASE_URL}/location-types/"
            response = requests.post(url, json=updated_data)

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Location type Created successfully!")
                # Intenta cerrar el subwindow si existe
                if hasattr(self, "parent_subwindow"):
                    self.parent_subwindow.close()
                else:
                    self.close()
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update.\n{response.text}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
