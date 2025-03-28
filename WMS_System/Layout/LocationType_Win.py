from PyQt5 import QtWidgets, uic, QtCore 
import requests
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class LocationTypes(QtWidgets.QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        uic.loadUi("UI/locationTypes.ui", self)



    