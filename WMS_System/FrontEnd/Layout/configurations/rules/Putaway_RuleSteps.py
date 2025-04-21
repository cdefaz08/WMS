from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from Layout.UI_PY.UI_PutawayRuleSteps import PutawayStepsMaintWindow
from PyQt5.QtWidgets import QMessageBox

class PutawayStepsLogic(PutawayStepsMaintWindow):
    def __init__(self, api_client, rule_id, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.location_types = []
        self.putaway_groups = []

        self.rule_id = rule_id
        self.original_data = []
        self.load_dropdown_data() 
        self.load_steps()

    def get_endpoint(self):
        return "/rules_steps/putaway-rule-steps/"

    def load_dropdown_data(self):
        # Load location types
        try:
            res = self.api_client.get("/location-types")
            if res.status_code == 200:
                self.location_types = [lt["location_type"] for lt in res.json()]
            else:
                self.location_types = ["(Ignore)"]
        except:
            self.location_types = ["(Ignore)"]

        # Load putaway groups
        try:
            res = self.api_client.get("/Groups/putaway-groups/")
            if res.status_code == 200:
                self.putaway_groups = [g["group_name"] for g in res.json()]
            else:
                self.putaway_groups = ["(Ignore)"]
        except:
            self.putaway_groups = ["(Ignore)"]


    def load_steps(self):
        try:
            response = self.api_client.get(self.get_endpoint())
            if response.status_code == 200:
                all_steps = response.json()
                steps = [s for s in all_steps if s["rule_id"] == self.rule_id]
                self.populate_table(steps)
                self.original_data = steps
            else:
                self.populate_table([])  # show empty
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load steps:\n{str(e)}")

    def populate_table(self, steps):
        self.table.setRowCount(0)
        if not steps:
            self.add_empty_row()
        else:
            for step in steps:
                self.add_step_row(step)

    def add_empty_row(self):
        self.add_step_row()

    def get_row_data(self, row):
        return {
            "rule_id": self.rule_id,
            "seq": self.table.cellWidget(row, 0).value(),
            "min_percent": self.table.cellWidget(row, 1).value(),
            "max_percent": self.table.cellWidget(row, 2).value(),
            "UOM": self.table.cellWidget(row, 3).currentText(),
            "location_type_from": self.table.cellWidget(row, 4).currentText(),
            "putaway_to": self.table.cellWidget(row, 5).currentText(),
            "location_type_to": self.table.cellWidget(row, 6).currentText(),
            "putaway_group": self.table.cellWidget(row, 7).currentText(),
            "sort_expresion": self.table.cellWidget(row, 8).text(),
            "max_loc_check": self.table.cellWidget(row, 9).value(),
            "id": self.table.item(row, 0).data(Qt.UserRole) if self.table.item(row, 0) else None
        }

    def is_row_modified(self, current, original):
        return any(current.get(k) != original.get(k) for k in current)

    def save_changes(self):
        row_count = self.table.rowCount()
        success = True
        updated_original_data = []

        used_seq = set()
        for row in range(row_count):
            data = self.get_row_data(row)
            if data["seq"] in used_seq:
                QMessageBox.warning(self, "Validation Error", f"Duplicate SEQ # found in row {row + 1}")
                return
            used_seq.add(data["seq"])

            row_id = self.table.item(row, 0).data(1000) if self.table.item(row, 0) else None
            try:
                if row_id:
                    original = next((r for r in self.original_data if r["id"] == row_id), {})
                    if self.is_row_modified(data, original):
                        response = self.api_client.put(f"{self.get_endpoint()}{row_id}", json=data)
                        if response.status_code != 200:
                            raise Exception(f"Update failed for row {row + 1}")
                        updated_original_data.append({**data, "id": row_id})
                    else:
                        updated_original_data.append(original)
                else:
                    response = self.api_client.post(self.get_endpoint(), json=data)
                    if response.status_code == 200:
                        new_id = response.json()["id"]
                        item = QtWidgets.QTableWidgetItem(str(data["seq"]))
                        item.setData(1000, new_id)
                        self.table.setItem(row, 0, item)
                        updated_original_data.append({**data, "id": new_id})
                    else:
                        raise Exception(f"Create failed for row {row + 1}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))
                success = False

        if success:
            self.original_data = updated_original_data
            QMessageBox.information(self, "Success", "Changes saved successfully.")

    def add_step_row(self, step=None):
        step = step or {}
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Combos con valores ya cargados
        combo_from = self._combobox(self.location_types or ["(Ignore)"], 180)
        combo_to = self._combobox(self.location_types or ["(Ignore)"], 180)
        combo_group = self._combobox(self.putaway_groups or ["(Ignore)"], 180)

        # Agregar widgets a la fila
        self.table.setCellWidget(row, 0, self._spinbox(step.get("seq", 1), 1, 1000))  # SEQ
        step_id = step.get("id")
        print("step_id", step_id)
        if step_id is not None:
            item = QtWidgets.QTableWidgetItem(str(step.get("seq", 1)))
            item.setData(1000, step_id)  # ✅ Guardamos el ID usando user role 1000
            self.table.setItem(row, 0, item)    
        self.table.setCellWidget(row, 1, self._doublespin(step.get("min_percent", 0), 0, 1000))
        self.table.setCellWidget(row, 2, self._doublespin(step.get("max_percent", 0), 0, 1000))
        self.table.setCellWidget(row, 3, self._combobox(["Pallet", "Case", "Piece"]))  # UOM

        # Preselección de combos
        self.table.setCellWidget(row, 4, combo_from)
        self.table.setCellWidget(row, 5, self._combobox(
            ["Empty Locations", "Consolidating Item", "Mixing Items"], 180))
        self.table.setCellWidget(row, 6, combo_to)
        self.table.setCellWidget(row, 7, combo_group)

        self.table.setCellWidget(row, 8, self._lineedit(step.get("sort_expresion", ""), 200))
        self.table.setCellWidget(row, 9, self._spinbox(step.get("max_loc_check", 0), 0, 100, 180))

        # Preseleccionar valores si están en los combos
        def set_combo_if_exists(combo, value):
            index = combo.findText(value)
            if index >= 0:
                combo.setCurrentIndex(index)

        set_combo_if_exists(combo_from, step.get("location_type_from", "(Ignore)"))
        set_combo_if_exists(combo_to, step.get("location_type_to", "(Ignore)"))
        set_combo_if_exists(combo_group, step.get("putaway_group", "(Ignore)"))


    def delete_selected_row(self):
        selected = self.table.currentRow()
        print ("selected", selected)
        if selected < 0:
            QMessageBox.warning(self, "Delete", "No row selected.")
            return

        row_id = self.table.item(selected, 0).data(1000) if self.table.item(selected, 0) else None
        print("row_id", row_id)


        if row_id:
            try:
                response = self.api_client.delete(f"{self.get_endpoint()}{row_id}")
                if response.status_code != 200:
                    raise Exception("Failed to delete row from server.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete row:\n{str(e)}")
                return
        
        self.table.removeRow(selected)


