import http
import sys
import requests
from PyQt6 import QtCore, QtGui, QtWidgets
from documents_window import DocumentsWindow

class RegistrationWindow(QtWidgets.QDialog):

    session_id = None

    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()

        self.setMinimumWidth(280)
        self.setMinimumHeight(150)
        self.setWindowTitle("Registration")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Продолжить")
        # self.pushButton.clicked.connect(self.authenticate)
        self.pushButton.clicked.connect(self.goToDocumentsWindow)

        self.usernameEdit = QtWidgets.QLineEdit(self)
        self.usernameEdit.setObjectName("usernameEdit")
        self.usernameEdit.setPlaceholderText("Логин")

        self.passwordEdit = QtWidgets.QLineEdit(self)
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setPlaceholderText("Пароль")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.usernameEdit)
        vbox.addWidget(self.passwordEdit)
        vbox.addWidget(self.pushButton)

        self.setLayout(vbox)


    def goToDocumentsWindow(self, user_id = -1):
        self.doc_win = DocumentsWindow()

        self.doc_win.username = self.usernameEdit.text()
        self.doc_win.user_id = user_id
        self.doc_win.password = self.passwordEdit.text()

        self.doc_win.show()
        self.close()


    def authenticate(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        
        url = 'http://api.cloudocs.parasource.tech:8080/api/v1/auth'
        data = {'username': username, 'password': password}
        response = requests.post(url, json = data)

        if response.status_code != 200:
            # TODO: сделать показ ошибок аутентификации
            dlg = QtWidgets.QMessageBox.critical(self, "Authentication failed!",
                                                 f"Status code: {response.status_code}")
            dlg.exec()
            print("АУ БЛЯТЬ")
            raise Exception('Authentication failed!')

        user_id = response.json()['user_id']

        print(f"User ID = {user_id}")

        self.goToDocumentsWindow(user_id)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    reg = RegistrationWindow()
    reg.show()

    sys.exit(app.exec())