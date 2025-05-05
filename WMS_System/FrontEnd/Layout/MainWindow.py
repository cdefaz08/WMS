from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import pyqtSignal
import requests
import sys
from Layout.Inquiry.item_search import ItemSearchWindow
from Layout.Inquiry.Location_search import LocationSearchWindow
from Layout.Security.User_table import UsersTableWindow
from Layout.Maintance.itemMaintanceDialog import ItemMaintanceDialog
from Layout.Maintance.add_item_dialog import AddItemDialog
from Layout.configurations.LocationType_Win import LocationTypes
from Layout.Maintance.LocationType_Maintance import LocationType_Maintance
from Layout.Maintance.AddLocationType import AddLocationType
from Layout.configurations.rules.RuleClases import RuleClases
from Layout.Maintance.LocationMaintance import LocationMaintance
from Layout.Maintance.add_location import AddLocationDialog
from Layout.configurations.Proximities import ProximityWindow
from Layout.configurations.Vendors import VendorSearchWindow
from Layout.configurations.VendorMaintane import VendorMaintanceDialog
from Layout.configurations.order_type import OrderTypeWindow
from Layout.configurations.label_forms_window import FormManager
from Layout.Activities.OrderSearch import OrderSearchWindow
from Layout.Activities.OrderMaintance import OrderMaintanceWindow
from Layout.Activities.OrderLinesWindow import OrderLinesWindow
from Layout.Activities.ReceiptSearchWindow import ReceiptSearchWindow
from Layout.Activities.ReceiptMaintance import ReceiptMaintanceWindow
from Layout.Activities.ReceiptLinesWindow import ReceiptLinesWindow
from Layout.Maintance.ItemConfiguration import ItemConfigurationWindow
from Layout.Inquiry.InventorySearchWindow import InventorySearchWindow
from Layout.Activities.PO_Search import PurchaseOrderSearchWindow
from Layout.Adjustments.AdjustmentWindow import AdjustmentWindow
from Layout.Activities.purchase_order_maint_window import PurchaseOrderMaintWindow
from Layout.configurations.item_class_window import ItemClassWindow
from Layout.Activities.Retail_Sale_POS import RetailSaleWindow
from Layout.configurations.rules.GroupClases import GroupMaintanceWindow
from Layout.configurations.rules.GroupClassTableWindow import GroupClassTableWindow
from Layout.configurations.rules.RuleMaintance import RuleMaintance
from Layout.configurations.rules.Putaway_RuleSteps import PutawayStepsLogic
from Layout.Adjustments.InsertAdjusmetn import InsertIntoLocationWindow
from api_client import APIClient

class TrackingSubWindow(QMdiSubWindow):
    resized = pyqtSignal(int, int)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.size()
        self.resized.emit(size.width(), size.height())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,token = None, username = None):
        super().__init__()
        uic.loadUi("FrontEnd/UI/MainWindow.ui", self)
        self.token = token
        self.current_user = username
        self.api_client = APIClient(token)

        self.connect_toolbar()
        self.mdiArea = self.findChild(QtWidgets.QMdiArea, 'mdiArea')
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.actionLogout = self.findChild(QtWidgets.QAction, 'actionLogout')
        self.actionItem_Search = self.findChild(QtWidgets.QAction, 'actionItem_Search')
        self.actionUser_table = self.findChild(QtWidgets.QAction, 'actionUsers')
        self.actionLocation_Types = self.findChild(QtWidgets.QAction,"actionLocation_Types")
        self.actionactionRule_Clases = self.findChild(QtWidgets.QAction,"actionRule_Clases")
        self.actionRule_Groups = self.findChild(QtWidgets.QAction,"actionRule_Groups")
        self.actionNewLocation = self.findChild(QtWidgets.QAction,"actionNewLocation")
        self.actionLocation_Search = self.findChild(QtWidgets.QAction,"actionLocation_Search")
        self.actionProximity = self.findChild(QtWidgets.QAction, 'actionProximity')
        self.actionactionVendors = self.findChild(QtWidgets.QAction, "actionVendors")
        self.actionOrder_Types = self.findChild(QtWidgets.QAction, "actionOrder_Types")
        self.actionForms = self.findChild(QtWidgets.QAction, "actionForms")
        self.actionOrder_Search = self.findChild(QtWidgets.QAction, "actionOrder_Search")
        self.actionReceipt_Search = self.findChild(QtWidgets.QAction, "actionReceipt_Search")
        self.actionInventory_Adjustment = self.findChild(QtWidgets.QAction, "actionInventory_Adjustment")
        self.actionPurchase_Order_Search = self.findChild(QtWidgets.QAction, "actionPurchase_Order_Search")
        self.actionItem_Clases = self.findChild(QtWidgets.QAction, "actionItem_Clases")
        self.actionSales = self.findChild(QtWidgets.QAction, "actionSales")
        self.actionRule_Maintance = self.findChild(QtWidgets.QAction, "actionRule_Maintance")   


        self.actionLogout.triggered.connect(self.logout)
        self.actionItem_Search.triggered.connect(self.open_item_search)
        self.actionUser_table.triggered.connect(self.open_user_table)
        self.actionLocation_Types.triggered.connect(self.open_locationType_win)
        self.actionactionRule_Clases.triggered.connect(self.open_RuleClases)
        self.actionRule_Groups.triggered.connect(self.open_RuleGroups)

        self.actionNewLocation.triggered.connect(self.open_new_Location)
        self.actionLocation_Search.triggered.connect(self.open_location_search)  
        self.actionProximity.triggered.connect(self.open_proximity_window)
        self.actionVendors.triggered.connect(self.open_vendorSearch_window)
        self.actionOrder_Types.triggered.connect(self.open_order_type_window)
        self.actionForms.triggered.connect(self.open_forms_window)
        self.actionOrder_Search.triggered.connect(self.open_Order_Search)
        self.actionReceipt_Search.triggered.connect(self.open_Receipt_Search_window)
        self.actionInventory_Adjustment.triggered.connect(self.open_inventory_adjustment_window)
        self.actionPurchase_Order_Search.triggered.connect(self.open_purchase_order_search_window)
        self.actionItem_Clases.triggered.connect(self.open_item_class_window)
        self.actionSales.triggered.connect(self.open_retail_sale_window)
        self.actionRule_Maintance.triggered.connect(self.open_RuleMaintance)


    def open_mdi_window(self, widget_class, window_title,user = None, size=(600, 400),
                        reuse_existing=True, extra_setup=None, check_existing=True,
                        min_size=(400, 300), max_size=(800, 600)):
        is_type = isinstance(widget_class, type)

        if check_existing and is_type:
            for sub_window in self.mdiArea.subWindowList():
                if isinstance(sub_window.widget(), widget_class):
                    if reuse_existing:
                        sub_window.show()
                        sub_window.setFocus()
                        return sub_window

        if callable(widget_class):
            try:
                widget = widget_class(api_client=self.api_client, user=self.current_user)  # 🔐 intenta pasar api_client
            except TypeError:
                widget = widget_class()  # fallback si no acepta el parámetro
        else:
            widget = widget_class

        # ✅ Aplicar límites de tamaño al widget antes de insertarlo en el subwindow
        widget.setMinimumSize(*min_size)
        #widget.setMaximumSize(*max_size)

        # ✅ Crear y limitar el subwindow también
        sub_window = TrackingSubWindow()
        sub_window.setWindowFlags(QtCore.Qt.Window)
        sub_window.setMinimumSize(*min_size)
        sub_window.setMaximumSize(*max_size)

        sub_window.setWidget(widget)
        sub_window.resized.connect(lambda w, h: self.on_subwindow_resized(window_title, w, h))
        sub_window.setWindowTitle(window_title)
        sub_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        sub_window.resize(*size)

        if hasattr(widget, "parent_subwindow"):
            widget.parent_subwindow = sub_window

        if extra_setup:
            extra_setup(widget, sub_window)

        self.mdiArea.addSubWindow(sub_window)
        sub_window.show()

        return sub_window


    def on_subwindow_resized(self, title, width, height):
        print(f"📐 '{title}' resized to {width} x {height}")

    def open_user_table(self):
        self.open_mdi_window(UsersTableWindow(api_client=self.api_client), "User Search", size=(750, 400))

    def open_retail_sale_window(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)       
        self.open_mdi_window(RetailSaleWindow(api_client=self.api_client), "Retail Sale", user = self.current_user, size=(1617, 664), extra_setup=setup, min_size=(900, 600), max_size=(1700, 800))

    def open_proximity_window(self):
        self.open_mdi_window(ProximityWindow(api_client=self.api_client), "Proximity Search", size=(600, 400))
    
    def open_RuleGroups(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)        
        self.open_mdi_window(GroupMaintanceWindow(api_client=self.api_client), "Rule Groups", size=(600, 400), extra_setup=setup)

    def open_RuleMaintance(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)        
        self.open_mdi_window(RuleMaintance(api_client=self.api_client), "Rule Maintance", size=(634, 409), extra_setup=setup, min_size=(634, 335), max_size=(635, 600))

    def open_locationType_win(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(LocationTypes(api_client=self.api_client), "Location Types", size=(500, 600), extra_setup=setup)

    def open_item_class_window(self):
        self.open_mdi_window(ItemClassWindow(api_client=self.api_client), "Item Clases", size = (580, 600))

    def open_order_type_window(self):
        self.open_mdi_window(OrderTypeWindow(api_client=self.api_client), "Order Types", size = (700, 400))

    def open_item_search(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(ItemSearchWindow(api_client=self.api_client), "Item Search", size=(1089, 720), extra_setup=setup,min_size=(1580, 531), max_size=(1818, 867))
    
    def open_purchase_order_search_window(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(PurchaseOrderSearchWindow(api_client=self.api_client), "Purchase Order Search", size=(1089, 720), extra_setup=setup,min_size=(697, 459), max_size=(1140, 850))

    def open_Order_Search(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(OrderSearchWindow(api_client=self.api_client), "Order Search", size=(1089, 720), extra_setup=setup,min_size=(697, 459), max_size=(1081, 874))

    def open_Receipt_Search_window(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(ReceiptSearchWindow(api_client=self.api_client), "Receipt Search", size=(1089, 720), extra_setup=setup,min_size=(697, 459), max_size=(1081, 874))

    def open_inventory_adjustment_window(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(
            lambda: InventorySearchWindow(api_client=self.api_client), "Inventory Search", size=(1580, 720), extra_setup=setup,min_size=(1580, 535), max_size=(1301, 899))

    def open_location_search(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(
            lambda: LocationSearchWindow(api_client=self.api_client), "Location Search", size=(1089, 720), extra_setup=setup,min_size=(1030, 677), max_size=(1223, 885))

    def open_vendorSearch_window(self):
        def setup(widget, sub_window):
            self.mdiArea.subWindowActivated.connect(self.handle_subwindow_focus_change)
            self.actionItemMaintance.setVisible(True)
            widget.destroyed.connect(self.hide_item_toolbar_action)
        self.open_mdi_window(
            lambda: VendorSearchWindow(api_client=self.api_client), "Vendor Search", size=(1089, 720), extra_setup=setup,min_size=(697, 459), max_size=(1135, 678))

    def open_RuleClases(self):
        self.open_mdi_window(RuleClases(api_client=self.api_client), "Rule Clases", size=(600, 500))

    def open_forms_window(self):
        self.open_mdi_window(FormManager(api_client=self.api_client), "Forms", size= (606,458))

    def open_new_Location(self):
        self.open_mdi_window(
            lambda: AddLocationDialog(api_client=self.api_client), "New Location", size=(710, 715),min_size=(697, 459), max_size=(1135, 678))

    def get_active_window(self):
        active_subwindow = self.mdiArea.activeSubWindow()
        if active_subwindow:
            return active_subwindow.widget()
        return None

    def logout(self):
        confirm = QtWidgets.QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.close()

    def connect_toolbar(self):
        self.new_button = self.findChild(QtWidgets.QAction, 'actionNew')
        self.save_button = self.findChild(QtWidgets.QAction, 'actionSave')
        self.discard_button = self.findChild(QtWidgets.QAction, 'actionDiscard')
        self.refresh_button = self.findChild(QtWidgets.QAction, 'actionRefresh')
        self.actionItemMaintance = self.findChild(QtWidgets.QAction, "actionItemMaintance")
        self.delete_button = self.findChild(QtWidgets.QAction,"actionDelete")
        self.actionOrderLines = self.findChild(QtWidgets.QAction,"actionOrderLines")
        self.actionAdjustment = self.findChild(QtWidgets.QAction,"actionAdjustment")
        self.actionAdjustment.setVisible(False)
        self.actionItemMaintance.setVisible(False)
        self.actionOrderLines.setVisible(False)
        self.actionAdjustment.triggered.connect(self.toolbar_adjustment)
        self.new_button.triggered.connect(self.toolbar_new)
        self.save_button.triggered.connect(self.toolbar_save)
        self.refresh_button.triggered.connect(self.toolbar_refresh)
        self.delete_button.triggered.connect(self.toolbar_delete)
        self.discard_button.triggered.connect(self.toolbar_discard)
        self.actionItemMaintance.triggered.connect(self.open_maintance_window)
        self.actionOrderLines.triggered.connect(self.open_OrderLines_window)

    def toolbar_adjustment(self):
        active_window = self.get_active_window()

        if isinstance(active_window, (LocationSearchWindow, InventorySearchWindow)):
            location_id = active_window.get_selected_location_id()

            if location_id:
                try:
                    # 1. Get the adjustments data (contents of that location)
                    response = self.api_client.get(f"/a-contents/by-location/?location_id={location_id}")

                    # 2. Get location details (to get location name + location type rules)
                    response_location = self.api_client.get(f"/locations/{location_id}")

                    if response.status_code == 200 and response_location.status_code == 200:
                        adjustments_data = response.json()
                        location_info = response_location.json()

                        location_name = location_info.get("location_id", "Unknown Location")
                        location_type_id = location_info.get("location_type")

                        # 3. Now get the location type rules
                        response_location_type = self.api_client.get(f"/location-types/{location_type_id}")

                        if response_location_type.status_code == 200:
                            location_type_info = response_location_type.json()

                            # Extract rules
                            location_type_rules = {
                                "mix_items": location_type_info.get("mix_items", True),
                                "mix_configurations": location_type_info.get("mix_configurations", True),
                                "mix_track_date": location_type_info.get("mix_track_date", True),
                                "mix_receiving_date": location_type_info.get("mix_receiving_date", True),
                                "allow_picking_pallet": location_type_info.get("allow_picking_pallet", True),
                                "allow_picking_carton": location_type_info.get("allow_picking_carton", True),
                                "allow_picking_pieces": location_type_info.get("allow_picking_pieces", True),
                                "storage_pallet": location_type_info.get("storage_pallet", True),
                                "storage_carton": location_type_info.get("storage_carton", False),
                                "storage_content": location_type_info.get("storage_content", False),
                                "merge": location_type_info.get("merge", True),
                            }

                            # 4. Finally open Adjustment Window with everything
                            self.open_mdi_window(
                                lambda: AdjustmentWindow(
                                    adjustments_data=adjustments_data,
                                    api_client=self.api_client,
                                    location_name=location_name,
                                    location_type_rules=location_type_rules,
                                    parent=self,
                                ),
                                "Inventory Adjustments",
                                size=(800, 600),
                                min_size=(697, 459),
                                max_size=(799, 569),
                                extra_setup=lambda w, s: setattr(w, "parent_subwindow", s),
                            )
                        else:
                            QtWidgets.QMessageBox.warning(
                                self, "Error", "Could not load location type details from server."
                            )
                    else:
                        QtWidgets.QMessageBox.warning(
                            self, "Error", "Could not load adjustments or location details."
                        )

                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(
                        self, "Error", "Could not connect to the server."
                    )

            else:
                QtWidgets.QMessageBox.warning(
                    self, "No Selection", "Please select a location from the table."
                )


    def toolbar_new(self):
        active_window = self.get_active_window()
        if isinstance(active_window, ItemSearchWindow):
            self.open_mdi_window(AddItemDialog, "Add New Item", size=(805, 569),min_size=(697, 459), max_size=(1072, 700))
        elif isinstance(active_window , LocationTypes):
            self.open_mdi_window(AddLocationType, "Add New Location Type", size=(902, 384))
        elif isinstance(active_window, UsersTableWindow):
            active_window.add_new_user()
        elif isinstance(active_window, RuleClases):
            active_window.add_new_row()
        elif isinstance(active_window, LocationSearchWindow):
            self.open_mdi_window(AddLocationDialog(api_client=self.api_client), "Add New Location", size=(900, 800),min_size=(800 , 600), max_size=(940, 900))
        elif isinstance(active_window, ProximityWindow):
            active_window.add_new_row()
        elif isinstance(active_window, VendorSearchWindow):
            self.open_mdi_window(VendorMaintanceDialog, "Add New Vendor", size=(800, 320))
        elif isinstance(active_window, OrderTypeWindow):
            active_window.add_new_row()
        elif isinstance(active_window, FormManager):
            active_window.add_new_row()
        elif isinstance(active_window, OrderSearchWindow):
            self.open_mdi_window(OrderMaintanceWindow, "Add New Order", size=(1200, 612))
        elif isinstance(active_window, OrderMaintanceWindow):
            current_tab = active_window.tabWidget.currentWidget()
            if isinstance(current_tab, OrderLinesWindow):
                current_tab.add_new_blank_row()
            else:
                active_window.add_new_row()
        elif isinstance(active_window, ReceiptSearchWindow):
            self.open_mdi_window(ReceiptMaintanceWindow(api_client= self.api_client), "Add New Receipt", size=(1072, 700),min_size=(697, 459), max_size=(1072, 700),)
        elif isinstance(active_window, ReceiptMaintanceWindow):
            current_tab = active_window.tabWidget.currentWidget()
            if isinstance(current_tab, ReceiptLinesWindow):
                current_tab.add_new_blank_row()
            else:
                active_window.add_new_row()
        elif isinstance(active_window, ItemConfigurationWindow):
            active_window.add_configuration_block()
        elif isinstance(active_window,PurchaseOrderMaintWindow):
            active_window.add_order_line_row()
        elif isinstance(active_window,PurchaseOrderSearchWindow):
            self.open_mdi_window(PurchaseOrderMaintWindow,"Add New Purchase Order",size=(1000, 710),min_size=(697, 459), max_size=(1072, 617),)
        elif isinstance(active_window,ItemClassWindow):
            active_window.add_empty_row()
        elif isinstance(active_window , GroupMaintanceWindow): 
            active_window.add_new_row_to_current_tab()
        elif isinstance(active_window , GroupClassTableWindow):
            active_window.add_empty_row()
        elif isinstance(active_window, RuleMaintance):
            active_window.add_empty_row(active_window.tab_widget.currentWidget())
        elif isinstance(active_window,PutawayStepsLogic):
            active_window.add_empty_row()
        elif isinstance(active_window, AdjustmentWindow):
            

            self.open_mdi_window(
                lambda: InsertIntoLocationWindow(
                    api_client=self.api_client,
                    user = self.current_user,
                    location_name=active_window.location_name,
                    location_type_rules=active_window.location_type_rules,
                    parent=self,
                ),
                window_title="Insert Into Location",
                size=(600, 500),       # <- suggest a good size for the Insert window
                min_size=(400, 300),    # <- minimum size allowed
                max_size=(800, 600),    # <- optional max size
            )
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    def toolbar_save(self):
        active_window = self.get_active_window()
        if isinstance(active_window, UsersTableWindow):
            active_window.save_changes()
        elif isinstance(active_window, ItemMaintanceDialog):
            active_window.save_changes()
        elif isinstance(active_window, AddItemDialog):
            active_window.createItem()
        elif isinstance(active_window, LocationType_Maintance):
            active_window.save_changes()
        elif isinstance(active_window, AddLocationType):
            active_window.save_changes()
        elif isinstance(active_window, RuleClases):
            active_window.save_changes()
        elif isinstance(active_window, LocationMaintance):
            active_window.save_changes()
        elif isinstance(active_window, AddLocationDialog):
            active_window.save_new_location()
        elif isinstance(active_window, ProximityWindow):
            active_window.save_changes()
        elif isinstance(active_window,VendorMaintanceDialog):
            active_window.save_changes()
        elif isinstance(active_window, OrderTypeWindow):
            active_window.save_changes()
        elif isinstance(active_window, FormManager):
            active_window.save_changes()
        elif isinstance(active_window, OrderMaintanceWindow):
            active_window.save_all()
        elif isinstance(active_window, ReceiptMaintanceWindow):
            active_window.save_all()
        elif isinstance(active_window,ItemConfigurationWindow):
            active_window.save_all_configurations()
        elif isinstance(active_window,PurchaseOrderMaintWindow):
            active_window.save_changes()
        elif isinstance(active_window,ItemClassWindow):
            active_window.save_changes()
        elif isinstance(active_window,GroupMaintanceWindow): 
            active_window.save_current_tab_changes()
        elif isinstance(active_window,GroupClassTableWindow):
            active_window.save_changes()
        elif isinstance(active_window,RuleMaintance):
            active_window.save_changes(active_window.tab_widget.currentWidget())
        elif isinstance(active_window,PutawayStepsLogic):
            active_window.save_changes()
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    def toolbar_delete(self):
        active_window = self.get_active_window()
        if isinstance(active_window, UsersTableWindow):
            active_window.delete_selection()
        elif isinstance(active_window, RuleClases):
            active_window.delete_selected_row()
        elif isinstance(active_window, ItemSearchWindow):
            active_window.delete_selected_item()
        elif isinstance(active_window, LocationSearchWindow):
            active_window.delete_selected_location()
        elif isinstance(active_window, ProximityWindow):
            active_window.delete_selected_row()
        elif isinstance(active_window, VendorSearchWindow):
            active_window.delete_selected_vendor()
        elif isinstance(active_window, OrderTypeWindow):
            active_window.delete_selected_row()
        elif isinstance(active_window, FormManager):
            active_window.delete_selected_row()
        elif isinstance(active_window, OrderMaintanceWindow):
            current_tab = active_window.tabWidget.currentWidget()
            if isinstance(current_tab, OrderLinesWindow):
                current_tab.delete_selected_row()
            else:
                active_window.delete_selected()
        elif isinstance(active_window, ReceiptMaintanceWindow):
            current_tab = active_window.tabWidget.currentWidget()
            if isinstance(current_tab, ReceiptLinesWindow):
                current_tab.delete_selected_row()
            else:
                active_window.delete_row()
        elif isinstance(active_window,ReceiptSearchWindow):
            active_window.delete_selected_receipt()
        elif isinstance(active_window,ItemConfigurationWindow):
            active_window.delete_selected_configuration()
        elif isinstance(active_window,PurchaseOrderMaintWindow):
            active_window.delete_selected_order_line()
        elif isinstance(active_window,ItemClassWindow):
            active_window.delete_selected_row()
        elif isinstance(active_window,PurchaseOrderSearchWindow):
            active_window.delete_selected_po()
        elif isinstance(active_window,GroupMaintanceWindow): 
            active_window.delete_selected_group()
        elif isinstance(active_window,GroupClassTableWindow):
            active_window.delete_selected_row()       
        elif isinstance(active_window,RuleMaintance):    
            active_window.delete_selected_row(active_window.tab_widget.currentWidget())
        elif isinstance(active_window,PutawayStepsLogic):
            active_window.delete_selected_row()
        else:
            QtWidgets.QMessageBox.warning(self,"No Active Window", "Please select a window First")

    def toolbar_discard(self):
        active_window = self.get_active_window()
        if isinstance(active_window, UsersTableWindow):
            active_window.discard_users()
        elif isinstance(active_window, ItemSearchWindow):
            active_window.clear_filters()
        elif isinstance(active_window, LocationSearchWindow):
            active_window.clear_filters()
        elif isinstance(active_window, VendorSearchWindow):
            active_window.clear_filters()
        else:
            QtWidgets.QMessageBox.warning(self, "No Active Window", "Please select a window first.")

    def toolbar_refresh(self):
        active_window = self.get_active_window()
        if isinstance(active_window, LocationTypes):
            active_window.load_location_types()
        elif isinstance(active_window, RuleClases):
            active_window.load_data()
        elif isinstance(active_window,GroupClassTableWindow):
            active_window.refresh_data()
        
        else:
            QtWidgets.QMessageBox.warning(self,"No Active Window", "Please select a window First")

    def hide_item_toolbar_action(self):
        self.actionItemMaintance.setVisible(False)
        self.actionOrderLines.setVisible(False)

    def open_maintance_window(self):
        active_window = self.get_active_window()
        if isinstance(active_window, ItemSearchWindow):
            item_id = active_window.get_selected_item_id()
            if item_id:
                try:
                    response = self.api_client.get(f"/items/{item_id}")
                    if response.status_code == 200:
                        item_data = response.json()
                        self.open_mdi_window(
                            lambda: ItemMaintanceDialog(api_client=self.api_client, item_data=item_data, parent=self),
                            "Item Code Maintanance", size=(700, 600),min_size=(697, 459), max_size=(799, 569),
                            extra_setup=lambda w, s: w.item_updated.connect(active_window.search_items)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window, GroupMaintanceWindow):
            group_name, group_type = active_window.get_selected_group_info()
            if group_name and group_type:
                try:
                    # Lógica: endpoint depende del tipo de grupo
                    response = self.api_client.get(f"/group-classes/{group_type}/")
                    if response.status_code == 200:
                        all_group_class_data = response.json()

                        # 🔍 Filtrar las clases por group_name
                        group_data = [r for r in all_group_class_data if r["group_name"] == group_name]
                    else:
                        group_data = []
                except Exception as e:
                    group_data = []
                    QtWidgets.QMessageBox.warning(self, "Warning", f"Could not load group classes:\n{str(e)}")

                # 🪟 Abrir la ventana de configuración, con datos o vacía
                self.open_mdi_window(
                    lambda: GroupClassTableWindow(
                        api_client=self.api_client,
                        group_name=group_name,
                        group_type=group_type,
                        group_data=group_data,
                        parent=self
                    ), f"{group_name} Group Classes",
                    size=(428, 399)
                )

        elif isinstance(active_window, OrderSearchWindow):
            order_id = active_window.get_selected_order_id()
            if order_id:
                try:
                    response = self.api_client.get(f"/orders/{order_id}")
                    if response.status_code == 200:
                        order_data = response.json()
                        self.open_mdi_window(
                            lambda: OrderMaintanceWindow(order_data=order_data,api_client=self.api_client, parent=self),
                            "Order Maintanance",
                            size=(1072, 617) ,min_size=(697, 459), max_size=(1072, 617),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window, ReceiptSearchWindow):
            receipt_id = active_window.get_selected_receipt_id()
            if receipt_id:
                try:
                    response = self.api_client.get(f"/receipts/{receipt_id}")
                    if response.status_code == 200:
                        receipt_data = response.json()
                        self.open_mdi_window(
                            lambda: ReceiptMaintanceWindow(receipt_data=receipt_data, api_client=self.api_client, parent=self),
                            "Receipt Maintanance",
                            size=(1072, 700),min_size=(697, 459), max_size=(1072, 700),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")

        elif isinstance(active_window , LocationTypes):
            location_type_id = active_window.get_selected_item_id()
            if location_type_id:
                try:
                    response = self.api_client.get(f"/location-types/{location_type_id}")
                    if response.status_code == 200:
                        locationTypeData = response.json()
                        self.open_mdi_window(
                            lambda: LocationType_Maintance(api_client= self.api_client, 
                                                           locationTypeData=locationTypeData,
                                                            parent=self),
                            "Location Type Maintanance",
                            size=(902, 384),
                            check_existing=False
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window, LocationSearchWindow):
            location_id = active_window.get_selected_location_id()
            if location_id:
                try:
                    response = self.api_client.get(f"/locations/{location_id}")
                    if response.status_code == 200:
                        location_data = response.json()
                        self.open_mdi_window(
                            lambda: LocationMaintance(api_client=self.api_client, location_data=location_data, parent=self),
                            "Location Maintanance",
                            size=(900, 800),min_size=(800 , 600), max_size=(940, 900),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window,VendorSearchWindow):
            vendor_id = active_window.get_selected_vendor_id()
            if vendor_id:
                try:
                    response = self.api_client.get(f"/vendors/{vendor_id}")
                    if response.status_code == 200:
                        vendor_data = response.json()
                        self.open_mdi_window(
                            lambda: VendorMaintanceDialog(api_client=self.api_client, vendor_data=vendor_data, parent=self),
                            "Vendor Maintanance",
                            size=(800, 400),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.") 
        elif isinstance(active_window,PurchaseOrderSearchWindow):
            purchase_order_id = active_window.get_selected_po_id()
            if purchase_order_id:
                try:
                    response = self.api_client.get(f"/purchase-orders/{purchase_order_id}")
                    if response.status_code == 200:
                        po_data = response.json()
                        self.open_mdi_window(
                            lambda: PurchaseOrderMaintWindow(po_data=po_data, api_client=self.api_client, parent=self),
                            "Purchase Order Maintanance",
                            size=(1000, 759),min_size=(800, 759), max_size=(1100, 780),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")               
        elif isinstance(active_window, RuleMaintance):
            rule_id, rule_type = active_window.get_selected_rule_info()
            print(f"rule id:{rule_id}, rule_type {rule_type}")
            if rule_id:
                try:
                    response = self.api_client.get(f"/rules_steps/{rule_type}/{rule_id}")
                    if response.status_code == 200:
                        rule_data = response.json()
                    else:
                        rule_data = {"rule_name": f"{rule_type.upper()} Rule"}
                except Exception:
                    rule_data = {"rule_name": f"{rule_type.upper()} Rule"}

                # Abrir la ventana según el tipo
                if rule_type == "putaway-rule-steps":
                    self.open_mdi_window(
                        lambda: PutawayStepsLogic(
                            api_client=self.api_client,
                            rule_id=rule_id
                        ),
                        "Putaway Steps",
                        size=(1405, 348),min_size=(1317, 200), max_size=(1317, 500),
                    )
                elif rule_type == "restock":
                    self.open_mdi_window(
                        lambda: PutawayStepsLogic( #cambiar a RestockStepsLogic
                            api_client=self.api_client,
                            rule_id=rule_id,
                            rule_name=rule_data["rule_name"]
                        ),
                        "Restock Steps"
                    )
                elif rule_type == "pick":
                    self.open_mdi_window(
                        lambda: PutawayStepsLogic( #cambiar a PickStepsLogic
                            api_client=self.api_client,
                            rule_id=rule_id,
                            rule_name=rule_data["rule_name"]
                        ),
                        "Pick Steps"
                    )
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a rule from the table.")



    
    def open_OrderLines_window(self):
        active_window = self.get_active_window()
        if isinstance(active_window, OrderMaintanceWindow):
            order_number = active_window.get_order_number()
            if order_number:
                try:
                    response = self.api_client.get(f"/order-lines/by-order/{order_number}")
                    if response.status_code == 200:
                        self.open_mdi_window(
                            lambda: OrderLinesWindow(order_number=order_number, api_client=self.api_client, parent=self),
                            "Order Lines",
                            size=(800,300),min_size=(697, 459), max_size=(1265, 374),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")       
        elif isinstance(active_window, ReceiptMaintanceWindow):
            receipt_number = active_window.get_receipt_number()
            if receipt_number:
                try:
                    response = self.api_client.get(f"/receipt-lines/by-receipt/{receipt_number}")
                    if response.status_code == 200:
                        self.open_mdi_window(
                            lambda: ReceiptLinesWindow(receipt_number=receipt_number, api_client=self.api_client, parent=self),
                            "Receipt Lines",
                            size=(800,300),min_size=(697, 459), max_size=(1265, 374),
                            extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                        )
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")
            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")
        elif isinstance(active_window, ItemMaintanceDialog):
            item_id = active_window.get_item_id()
            if item_id:
                try:
                    response = self.api_client.get(f"/item-config/items/{item_id}/configurations")

                    if response.status_code == 200:
                        item_config = response.json()
                    elif response.status_code == 404:
                        # No configurations found for this item → abrimos ventana vacía
                        item_config = []
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Could not load item from server.")
                        return

                    self.open_mdi_window(
                        lambda: ItemConfigurationWindow(
                            item_config=item_config,
                            item_name=item_id,
                            api_client=self.api_client,
                            parent=self
                        ),
                        "Item Configurations",
                        size=(1100, 700),
                        min_size=(697, 459),
                        max_size=(1047, 1000),
                        extra_setup=lambda w, s: setattr(w, "parent_subwindow", s)
                    )

                except requests.exceptions.RequestException:
                    QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to the server.")

            else:
                QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item from the table.")

    def handle_subwindow_focus_change(self, active_subwindow):
        self.actionItemMaintance.setVisible(False)
        self.actionOrderLines.setVisible(False)
        self.actionAdjustment.setVisible(False)

        if not active_subwindow:
            return

        widget = active_subwindow.widget()

        if isinstance(widget, (
            ItemSearchWindow,
            GroupMaintanceWindow, 
            LocationTypes, 
            VendorSearchWindow,
            OrderSearchWindow,
            ReceiptSearchWindow,
            PurchaseOrderSearchWindow,
            RuleMaintance)):
            self.actionItemMaintance.setVisible(True)
        elif isinstance(widget, (OrderMaintanceWindow,ReceiptMaintanceWindow,ItemMaintanceDialog)):
            self.actionOrderLines.setVisible(True)
        elif isinstance(widget, (LocationSearchWindow,InventorySearchWindow)):
            self.actionItemMaintance.setVisible(True)
            self.actionAdjustment.setVisible(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
