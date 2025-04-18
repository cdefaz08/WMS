from PyQt5 import QtWidgets, uic

class RuleClases(QtWidgets.QDialog):
    def __init__(self, api_client=None, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/RuleClases.ui", self)
        self.api_client = api_client

        self.tableWidget_PutawayClass.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_PutawayClass.verticalHeader().setVisible(False)
        self.tableWidget_RestockClass.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_RestockClass.verticalHeader().setVisible(False)
        self.tableWidget_PickClass.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_PickClass.verticalHeader().setVisible(False)

        self.load_data()

    def load_data(self):
        endpoints = {
            "putaway": self.tableWidget_PutawayClass,
            "restock": self.tableWidget_RestockClass,
            "pick": self.tableWidget_PickClass,
        }

        for endpoint, widget in endpoints.items():
            try:
                response = self.api_client.get(f"/classes/{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                else:
                    data = []
            except Exception:
                data = []

            self.fill_table(widget, data)

    def fill_table(self, table_widget, data):
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["ID", "Class Name", "Description"])

        for row_index, item in enumerate(data):
            table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item["id"])))
            table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item["class_name"]))
            table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(item["description"]))

        table_widget.setColumnHidden(0, True)
        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)

    def add_new_row(self):
        current_tab = self.tabWidget_Clases.currentIndex()
        if current_tab == 0:
            table = self.tableWidget_PutawayClass
        elif current_tab == 1:
            table = self.tableWidget_RestockClass
        elif current_tab == 2:
            table = self.tableWidget_PickClass
        else:
            return

        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(""))
        table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(""))
        table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(""))

    def delete_selected_row(self):
        current_tab = self.tabWidget_Clases.currentIndex()
        if current_tab == 0:
            table = self.tableWidget_PutawayClass
            endpoint = "putaway"
        elif current_tab == 1:
            table = self.tableWidget_RestockClass
            endpoint = "restock"
        elif current_tab == 2:
            table = self.tableWidget_PickClass
            endpoint = "pick"
        else:
            return

        selected = table.currentRow()
        if selected >= 0:
            item_id = table.item(selected, 0)
            if item_id:
                confirm = QtWidgets.QMessageBox.question(
                    self,
                    "Confirm Deletion",
                    "Are you sure you want to delete this class?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
                if confirm != QtWidgets.QMessageBox.Yes:
                    return

                try:
                    response = self.api_client.delete(f"/classes/{endpoint}/{item_id.text()}")
                    if response.status_code in (200, 204):
                        table.removeRow(selected)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not delete class.")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Could not delete:\n{str(e)}")

    def save_changes(self):
        current_tab = self.tabWidget_Clases.currentIndex()
        if current_tab == 0:
            table = self.tableWidget_PutawayClass
            endpoint = "putaway"
        elif current_tab == 1:
            table = self.tableWidget_RestockClass
            endpoint = "restock"
        elif current_tab == 2:
            table = self.tableWidget_PickClass
            endpoint = "pick"
        else:
            return

        for row in range(table.rowCount()):
            id_item = table.item(row, 0)
            class_name = table.item(row, 1)
            description = table.item(row, 2)

            data = {
                "class_name": class_name.text() if class_name else "",
                "description": description.text() if description else ""
            }

            try:
                if not id_item or not id_item.text().strip():
                    response = self.api_client.post(f"/classes/{endpoint}/", json=data)
                    if response.status_code in (200, 201):
                        new_id = response.json().get("id")
                        table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(new_id)))
                else:
                    class_id = id_item.text().strip()
                    self.api_client.put(f"/classes/{endpoint}/{class_id}", json=data)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Connection Error", str(e))

        self.load_data()

    def refresh_data(self):
        self.load_data()

    def has_unsaved_changes(self):
        current_tab = self.tabWidget_Clases.currentIndex()
        if current_tab == 0:
            table = self.tableWidget_PutawayClass
            endpoint = "putaway"
        elif current_tab == 1:
            table = self.tableWidget_RestockClass
            endpoint = "restock"
        elif current_tab == 2:
            table = self.tableWidget_PickClass
            endpoint = "pick"
        else:
            return False

        try:
            response = self.api_client.get(f"/classes/{endpoint}")
            if response.status_code != 200:
                return False

            original_data = {str(item["id"]): item for item in response.json()}

            for row in range(table.rowCount()):
                id_item = table.item(row, 0)
                class_name = table.item(row, 1).text() if table.item(row, 1) else ""
                description = table.item(row, 2).text() if table.item(row, 2) else ""

                if not id_item or not id_item.text().strip():
                    return True

                id_str = id_item.text().strip()
                if id_str in original_data:
                    original = original_data[id_str]
                    if (
                        original["class_name"] != class_name
                        or original["description"] != description
                    ):
                        return True
        except:
            return False

        return False

    def closeEvent(self, event):
        if self.has_unsaved_changes():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to close without saving?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                event.ignore()
                return
        event.accept()
