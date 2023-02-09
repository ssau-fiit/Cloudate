from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fieldName = QtWidgets.QLineEdit(self.centralwidget)
        self.fieldName.setGeometry(QtCore.QRect(90, 80, 113, 20))
        self.fieldName.setAlignment(QtCore.Qt.AlignCenter)
        self.fieldName.setObjectName("fieldName")
        self.labelEnterName = QtWidgets.QLabel(self.centralwidget)
        self.labelEnterName.setGeometry(QtCore.QRect(10, 60, 281, 20))
        self.labelEnterName.setStyleSheet("")
        self.labelEnterName.setScaledContents(False)
        self.labelEnterName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEnterName.setObjectName("labelEnterName")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 120, 75, 23))
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()

    def add_functions(self):
        self.pushButton.clicked.connect()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelEnterName.setText(_translate("MainWindow", "Введите имя"))
        self.pushButton.setText(_translate("MainWindow", "Продолжить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
