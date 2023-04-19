import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout
import requests as rq
from editor import Editor


class FileItem(QtWidgets.QListWidgetItem):
    def __init__(self, ID: int, name: str, author: str):
        super().__init__(name)

        self.ID = ID
        self.name = name
        self.author = author


class DocumentsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.menuBar = None
        self.editor_win = None

        # Will be initialized after call registration_window
        self.username = None
        self.user_id = None
        self.password = None

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.documentsList = QtWidgets.QListWidget(self)
        self.documentsList.setGeometry(QtCore.QRect(20, 20, 480, 480))
        self.documentsList.itemDoubleClicked.connect(self.filenameClicked)
        self.addDocumentsToList()
        self.documentsList.setObjectName("documentsList")

        self.newDocumentButton = QtWidgets.QPushButton(self)
        self.newDocumentButton.clicked.connect(self.addNewDocument)
        self.newDocumentButton.setObjectName("newDocumentButton")
        self.newDocumentButton.setText("Новый документ")

        self.createMenuBar()

        vbox = QVBoxLayout()
        vbox.addWidget(self.documentsList)
        vbox.addWidget(self.newDocumentButton)

        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        # self.setLayout(vbox)

    def createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar()
        self.setMenuBar(self.menuBar)

        fileMenu = QtWidgets.QMenu("&Файл", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction("Новый документ", self.addNewDocumentMenu)

    def show(self):
        super().show()
        self.setWindowTitle(f"Documents list ({self.username}, id = {self.user_id})")

    def addDocumentsToList(self):
        try:
            # JSON objects of documents
            documents = rq.get("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents")

            if documents.status_code == 200 and documents is not None:
                # Adding documents to the list
                for doc in documents.json():
                    self.documentsList.addItem(FileItem(doc["ID"], doc["name"], doc["author"]))
        except Exception as e:
            print(e)
            print("Ошибка")

    def addNewDocument(self):
        self.editor_win = Editor("Default", -1)
        self.editor_win.show()

    def addNewDocumentMenu(self):
        action = self.sender()

        if action.text() == "Новый документ":
            print("Новый документ")
            # self.editor_win = Editor()
            # self.editor_win.show()


    def filenameClicked(self, item):
        print(f"Filename: {item.name}")
        self.editor_win = Editor(item.name, item.ID)
        self.editor_win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    docs_win = DocumentsWindow()
    docs_win.show()

    sys.exit(app.exec())
