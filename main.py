import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import ConfigurationUI

if __name__ == '__main__':
    from PyQt5 import QtCore
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) #importantce
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ConfigurationUI.Ui_Configuration_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

