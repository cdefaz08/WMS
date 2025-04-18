from PyQt5 import QtWidgets
from Layout.UI_PY.UI_ItemClassWindow import UI_ItemClassWindow

class ItemClassWindow(UI_ItemClassWindow):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)

        self.api_client = api_client
        self.original_data = []  # Para rastrear cambios
        self.tableWidget_ItemClass.verticalHeader().setVisible(False)

        self.tableWidget_ItemClass.setColumnHidden(0, True)  # Oculta columna ID
        self.tableWidget_ItemClass.setColumnWidth(1, 200) #Name
        self.tableWidget_ItemClass.setColumnWidth(2, 300) #Description
        self.tableWidget_ItemClass.horizontalHeader().setStretchLastSection(True)

        self.load_data()

    def load_data(self):
        response = self.api_client.get("/item-classes/")
        if response.status_code == 200:
            self.original_data = response.json()
            self.tableWidget_ItemClass.setRowCount(0)
            for item in self.original_data:
                self.add_row(item["id"], item["item_class"], item["description"])

    def add_row(self, id_val="", item_class_id="", description=""):
        row_position = self.tableWidget_ItemClass.rowCount()
        self.tableWidget_ItemClass.insertRow(row_position)
        self.tableWidget_ItemClass.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(id_val)))
        self.tableWidget_ItemClass.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item_class_id))
        self.tableWidget_ItemClass.setItem(row_position, 2, QtWidgets.QTableWidgetItem(description))

    def add_empty_row(self):
        self.add_row()

    def delete_selected_row(self):
        row = self.tableWidget_ItemClass.currentRow()
        if row >= 0:
            id_item = self.tableWidget_ItemClass.item(row, 0)
            if id_item and id_item.text():  # Tiene ID, entonces borrar del backend
                id_val = id_item.text()
                response = self.api_client.delete(f"/item-classes/{id_val}")
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "Item class deleted.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete item.")
            self.tableWidget_ItemClass.removeRow(row)

    def get_current_data(self):
        data = []
        for row in range(self.tableWidget_ItemClass.rowCount()):
            id_val = self.tableWidget_ItemClass.item(row, 0)
            item_class_id = self.tableWidget_ItemClass.item(row, 1)
            description = self.tableWidget_ItemClass.item(row, 2)

            data.append({
                "id": id_val.text() if id_val else "",
                "item_class_id": item_class_id.text() if item_class_id else "",
                "description": description.text() if description else "",
            })
        return data

    def save_changes(self):
        current_data = self.get_current_data()
        for row in current_data:
            # Validación
            if not row["item_class_id"]:
                continue

            # Fila nueva
            if row["id"] == "":
                response = self.api_client.post("/item-classes/", json={
                    "item_class_id": row["item_class_id"],
                    "description": row["description"]
                })
                if response.status_code != 200:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to create item class: {row['item_class_id']}")
                continue

            # Fila existente → buscar cambios
            original = next((x for x in self.original_data if str(x["id"]) == row["id"]), None)
            if original:
                if (
                    row["item_class_id"] != original["item_class"] or
                    row["description"] != original["description"]
                ):
                    # Enviar PUT solo si hay diferencias
                    response = self.api_client.put(f"/item-classes/{row['id']}", json={
                        "item_class_id": row["item_class_id"],
                        "description": row["description"]
                    })
                    if response.status_code != 200:
                        QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update item class: {row['item_class_id']}")

        QtWidgets.QMessageBox.information(self, "Success", "Changes saved successfully.")
        self.load_data()
