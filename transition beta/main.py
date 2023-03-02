import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from signup import Ui_MainWindow
from Redactor import Window
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
from PyQt5 import QtCore

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()


def openOtherWindow():
    global window
    window = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(Window)
    MainWindow.close()
    window.show()
    

    



ui.pushButton.clicked.connect(openOtherWindow)

sys.exit(app.exec_())