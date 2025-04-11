from PyQt5 import QtWidgets, QtCore
from Layout.UI_PY.UI_OrderMaintance import Ui_OrderMaintance
import requests
from config import API_BASE_URL
from datetime import datetime
from Layout.Activities.OrderLinesWindow import OrderLinesWindow

class OrderMaintanceWindow(QtWidgets.QDialog, Ui_OrderMaintance):
    def __init__(self,api_client = None, order_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.api_client = api_client
        self.order_data = order_data
        self.lineEdit_CreatedBy.setReadOnly(True)
        self.lineEdit_Status.setReadOnly(True)
        self.lineEdit_CreatedBy.setStyleSheet("background-color: #f0f0f0;")
        self.lineEdit_Status.setStyleSheet("background-color: #f0f0f0;")
        self.dateEdit_OrderDate.setCalendarPopup(True)
        self.dateEdit_ShipDate.setCalendarPopup(True)



        self.original_data = order_data.copy() if order_data else {}

        self.dateEdit_OrderDate.setDisplayFormat("MM/dd/yyyy")
        self.dateEdit_ShipDate.setDisplayFormat("MM/dd/yyyy")
        self.init_order_lines_tab_if_ready()

        if not self.order_data:
            self.dateEdit_OrderDate.setDate(QtCore.QDate.currentDate())

        self.setWindowTitle("Edit Order" if self.order_data else "Create Order")

        self.load_order_dropdowns()

        if not order_data:
            # Capture accurate default state after all dropdowns are loaded
            self.original_data = self.collect_form_data()


        self.load_order_dropdowns()

    def init_order_lines_tab_if_ready(self):
        if not self.order_data:
            self.tabWidget.setTabEnabled(self.tabWidget.count() - 1, False)
            return  # ⛔️ No hay datos aún, no hagas nada

        order_number = self.order_data.get("order_number")
        if order_number:
            self.order_lines_tab = OrderLinesWindow(order_number=order_number, api_client=self.api_client)
            self.tabWidget.addTab(self.order_lines_tab, "Order Lines")
        else:
            self.tabWidget.setTabEnabled(self.tabWidget.count() - 1, False)


    def load_order_dropdowns(self):
        try:
            order_types_response = self.api_client.get(f"/order_types")
            if order_types_response.status_code == 200:
                order_types = order_types_response.json()
                self.comboBox_OrderType.clear()
                for ot in order_types:
                    self.comboBox_OrderType.addItem(ot["order_type"])

            label_forms_response = self.api_client.get(f"/label_forms")
            if label_forms_response.status_code == 200:
                label_forms = label_forms_response.json()
                self.comboBox_Label_Form.clear()
                for lf in label_forms:
                    self.comboBox_Label_Form.addItem(lf["label_form"])

            document_forms_response = self.api_client.get(f"/document_forms")
            if document_forms_response.status_code == 200:
                document_forms = document_forms_response.json()
                self.comboBox_Doc_Form.clear()
                for df in document_forms:
                    self.comboBox_Doc_Form.addItem(df["document_form"])

            if self.order_data:
                self.populate_fields()

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo cargar los datos de dropdowns.\n{str(e)}")

    def populate_fields(self):
        data = self.order_data
        self.lineEdit_order_number.setText(data.get("order_number", ""))
        self.lineEdit_customer_name.setText(data.get("customer_name", ""))
        self.comboBox_OrderType.setCurrentText(data.get("order_type", ""))
        self.comboBox_Label_Form.setCurrentText(data.get("label_form", ""))
        self.comboBox_Doc_Form.setCurrentText(data.get("document_form", ""))

        order_date = self.safe_parse_date(data.get("order_date"))
        ship_date = self.safe_parse_date(data.get("ship_date"))
        if order_date:
            self.dateEdit_OrderDate.setDate(order_date)
        if ship_date:
            self.dateEdit_ShipDate.setDate(ship_date)

        self.lineEdit_CreatedBy.setText(str(data.get("created_by", "")))
        self.lineEdit_Status.setText(data.get("status", ""))
        self.lineEdit_Carrier.setText(data.get("carrier", ""))
        self.lineEdit_Ship_method.setText(data.get("ship_method", ""))

        self.lineEdit_Store.setText(data.get("Store", ""))
        self.lineEdit_InvoiceNumber.setText(data.get("InvoiceNumber", ""))
        self.lineEdit_Vendor_num.setText(data.get("Vendor_num", ""))

        self.lineEdit_shp_to_City.setText(data.get("shp_to_City", ""))
        self.lineEdit_shp_to_State.setText(data.get("shp_to_State", ""))
        self.lineEdit_shp_to_ZipCode.setText(data.get("shp_to_ZipCode", ""))
        self.lineEdit_shp_to_Country.setText(data.get("shp_to_Country", ""))
        self.lineEdit_shp_to_ContactName.setText(data.get("shp_to_ContactName", ""))
        self.lineEdit_shp_to_ContactPhone.setText(data.get("shp_to_ContactPhone", ""))
        self.lineEdit_shp_to_TaxId.setText(data.get("shp_to_TaxId", ""))
        self.lineEdit_shp_to_Company.setText(data.get("shp_to_Company", ""))
        self.lineEdit_shp_to_Addres2.setText(data.get("shp_to_Address", ""))

        self.lineEdit_bill_to_City.setText(data.get("bill_to_City", ""))
        self.lineEdit_bill_to_State.setText(data.get("bill_to_State", ""))
        self.lineEdit_bill_to_ZipCode.setText(data.get("bill_to_ZipCode", ""))
        self.lineEdit_bill_to_Country.setText(data.get("bill_to_Country", ""))
        self.lineEdit_bill_to_ContactName.setText(data.get("bill_to_ContactName", ""))
        self.lineEdit_bill_to_ContactPhone.setText(data.get("bill_to_ContactPhone", ""))
        self.lineEdit_bill_to_TaxId.setText(data.get("bill_to_TaxId", ""))
        self.lineEdit_bill_to_Company.setText(data.get("bill_to_Company", ""))
        self.lineEdit_bill_to_Addres2.setText(data.get("bill_to_Address", ""))

        self.lineEdit_custom_1.setText(data.get("custom_1", ""))
        self.lineEdit_custom_2.setText(data.get("custom_2", ""))
        self.lineEdit_custom_3.setText(data.get("custom_3", ""))
        self.lineEdit_custom_4.setText(data.get("custom_4", ""))
        self.lineEdit_custom_5.setText(data.get("custom_5", ""))

    def has_unsaved_changes(self):
        current = self.collect_form_data()
        original = self.original_data or {}

        for key in current:
            current_value = str(current.get(key, "")).strip()
            original_value = str(original.get(key, "")).strip()

            # ✅ Normalizar fechas con hora tipo ISO
            if "date" in key.lower() and "T" in original_value:
                original_value = original_value.split("T")[0]

            if current_value != original_value:
                print(f"🔄 Diferencia en '{key}': '{original_value}' vs '{current_value}'")
                return True

        return False



    def safe_parse_date(self, date_str):
        if date_str:
            try:
                return QtCore.QDate.fromString(date_str, QtCore.Qt.ISODate)
            except Exception:
                return QtCore.QDate.currentDate()
        return QtCore.QDate.currentDate()

    def collect_form_data(self):
        def get(field):
            widget = getattr(self, f"lineEdit_{field}", None)
            return widget.text().strip() if widget else ""

        def get_combo(field): return getattr(self, f"comboBox_{field}", None).currentText().strip()
        def get_date(widget): return widget.date().toString("yyyy-MM-dd")

        data = {
            "order_number": get("order_number"),
            "customer_name": get("customer_name"),
            "order_type": get_combo("OrderType"),
            "label_form": get_combo("Label_Form"),
            "document_form": get_combo("Doc_Form"),
            "order_date": get_date(self.dateEdit_OrderDate),
            "ship_date": get_date(self.dateEdit_ShipDate),
            "created_by": int(get("CreatedBy")) if get("CreatedBy").isdigit() else None,
            "status": get("Status"),
            "carrier": get("Carrier"),
            "ship_method": get("Ship_method"),
            "Store": get("Store"),
            "InvoiceNumber": get("InvoiceNumber"),
            "Vendor_num": get("Vendor_num"),
            "shp_to_City": get("shp_to_City"),
            "shp_to_State": get("shp_to_State"),
            "shp_to_ZipCode": get("shp_to_ZipCode"),
            "shp_to_Country": get("shp_to_Country"),
            "shp_to_ContactName": get("shp_to_ContactName"),
            "shp_to_ContactPhone": get("shp_to_ContactPhone"),
            "shp_to_TaxId": get("shp_to_TaxId"),
            "shp_to_Company": get("shp_to_Company"),
            "shp_to_Address": get("shp_to_Addres2"),
            "bill_to_City": get("bill_to_City"),
            "bill_to_State": get("bill_to_State"),
            "bill_to_ZipCode": get("bill_to_ZipCode"),
            "bill_to_Country": get("bill_to_Country"),
            "bill_to_ContactName": get("bill_to_ContactName"),
            "bill_to_ContactPhone": get("bill_to_ContactPhone"),
            "bill_to_TaxId": get("bill_to_TaxId"),
            "bill_to_Company": get("bill_to_Company"),
            "bill_to_Address": get("bill_to_Addres2"),
            "custom_1": get("custom_1"),
            "custom_2": get("custom_2"),
            "custom_3": get("custom_3"),
            "custom_4": get("custom_4"),
            "custom_5": get("custom_5"),
        }
        return {k: v for k, v in data.items() if v not in [None, ""]}
    
    def get_updated_fields(self):
        updated = {}
        current_data = self.collect_form_data()

        for key, current_value in current_data.items():
            original_value = self.original_data.get(key, "")
            if str(current_value).strip() != str(original_value).strip():
                updated[key] = current_value

        return updated


    def save_order(self):
        if self.order_data and "id" in self.order_data:
            updated_data = self.get_updated_fields()
            if not updated_data:
                QtWidgets.QMessageBox.information(self, "No Changes", "No fields were modified.")
                return
            response = self.api_client.put(f"/orders/{self.order_data['id']}", json=updated_data)
        else:
            full_data = self.collect_form_data()
            response = self.api_client.post(f"/orders", json=full_data)

        if response.status_code in (200, 201):
            QtWidgets.QMessageBox.information(self, "Success", "Order saved successfully.")
            self.original_data = self.original_data | (self.collect_form_data() if not self.order_data else self.get_updated_fields())
            mdi = self.parent()
            while mdi and not isinstance(mdi, QtWidgets.QMdiSubWindow):
                mdi = mdi.parent()
            if mdi:
                mdi.close()
            else:
                self.close()  
        else:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to save order: {response.text}")

    def get_order_number(self):
        """
        Returns the current order number from the field.
        If the window was loaded with order_data, it will return the saved value.
        """
        if self.order_data and "order_number" in self.order_data:
            return self.order_data["order_number"]
        
        # Fallback: get from the input field (in case it's a new order)
        return self.lineEdit_order_number.text().strip()


    def closeEvent(self, event):
        if self.has_unsaved_changes():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you really want to close?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
