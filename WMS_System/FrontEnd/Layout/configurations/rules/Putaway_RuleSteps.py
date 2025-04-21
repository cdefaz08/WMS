from PyQt5 import QtWidgets
from Layout.UI_PY.UI_PutawayRuleSteps import PutawayStepsMaintWindow

class PutawayStepsLogic(PutawayStepsMaintWindow):
    def __init__(self, api_client, rule_id, rule_name, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.setWindowTitle(f"Putaway Steps for Rule: {rule_name}")

        self.load_steps()

    def get_endpoint(self):
        return "/rules_steps/putaway-rule-steps/"

    def load_steps(self):
        try:
            response = self.api_client.get(self.get_endpoint())
            if response.status_code == 200:
                all_steps = response.json()
                steps = [s for s in all_steps if s["rule_id"] == self.rule_id]
                self.populate_table(steps)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load steps:\n{str(e)}")

    def populate_table(self, steps):
        self.table.setRowCount(0)
        for step in steps:
            self.add_step_row(step)

    def add_step_row(self, step):
        row = self.table.rowCount()
        self.table.insertRow(row)

        def set_combo(index, value):
            combo = self.table.cellWidget(row, index)
            idx = combo.findText(value)
            if idx != -1:
                combo.setCurrentIndex(idx)

        self.table.cellWidget(row, 0).setValue(step.get("seq", 1))
        self.table.cellWidget(row, 1).setValue(step.get("min_percent", 0))
        self.table.cellWidget(row, 2).setValue(step.get("max_percent", 0))
        set_combo(3, step.get("uom", "Pallet"))
        set_combo(4, step.get("location_type_from", "(Ignore)"))
        set_combo(5, step.get("putaway_to", "Empty Locations"))
        set_combo(6, step.get("location_type_to", "(Ignore)"))
        set_combo(7, step.get("putaway_group", "(Ignore)"))
        self.table.cellWidget(row, 8).setText(step.get("sort_expression", ""))
        self.table.cellWidget(row, 9).setValue(step.get("max_loc_check", 0))
