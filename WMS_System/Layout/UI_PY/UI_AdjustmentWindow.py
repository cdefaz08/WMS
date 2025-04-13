from PyQt5 import QtWidgets, QtCore

class Ui_AdjustmentWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("AdjustmentWindow")
        Form.resize(900, 600)

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Tree Widget (QTreeWidget instead of QTreeView to allow top-level items)
        self.tree_widget = QtWidgets.QTreeWidget(Form)
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(["PALLET ID", "ITEM CODE", "QTY"])
        self.horizontalLayout.addWidget(self.tree_widget, 3)

        # Scrollable area with detail panel
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollContent = QtWidgets.QWidget()
        self.scrollContent.setGeometry(QtCore.QRect(0, 0, 400, 580))
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.scrollLayout.setObjectName("scrollLayout")

        self.groupBoxDetails = QtWidgets.QGroupBox(self.scrollContent)
        self.groupBoxDetails.setTitle("Details")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxDetails)
        self.formLayout.setObjectName("formLayout")

        self.scrollLayout.addWidget(self.groupBoxDetails)
        self.scrollArea.setWidget(self.scrollContent)

        self.horizontalLayout.addWidget(self.scrollArea,3 )