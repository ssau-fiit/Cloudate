import sys
import requests
from PySide6 import QtWidgets
from documents_window import DocumentsWindow


class RegistrationWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(280)
        self.setMinimumHeight(150)
        self.setWindowTitle("Registration")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Продолжить")
        self.pushButton.clicked.connect(self.authenticate)
        # self.pushButton.clicked.connect(self.goToDocumentsWindow)

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

        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        # self.setLayout(vbox)

    def goToDocumentsWindow(self, user_id=-1):
        self.doc_win = DocumentsWindow()

        self.doc_win.username = self.usernameEdit.text()
        self.doc_win.user_id = user_id
        self.doc_win.password = self.passwordEdit.text()

        self.doc_win.show()
        self.close()

    def authenticate(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()

        url = "http://api.cloudocs.parasource.tech:8080/api/v1/auth"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, json = data)
            if response.status_code != 200:
                QtWidgets.QMessageBox.critical(self, "Authentication failed!",
                                                     f"Status code: {response.status_code}")

            user_id = response.json()['user_id']
            self.goToDocumentsWindow(user_id)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    reg = RegistrationWindow()
    reg.show()

    sys.exit(app.exec())
