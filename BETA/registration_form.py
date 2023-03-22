import http
import sys

import requests
from PyQt6 import QtCore, QtGui, QtWidgets


class RegistrationWindow(QtWidgets.QMainWindow):

    session_id = None

    def authenticate(self):
        print("kek")
        username = self.lineEdit.text()
        password = ''
        url = 'http://127.0.0.1:8080/api/v1/auth'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            # TODO сделать показ ошибок аутентификации
            raise Exception('Authentication failed!')
        self.user_id = response.json()['user_id']  # assuming the API returns a token
        print(self.user_id)

    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()

        self.setMinimumWidth(280)
        self.setMinimumHeight(150)
        self.setWindowTitle("Registration")


        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Продолжить")
        self.pushButton.clicked.connect(self.authenticate)

        self.usernameEdit = QtWidgets.QLineEdit(self)
        self.usernameEdit.setGeometry(QtCore.QRect(70, 40, 151, 20))
        self.usernameEdit.setObjectName("lineEdit")
        self.usernameEdit.setPlaceholderText("Логин")

        self.passwordEdit = QtWidgets.QLineEdit(self)
        self.passwordEdit.setGeometry(QtCore.QRect(70, 40, 151, 20))
        self.passwordEdit.setObjectName("lineEdit")
        self.passwordEdit.setPlaceholderText("Пароль")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.usernameEdit)
        vbox.addWidget(self.passwordEdit)
        vbox.addWidget(self.pushButton)

        self.setLayout(vbox)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    reg = RegistrationWindow()
    reg.show()

    sys.exit(app.exec_())