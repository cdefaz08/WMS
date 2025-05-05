from PyQt5 import QtWidgets

class InsertIntoLocationWindow(QtWidgets.QWidget):
    def __init__(self,api_client,location_name, location_type_rules, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.location_name = location_name
        self.rules = location_type_rules
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle(f"Insert into Location: {self.location_name}")

        # Insert Options
        self.insert_group = QtWidgets.QGroupBox("Insert")
        self.radio_pallet = QtWidgets.QRadioButton("Pallet")
        self.radio_carton = QtWidgets.QRadioButton("Carton")
        self.radio_content = QtWidgets.QRadioButton("Content")
        insert_layout = QtWidgets.QVBoxLayout()
        insert_layout.addWidget(self.radio_pallet)
        insert_layout.addWidget(self.radio_carton)
        insert_layout.addWidget(self.radio_content)
        self.insert_group.setLayout(insert_layout)

        # Into Options
        self.into_group = QtWidgets.QGroupBox("Into")
        self.radio_location = QtWidgets.QRadioButton(f"Location{self.location_name}")
        self.radio_into_pallet = QtWidgets.QRadioButton("Pallet")
        self.radio_into_carton = QtWidgets.QRadioButton("Carton")
        into_layout = QtWidgets.QVBoxLayout()
        into_layout.addWidget(self.radio_location)
        into_layout.addWidget(self.radio_into_pallet)
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
        self.radio_pallet.toggled.connect(self.update_dynamic_area)
        self.radio_content.toggled.connect(self.update_dynamic_area)
        self.button_ok.clicked.connect(self.submit)

        self.apply_rules()

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
        self.input_owner = QtWidgets.QLineEdit()
        self.input_item_code = QtWidgets.QLineEdit()
        self.input_description = QtWidgets.QLineEdit()
        self.input_serial_number = QtWidgets.QLineEdit()
        self.input_lot = QtWidgets.QLineEdit()
        self.input_tracking_date = QtWidgets.QDateEdit()
        self.input_received_date = QtWidgets.QDateEdit()
        self.input_onhand = QtWidgets.QSpinBox()
        layout.addRow("Owner:", self.input_owner)
        layout.addRow("Item:", self.input_item_code)
        layout.addRow("Description:", self.input_description)
        layout.addRow("Serial Number:", self.input_serial_number)
        layout.addRow("Lot:", self.input_lot)
        layout.addRow("Tracking Date:", self.input_tracking_date)
        layout.addRow("Received Date:", self.input_received_date)
        layout.addRow("Onhand:", self.input_onhand)
        return widget

    def update_dynamic_area(self):
        if self.radio_pallet.isChecked():
            self.dynamic_area.setCurrentIndex(0)
        elif self.radio_content.isChecked():
            self.dynamic_area.setCurrentIndex(1)

    def apply_rules(self):
        if not self.rules.get("allow_picking_carton", True):
            self.radio_carton.setEnabled(False)

    def submit(self):
        try:
            payload = {}

            if self.radio_pallet.isChecked():
                # 👉 Creating a new Pallet
                pallet_id = self.input_pallet_id.text().strip()
                if not pallet_id:
                    QtWidgets.QMessageBox.warning(self, "Error", "Pallet ID is required.")
                    return

                payload = {
                    "pallet_id": pallet_id,
                    "pallet_type": self.input_pallet_type.text().strip(),
                    "condition": self.input_condition.text().strip(),
                    "adjust_reason": self.input_adjust_reason.text().strip(),
                    "requester": self.input_requester.text().strip(),
                    "location_id": self.location_name,
                    "pieces_on_hand": 0  # New pallets start empty
                }

            elif self.radio_content.isChecked():
                # 👉 Inserting Content
                item_id = self.input_item_code.text().strip()
                if not item_id:
                    QtWidgets.QMessageBox.warning(self, "Error", "Item Code is required.")
                    return

                payload = {
                    "owner": self.input_owner.text().strip(),
                    "item_id": item_id,
                    "description": self.input_description.text().strip(),
                    "serial_number": self.input_serial_number.text().strip(),
                    "lot": self.input_lot.text().strip(),
                    "tracking_date": self.input_tracking_date.date().toString("yyyy-MM-dd"),
                    "received_date": self.input_received_date.date().toString("yyyy-MM-dd"),
                    "pieces_on_hand": self.input_onhand.value(),
                }

                # Now check WHERE to insert the content
                if self.radio_location.isChecked():
                    payload["location_name"] = self.location_name
                elif self.radio_into_pallet.isChecked():
                    # We would need to ask for pallet_id from user
                    pallet_id, ok = QtWidgets.QInputDialog.getText(self, "Pallet ID", "Enter Pallet ID:")
                    if ok and pallet_id.strip():
                        payload["pallet_id"] = pallet_id.strip()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Pallet ID is required to insert into pallet.")
                        return
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Please select where to insert the content.")
                    return

            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select what to insert (Pallet or Content).")
                return

            # ✅ Now send the API request
            response = self.api_client.post("/a-contents/", json=payload)

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Inserted successfully!")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to insert.\n{response.text}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

