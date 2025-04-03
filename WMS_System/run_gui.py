from Layout.login import LoginWindow
from PyQt5 import QtWidgets
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
