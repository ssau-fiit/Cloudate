import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from Redactor import Editor


class DocumentsWindow(QtWidgets.QDialog):
    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setWindowTitle("Documents list")

        self.documentsList = QtWidgets.QListWidget(self)
        self.documentsList.setGeometry(QtCore.QRect(20, 20, 480, 480))
        self.documentsList.setObjectName("documentsList")
        
        self.editorButton = QtWidgets.QPushButton(self)
        self.editorButton.clicked.connect(self.showRedactor)
        self.editorButton.setObjectName("editorButton")
        self.editorButton.setText("Редактор")

        self.newDocumentButton = QtWidgets.QPushButton(self)
        self.newDocumentButton.clicked.connect(self.addNewDocument)
        self.newDocumentButton.setObjectName("newDocumentButton")
        self.newDocumentButton.setText("Новый документ")        

        vbox = QVBoxLayout()
        vbox.addWidget(self.documentsList)
        vbox.addWidget(self.editorButton)
        vbox.addWidget(self.newDocumentButton)

        self.setLayout(vbox)

    def showRedactor(self):
        self.editor_win = Editor()
        self.editor_win.show()

    def addNewDocument(self):
        self.documentsList.addItem("Empty document")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    docs_win = DocumentsWindow()
    docs_win.show()

    sys.exit(app.exec_())