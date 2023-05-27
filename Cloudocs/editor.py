from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QDialog
import requests as rq
from Constants import ServerAPI, OpType
import websockets
import json
import base64
import asyncio


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
    def __init__(self, wsock, ID: int):
        super().__init__()
        self.wsock = wsock
        self.ID = ID
        self.prev_cursor_position = 0

    def getServerEvent(self, op_type: str, length: int, version: int, index: int, text: str):
        # op_type from ServerConstants.OpType

        operation = {
            "userID": self.ID,
            "type": op_type,
            "len": length,
            "index": index,
            "version": version,
            "text": text
        }
        json_op = json.dumps(operation)
        encoded_json_op = base64.b64encode(bytes(json_op, 'utf-8'))
        serv_event = {
            "type": "OPERATION",
            "event": encoded_json_op.decode("utf-8")
        }

        return serv_event

    def keyPressEvent(self, event):
        # Get cursor index
        cursor = self.textCursor()
        current_position = cursor.selectionStart()
        serv_event = None

        # print(f"Selection start {cursor.selectionStart()}")
        # print(f"Selection end {cursor.selectionEnd()}")

        if event.key() == Qt.Key_Backspace:
            if cursor.hasSelection():
                # Selection to the left
                if cursor.position() - cursor.selectionEnd() < 0:
                    # print("Selection to the left")
                    current_position = cursor.selectionEnd()
                # Selection to the right
                else:
                    # print("Selection to the right")
                    pass

            serv_event = self.getServerEvent(OpType.DELETE, 1, 1, current_position, "\b")
            # print("Backspace pressed")

        elif event.key() == Qt.Key_Enter:
            serv_event = self.getServerEvent(OpType.INSERT, 1, 1, current_position, "\n")
            # print("Enter pressed")

        elif event.key() == Qt.Key_Space:
            serv_event = self.getServerEvent(OpType.INSERT, 1, 1, current_position, " ")
            # print("Space pressed")

        elif event.key() == Qt.Key_Tab:
            serv_event = self.getServerEvent(OpType.INSERT, 1, 1, current_position, "\t")
            # print("Tab pressed")

        else:
            text_key = event.text()
            if text_key:
                serv_event = self.getServerEvent(OpType.INSERT, 1, 1, current_position, text_key)
                # print(f"Text: {text_key}")
            else:
                # print(event.key())
                pass

        # print(f"Index sent: {current_position}")

        super().keyPressEvent(event)
        print("Event: ", serv_event)

        # if self.wsock is not None:
        #     self.wsock.send(json.dumps(serv_event))


class Editor(QtWidgets.QMainWindow):
    new_file = Signal()

    def __init__(self, name: str, ID: int):
        super().__init__()

        self.name = name
        self.ID = ID
        self.wsock = None

        self.wsock_url = "ws://api.cloudocs.parasource.tech:8080/api/v1/documents/" + str(self.ID)
        # self.wsock = websockets.connect(self.wsock_url,
        #                                 extra_headers={"X-Cloudocs-ID": "3"})
        self.wsock = None
        asyncio.get_event_loop().run_until_complete(self.listen())


        self.menuBar = None
        self.filename = None

        self.setWindowTitle(self.name)
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = TextEdit(self.wsock, self.ID)
        # self.text_edit.textChanged.connect(self.on_text_changed)

        self.setCentralWidget(self.text_edit)

        # Get text from server
        # resp = rq.get("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents/" + str(ID))
        #
        # if resp.status_code == 200:
        #     doc_text = resp.json()["text"]
        #     self.text_edit.setText(doc_text)

        self.createMenuBar()

    async def on_message(self, message):
        # This function is called everytime a new message is received from the server
        data = json.loads(message)
        print(f"Received message: {data}")
        decoded_string = base64.b64decode(data["event"]).decode('utf-8')
        print(decoded_string)


    async def on_error(self, error):
        # This function is called when an error occurs
        print(f"Error: {error}")


    async def on_close(self):
        # This function is called when the WebSocket connection is closed
        print("Connection closed")

    async def on_open(self):
        # This function is called when the WebSocket connection is opened
        print("Connection opened")
        # Send a message to the server
        message = {"type": "hello"}
        await self.wsock.send(json.dumps(message))

    async def listen(self):
        # Create a WebSocket connection
        async with websockets.connect(self.wsock_url, extra_headers={"X-Cloudocs-ID": "3"}) as ws:
            self.wsock = ws
            # Call on_open() after the connection is opened
            await self.on_open()
            async for message in ws:
                # Call on_message() for each message received from the server
                await self.on_message(message)

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
                    resp = rq.post(ServerAPI.url + ServerAPI.createDocument,
                                   json={
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
                           json={"text": doc_text})

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
