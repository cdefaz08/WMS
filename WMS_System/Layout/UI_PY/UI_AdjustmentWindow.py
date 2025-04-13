# UI_AdjustmentWindow.py
from PyQt5 import QtWidgets, QtGui, QtCore

class Ui_AdjustmentWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("AdjustmentWindow")
        Form.resize(900, 600)

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Tree View for pallets and items
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView, 2)

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

        self.horizontalLayout.addWidget(self.scrollArea, 3)