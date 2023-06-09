import asyncio
import sys


from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QVBoxLayout
import requests as rq

from Constants import ServerAPI

from editor import Editor, InputDialog


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
        # self.documentsList.setSelectionMode(QtGui.QListView.Extended)
        self.documentsList.setGeometry(QtCore.QRect(20, 20, 480, 480))
        self.documentsList.itemDoubleClicked.connect(self.filenameClicked)
        self.addDocumentsToList()
        self.documentsList.setObjectName("documentsList")

        self.newDocumentButton = QtWidgets.QPushButton(self)
        self.newDocumentButton.clicked.connect(self.addNewDocument)
        self.newDocumentButton.setObjectName("newDocumentButton")
        self.newDocumentButton.setText("Новый документ")

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.clicked.connect(self.deleteDocument)
        self.deleteButton.setText("Удалить")

        self.refreshButton = QtWidgets.QPushButton(self)
        self.refreshButton.clicked.connect(self.updateDocuments)
        self.refreshButton.setText("Обновить список")

        self.createMenuBar()

        vbox = QVBoxLayout()
        vbox.addWidget(self.documentsList)
        vbox.addWidget(self.newDocumentButton)
        vbox.addWidget(self.deleteButton)
        vbox.addWidget(self.refreshButton)

        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

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
            documents = rq.get(ServerAPI.url + ServerAPI.getDocuments)

            if documents.status_code == 200 and documents is not None:
                # Adding documents to the list
                for doc in documents.json():
                    item = FileItem(doc["ID"], doc["name"], doc["author"])
                    self.documentsList.addItem(item)

        except Exception as e:
            print(e)

    def addNewDocument(self):
        inputDialog = InputDialog()
        inputDialog.setMinimumWidth(400)
        inputDialog.setMinimumHeight(200)
        inputDialog.setWindowTitle("Создать документ")
        inputDialog.continueBtn.setText("Создать")
        inputDialog.nameEdit.setPlaceholderText("Название документа")
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

                # self.setWindowTitle(self.name)

                QtWidgets.QMessageBox.information(self,
                                                  "Creating new document",
                                                  "New document created successfully")
                # self.new_file.emit()

            else:
                QtWidgets.QMessageBox.critical(self,
                                               "Creating document error",
                                               f"Status code: {resp.status_code}")
        self.updateDocuments()

    def updateDocuments(self):
        self.documentsList.clear()
        try:
            # JSON objects of documents
            documents = rq.get(ServerAPI.url + ServerAPI.getDocuments)

            if documents.status_code == 200 and documents is not None:
                # Adding documents to the list
                for doc in documents.json():
                    item = FileItem(doc["ID"], doc["name"], doc["author"])
                    self.documentsList.addItem(item)

        except Exception as e:
            print(e)

    def addNewDocumentMenu(self):
        action = self.sender()

        if action.text() == "Новый документ":
            print("Новый документ")
            # self.editor_win = Editor()
            # self.editor_win.show()

    def filenameClicked(self, item):
        print(f"Filename: {item.name}")
        self.editor_win = Editor(item.name, item.ID, self.user_id)
        self.editor_win.show()

    def deleteDocument(self):
        if not self.documentsList.selectedItems():
            print("error")
            return
        item = self.documentsList.selectedItems()[0]
        self.documentsList.takeItem(self.documentsList.row(item))

        try:
            # JSON objects of documents
            doc_delete = rq.delete(ServerAPI.url + ServerAPI.getDocument + item.ID)
            if doc_delete.status_code != 200:
                print("Error")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    docs_win = DocumentsWindow()
    docs_win.show()

    sys.exit(app.exec())
