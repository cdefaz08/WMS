from Layout.login import LoginWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys

def apply_theme_from_file(app, qss_file):
    with open(qss_file, "r") as f:
        app.setStyleSheet(f.read())

def main():
    app = QtWidgets.QApplication(sys.argv)
    apply_theme_from_file(app, "themes/dark_orange_theme.qss")
    app.setWindowIcon(QIcon("icons/Logo/de-faz Logo_Transparent.png"))
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
