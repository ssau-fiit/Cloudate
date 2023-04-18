import sys
from PyQt6 import QtWidgets
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout
import requests as rq
from editor import Editor


class FileItem(QtWidgets.QListWidgetItem):
    def __init__(self, fullpath: str):
        super().__init__(fullpath.split('/')[-1])

        self.fullpath = fullpath


class DocumentsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.editor_win = None

        # Will be initialized after call registration_window
        self.username = None
        self.user_id = None
        self.password = None

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.documentsList = QtWidgets.QListWidget(self)
        self.documentsList.setGeometry(QtCore.QRect(20, 20, 480, 480))
        self.documentsList.itemClicked.connect(self.filenameClicked)
        self.documentsList.setObjectName("documentsList")

        self.addDocumentsToList()

        self.newDocumentButton = QtWidgets.QPushButton(self)
        self.newDocumentButton.clicked.connect(self.addNewDocument)
        self.newDocumentButton.setObjectName("newDocumentButton")
        self.newDocumentButton.setText("Новый документ")

        vbox = QVBoxLayout()
        vbox.addWidget(self.documentsList)
        vbox.addWidget(self.newDocumentButton)

        self.setLayout(vbox)

    def show(self):
        super().show()
        self.setWindowTitle(f"Documents list ({self.username}, id = {self.user_id})")

    def addDocumentsToList(self):
        try:
            # JSON objects of documents
            json_documents = rq.get("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents")

            if json_documents.status_code == 200 and json_documents is not None:
                # Get name of each document
                document_names = list(
                    map(lambda json_obj: f"{json_obj['name']} (ID = {json_obj['ID']})", json_documents.json())
                )
                # Adding documents to the list
                for name in document_names:
                    self.documentsList.addItem(FileItem(name))
        except Exception as e:
            print(e)

    def addNewDocument(self):
        # Get filenames from QFileDialog
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self)[0]
        # Cast it to the FileItem
        list_items = [FileItem(fullpath) for fullpath in filenames]
        # Add to the list
        for item in list_items:
            self.documentsList.addItem(item)

    def filenameClicked(self, item):
        print(f"Filename: {item.fullpath}")
        self.editor_win = Editor()
        self.editor_win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    docs_win = DocumentsWindow()
    docs_win.show()

    sys.exit(app.exec())
