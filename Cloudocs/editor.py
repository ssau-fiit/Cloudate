from PySide6.QtCore import QThread

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


class WebSocketThread(QThread):
    srvMsgChannel = Signal(str)

    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.listen())

    async def on_message(self, message):
        # This function is called everytime a new message is received from the server
        self.srvMsgChannel.emit(message)
        print("Message:", message)

    async def listen(self):
        # Create a WebSocket connection
        async with websockets.connect(self.text_edit.wsock_url,
                                      extra_headers={"X-Cloudocs-ID": str(self.text_edit.user_id)}) as ws:
            self.text_edit.wsock = ws
            # Call on_open() after the connection is opened
            async for message in ws:
                # Call on_message() for each message received from the server
                await self.on_message(message)


class TextEdit(QtWidgets.QTextEdit):
    userPress = Signal(QtGui.QKeyEvent)

    def __init__(self, editor, file_id: int, user_id: int):
        super().__init__()
        self.file_id = file_id
        self.user_id = user_id
        self.prev_cursor_position = 0
        self.editor = editor
        self.last_ver = 1

        # Creating websocket (will be initialized in webSocketThread)
        self.wsock_url = f"ws://{ServerAPI.host}:{ServerAPI.port}/api/v1/documents/" + str(self.file_id)
        self.wsock = None

        # Creating separate thread for socket listener
        self.webSocketThread = WebSocketThread(self)
        self.webSocketThread.srvMsgChannel.connect(self.msgsHandler)
        self.webSocketThread.start()

    def getServerEvent(self, op_type: str, length: int, index: int, text: str):
        # op_type from ServerConstants.OpType

        self.last_ver += 1
        operation = {
            "userID": self.user_id,
            "type": op_type,
            "len": length,
            "index": index,
            "version": self.last_ver,
            "text": text
        }

        print("Operation:", operation)

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

            serv_event = self.getServerEvent(OpType.DELETE,
                                             cursor.selectionEnd() - cursor.selectionStart(),
                                             current_position - 1,
                                             "\b")
            # print("Backspace pressed")

        elif event.key() == Qt.Key_Enter:
            serv_event = self.getServerEvent(OpType.INSERT, 1, current_position, "\n")
            # print("Enter pressed")

        elif event.key() == Qt.Key_Space:
            serv_event = self.getServerEvent(OpType.INSERT, 1, current_position, " ")
            # print("Space pressed")

        elif event.key() == Qt.Key_Tab:
            serv_event = self.getServerEvent(OpType.INSERT, 1, current_position, "\t")
            # print("Tab pressed")

        else:
            text_key = event.text()
            if text_key:
                serv_event = self.getServerEvent(OpType.INSERT, 1, current_position, text_key)
                # print(f"Text: {text_key}")
            else:
                # print(event.key())
                pass

        # print(f"Index sent: {current_position}")

        asyncio.run(self.wsock.send(json.dumps(serv_event)))
        # print("Event: ", serv_event)
        super().keyPressEvent(event)

    @QtCore.Slot(str)
    def msgsHandler(self, text: str):
        data = json.loads(text)
        decoded_string = base64.b64decode(data["event"]).decode('utf-8')
        json_data = json.loads(decoded_string)

        print("Json data:", json_data)

        if "lastVersion" in json_data:
            last_ver = json_data["lastVersion"]
            self.last_ver = last_ver
            print("received last version is", last_ver)

        # if type is present in data, then it is not first message
        if 'type' in data:
            if "text" in json_data:
                # Обработка приходящих операций
                self.last_ver = json_data["version"]

                index = 0
                if "index" in json_data:
                    index = json_data["index"]
                current_text = self.toPlainText()
                new_text = ""
                # Insert
                if "type" not in json_data:
                    new_text = current_text[:index] + json_data["text"] + current_text[index:]
                # Delete
                else:
                    new_text = current_text[:index] + current_text[index+json_data["len"]:]
                self.setText(new_text)

        else:
            self.setFontFamily("SF Pro Display")
            json_data = json.loads(decoded_string)
            self.setText(json_data["text"])


class Editor(QtWidgets.QMainWindow):
    new_file = Signal()

    def __init__(self, name: str, file_id: int, user_id: int):
        super().__init__()

        self.name = name
        self.file_id = file_id
        self.user_id = user_id

        self.menuBar = None
        self.filename = None

        self.setWindowTitle(self.name)
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = TextEdit(self, self.file_id, self.user_id)
        self.text_edit.setTextColor("black")

        self.setCentralWidget(self.text_edit)

    def closeEvent(self, event):
        self.text_edit.webSocketThread.terminate()
