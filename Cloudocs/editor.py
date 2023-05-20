from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog, QDialog
import requests as rq
import sys
from ServerConstants import Server
from websockets.sync.client import connect


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input dialog")
        self.nameEdit = QtWidgets.QLineEdit()

        self.continueBtn = QtWidgets.QPushButton("Continue")
        self.continueBtn.clicked.connect(self.closeDialog)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.nameEdit)
        self.layout.addWidget(self.continueBtn)

        self.setLayout(self.layout)

    def closeDialog(self):
        if self.nameEdit.text() == "":
            QtWidgets.QMessageBox.information(self,
                                              "Empty name",
                                              "Input some name")
            return

        self.close()


class Editor(QtWidgets.QMainWindow):
    new_file = Signal()

    def __init__(self, name: str, ID: int):
        super().__init__()

        with connect("ws://api.cloudocs.parasource.tech:8080/api/v1/documents/981723") as websocket:
            websocket.send("Hello world!")
            message = websocket.recv()
            print(f"Received: {message}")

        self.name = name
        self.ID = ID

        self.menuBar = None
        self.filename = None

        self.setWindowTitle(self.name)
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = QtWidgets.QTextEdit(self)
        # self.text_edit.textChanged(self.send_doc)
        self.setCentralWidget(self.text_edit)


        # Get text from server
        resp = rq.get("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents/" + str(ID))

        if resp.status_code == 200:
            doc_text = resp.json()["text"]
            self.text_edit.setText(doc_text)

        self.createMenuBar()

    def createMenuBar(self):
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        fileMenu = QMenu("&Файл", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction("Сохранить", self.action_clicked)

    def action_clicked(self):
        action = self.sender()

        if action.text() == "Сохранить":

            # If creating new document
            if self.ID == -1:
                inputDialog = InputDialog()
                if inputDialog.exec() == 0:
                    # Creating new document
                    doc_name = inputDialog.nameEdit.text()
                    resp = rq.post(Server.url + Server.createDocument,
                                   json = {
                                       "name": doc_name,
                                       "author": "Will Smith"
                                   })

                    if resp.status_code == 200:
                        json_doc = resp.json()
                        self.ID = json_doc["ID"]
                        self.name = json_doc["name"]

                        self.setWindowTitle(self.name)

                        QtWidgets.QMessageBox.information(self,
                                                          "Creating new document",
                                                          "New document created successfully")
                        self.new_file.emit()

                    else:
                        QtWidgets.QMessageBox.critical(self,
                                                       "Creating document error",
                                                       f"Status code: {resp.status_code}")

                else:
                    QtWidgets.QMessageBox.critical(self,
                                                   "Dialog error",
                                                   f"Some error with dialog")

            # Saving text of document
            doc_text = self.text_edit.toPlainText()
            resp = rq.post("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents/" + str(self.ID),
                           json = {"text": doc_text})

            if resp.status_code == 200:
                QtWidgets.QMessageBox.information(self, "All is good", "Changes saved!")
            else:
                QtWidgets.QMessageBox.critical(self, "Sending text error", f"Status code: {resp.status_code}")

    def send_doc(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Editor()
    window.show()

    sys.exit(app.exec())
