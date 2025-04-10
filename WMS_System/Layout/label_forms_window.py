import sys
import requests
from PyQt5 import QtWidgets
from Layout.UI_PY.forms_ui import Ui_Forms
from config import API_BASE_URL

class FormManager(QtWidgets.QWidget):
    def __init__(self,api_client = None):
        super().__init__()
        self.ui = Ui_Forms()
        self.ui.setupUi(self)
        self.api_client = api_client

        self.setup_tables()
        self.load_all_data()

    def setup_tables(self):
        for table in [self.ui.tableWidget_LabelForms, self.ui.tableWidgetDocForms]:
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Form Name", "Description", "Template"])
            table.setColumnHidden(0, True)
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setStretchLastSection(True)

    def load_all_data(self):
        self.load_forms(
            endpoint="label_forms",
            table=self.ui.tableWidget_LabelForms
        )
        self.load_forms(
            endpoint="document_forms",
            table=self.ui.tableWidgetDocForms
        )

    def load_forms(self, endpoint, table):
        try:
            response = requests.get(f"{API_BASE_URL}/{endpoint}/")
            if response.status_code == 200:
                self.fill_table(table, response.json())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load {endpoint}:\n{str(e)}")

    def fill_table(self, table, data):
        table.setRowCount(len(data))
        for row_index, item in enumerate(data):
            table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item["id"])))
            table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("document_form", "") or item.get("label_form", "")))
            table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(item.get("description", "")))
            table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(item.get("template_content", "")))

    def add_new_row(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:
            self.add_new_row_for(self.ui.tableWidgetDocForms)
        elif current_tab == 1:
            self.add_new_row_for(self.ui.tableWidget_LabelForms)

    def add_new_row_for(self, table):
        row = table.rowCount()
        table.insertRow(row)
        for col in range(4):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(""))

    def save_changes(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:
            self._save_changes_for(self.ui.tableWidgetDocForms, "document_forms", "document_form")
        elif current_tab == 1:
            self._save_changes_for(self.ui.tableWidget_LabelForms, "label_forms", "label_form")

    def _save_changes_for(self, table, endpoint, name_field):
        for row in range(table.rowCount()):
            id_item = table.item(row, 0)
            form_name = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            description = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            template = table.item(row, 3).text().strip() if table.item(row, 3) else ""

            data = {
                name_field: form_name,
                "description": description,
                "template_content": template
            }

            try:
                if not id_item or not id_item.text().strip():
                    response = requests.post(f"{API_BASE_URL}/{endpoint}/", json=data)
                    if response.status_code in (200, 201):
                        new_id = response.json().get("id")
                        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(new_id)))
                else:
                    form_id = id_item.text().strip()
                    requests.put(f"{API_BASE_URL}/{endpoint}/{form_id}", json=data)
            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))

        QtWidgets.QMessageBox.information(self, "Saved", f"{endpoint.replace('_', ' ').title()} saved successfully.")
        self.load_all_data()


    def delete_selected_row(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:
            self._delete_selected_row_for(self.ui.tableWidgetDocForms, "document_forms")
        elif current_tab == 1:
            self._delete_selected_row_for(self.ui.tableWidget_LabelForms, "label_forms")

    def _delete_selected_row_for(self, table, endpoint):
        row = table.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a row to delete.")
            return

        id_item = table.item(row, 0)
        if not id_item or not id_item.text().strip():
            table.removeRow(row)
            return

        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm Deletion", "Delete this item?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        form_id = id_item.text().strip()
        try:
            response = requests.delete(f"{API_BASE_URL}/{endpoint}/{form_id}")
            if response.status_code in (200, 204):
                table.removeRow(row)
                QtWidgets.QMessageBox.information(self, "Deleted", "Item deleted.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Could not delete item.")
        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Delete failed:\n{str(e)}")
