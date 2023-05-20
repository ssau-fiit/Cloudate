from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QDialog
import requests as rq
import sys
from ServerConstants import Server
from websockets.sync.client import connect
from string import printable

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


class TextEdit(QtWidgets.QTextEdit):
    def __init__(self,wsock):
        super().__init__()
        self.wsock = wsock


    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Backspace:
            print("Backspace pressed")

        elif event.key() == Qt.Key_Enter:
            print("Enter pressed")
        elif event.key() == Qt.Key_Space:
            print("Space pressed")
        elif event.key() == Qt.Key_Tab:
            print("Tab pressed")
        elif event.key() == Qt.Key_Escape:
            print("Escape pressed")
        else:
            text_key = event.text()
            if text_key:
                print(text_key)
            else:
                print(event.key())


class Editor(QtWidgets.QMainWindow):
    new_file = Signal()

    def __init__(self, name: str, ID: int):
        super().__init__()

        self.name = name
        self.ID = ID
        self.wsock = connect("ws://api.cloudocs.parasource.tech:8080/api/v1/documents/" + str(self.ID))



        # with connect("ws://api.cloudocs.parasource.tech:8080/api/v1/documents/" + str(self.ID)) as websocket:
        #     websocket.send("Hello world!")
            # message = websocket.recv()
            # print(f"Received: {message}")




        self.menuBar = None
        self.filename = None

        self.setWindowTitle(self.name)
        self.setGeometry(300, 250, 350, 200)

        # self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit = TextEdit(self.wsock)
        # self.text_edit.textChanged.connect(self.on_text_changed)

        self.setCentralWidget(self.text_edit)

        # # Создаем горячую клавишу для нажатия клавиши backspace
        # shortcut = QtGui.QShortcut(QtGui.QKeySequence("Backspace"), self.text_edit)
        # shortcut.activated.connect(self.on_backspace_pressed)

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
                QtWidgets.QMessageBox.critical(self,
                                               "Sending text error", f"Status code: {resp.status_code}")

    def on_text_changed(self):
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        line_number = cursor.blockNumber()
        print(f"Курсор находится на позиции {position} в строке номер {line_number}")
