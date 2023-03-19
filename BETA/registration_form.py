import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class RegistrationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()

        self.setMinimumWidth(280)
        self.setMinimumHeight(150)
        self.setWindowTitle("Registration")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Продолжить")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(70, 40, 151, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Введите имя")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    reg = RegistrationWindow()
    reg.show()

    sys.exit(app.exec_())