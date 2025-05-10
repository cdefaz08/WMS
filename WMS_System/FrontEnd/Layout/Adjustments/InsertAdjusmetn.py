from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from datetime import datetime

class InsertIntoLocationWindow(QtWidgets.QWidget):
    def __init__(self,api_client,location_name= None,pallet_id= None,user= None, location_type_rules= None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user = user
        self.pallet_id = pallet_id
        print(self.pallet_id)
        self.location_name = location_name
        self.rules = location_type_rules or {}
        self.setup_ui()
        self.input_upc.editingFinished.connect(self.lookup_upc)
        self.input_tracking_date.setDate(QDate.currentDate())
        self.input_received_date.setDate(QDate.currentDate())
        # Auto-select and limit behavior based on context
        if self.pallet_id:
            self.radio_content.setChecked(True)
            self.radio_pallet.setEnabled(False)
            self.radio_carton.setEnabled(False)

            self.radio_location.setEnabled(False)
            self.radio_pallet.setChecked(True)
            self.radio_into_carton.setEnabled(False)
        else:
            self.insert_radio_pallet.setChecked(True)
            self.insert_radio_pallet.setEnabled(True)
            self.radio_location.setChecked(True)

            
    def setup_ui(self):
        self.setWindowTitle(f"Insert into Location: {self.location_name}")

        # Insert Options
        self.insert_group = QtWidgets.QGroupBox("Insert")
        self.insert_radio_pallet = QtWidgets.QRadioButton("Pallet")
        self.radio_carton = QtWidgets.QRadioButton("Carton")
        self.radio_content = QtWidgets.QRadioButton("Content")
        insert_layout = QtWidgets.QVBoxLayout()
        insert_layout.addWidget(self.insert_radio_pallet)
        insert_layout.addWidget(self.radio_carton)
        insert_layout.addWidget(self.radio_content)
        self.insert_group.setLayout(insert_layout)

        # Into Options
        self.into_group = QtWidgets.QGroupBox("Into")
        self.radio_location = QtWidgets.QRadioButton(f"Location {self.location_name}")
        if self.pallet_id:
            self.radio_pallet = QtWidgets.QRadioButton(f"Pallet {self.pallet_id}" )
        else:
            self.radio_pallet = QtWidgets.QRadioButton(f"Pallet" )
        self.radio_into_carton = QtWidgets.QRadioButton("Carton")
        into_layout = QtWidgets.QVBoxLayout()
        into_layout.addWidget(self.radio_location)
        into_layout.addWidget(self.radio_pallet)
        into_layout.addWidget(self.radio_into_carton)
        self.into_group.setLayout(into_layout)

        # Dynamic Fields Area
        self.dynamic_area = QtWidgets.QStackedWidget()

        self.pallet_fields = self.build_pallet_fields()
        self.content_fields = self.build_content_fields()

        self.dynamic_area.addWidget(self.pallet_fields)
        self.dynamic_area.addWidget(self.content_fields)

        # Buttons
        self.button_ok = QtWidgets.QPushButton("OK")
        self.button_cancel = QtWidgets.QPushButton("Cancel")

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.insert_group)
        main_layout.addWidget(self.into_group)
        main_layout.addWidget(self.dynamic_area)
        main_layout.addWidget(self.button_ok)
        main_layout.addWidget(self.button_cancel)

        # Connections
        self.insert_radio_pallet.toggled.connect(self.update_dynamic_area)
        self.radio_content.toggled.connect(self.update_dynamic_area)
        self.button_ok.clicked.connect(self.submit)

        self.apply_rules()
        self.update_dynamic_area() 

    def build_pallet_fields(self):
        # Return a QWidget with all Pallet fields
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        self.input_pallet_id = QtWidgets.QLineEdit()
        self.input_pallet_type = QtWidgets.QLineEdit()
        self.input_condition = QtWidgets.QLineEdit()
        self.input_adjust_reason = QtWidgets.QLineEdit()
        self.input_requester = QtWidgets.QLineEdit()
        layout.addRow("Pallet:", self.input_pallet_id)
        layout.addRow("Pallet Type:", self.input_pallet_type)
        layout.addRow("Condition:", self.input_condition)
        layout.addRow("Adjust Reason:", self.input_adjust_reason)
        layout.addRow("Requester:", self.input_requester)
        return widget

    def build_content_fields(self):
        # Return a QWidget with all Content fields
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        self.input_upc = QtWidgets.QLineEdit()
        self.input_item_code = QtWidgets.QLineEdit()
        self.input_description = QtWidgets.QLineEdit()
        self.input_tracking_date = QtWidgets.QDateEdit()
        self.input_tracking_date.setReadOnly(True)
        self.input_tracking_date.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.input_tracking_date.setFocusPolicy(QtCore.Qt.NoFocus)

        self.input_received_date = QtWidgets.QDateEdit()
        self.input_received_date.setReadOnly(True)
        self.input_received_date.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.input_received_date.setFocusPolicy(QtCore.Qt.NoFocus)
        self.input_onhand = QtWidgets.QSpinBox()
        layout.addRow("UPC:", self.input_upc)
        layout.addRow("Item:", self.input_item_code)
        layout.addRow("Description:", self.input_description)
        layout.addRow("Tracking Date:", self.input_tracking_date)
        layout.addRow("Received Date:", self.input_received_date)
        layout.addRow("Onhand:", self.input_onhand)
        return widget

    def update_dynamic_area(self):
        if self.insert_radio_pallet.isChecked():
            self.dynamic_area.setCurrentWidget(self.pallet_fields)
        elif self.radio_content.isChecked():
            self.dynamic_area.setCurrentWidget(self.content_fields)
        else:
            self.dynamic_area.setCurrentIndex(-1)


    def lookup_upc(self):
        upc = self.input_upc.text().strip()
        if not upc:
            return

        try:
            response = self.api_client.get(f"/items/upc/{upc}")
            if response.status_code == 200:
                item = response.json()
                self.input_item_code.setText(item.get("item_id", ""))
                self.input_description.setText(item.get("description", ""))
            else:
                self.input_item_code.clear()
                self.input_description.clear()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"UPC lookup failed:\n{str(e)}")

    def apply_rules(self):
        if not self.rules.get("allow_picking_carton", True):
            self.radio_carton.setEnabled(False)

    def submit(self):
        now = datetime.now()

        if self.insert_radio_pallet.isChecked() and not self.pallet_id:
            # ➡ Crear un nuevo pallet
            data = {
                "pallet_id": self.input_pallet_id.text().strip(),
                "pallet_type": self.input_pallet_type.text().strip(),
                "condition": self.input_condition.text().strip(),
                "adjust_reason": self.input_adjust_reason.text().strip(),
                "requester": self.input_requester.text().strip(),
                "location_id": self.location_name,
                "pieces_on_hand": 0,
                "created_date": now.isoformat(),
                "created_by": self.user,
            }
            try:
                response = self.api_client.post("/pallets/", json=data)
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "Pallet created successfully!")
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to create pallet.\n{response.text}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"API Error:\n{str(e)}")

        elif self.radio_content.isChecked():
            # ➡ Insertar contenido (puede ser suelto o en un pallet)
            target_pallet_id = self.pallet_id if self.radio_pallet.isChecked() and self.pallet_id else None
            data = {
                "location_id": self.location_name,
                "pallet_id": target_pallet_id,
                "item_id": self.input_item_code.text().strip(),
                "pieces_on_hand": self.input_onhand.value(),
                "receipt_info": "",
                "receipt_release_num": "",
                "date_time_last_touched": self.input_tracking_date.dateTime().toString("yyyy-MM-ddTHH:mm:ss"),
                "user_last_touched": self.user
            }
            try:
                response = self.api_client.post("/a-contents/", json=data)
                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Success", "Content inserted successfully!")
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to insert content.\n{response.text}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"API Error:\n{str(e)}")

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a valid insert option.")

