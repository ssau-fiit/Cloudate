import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Redactor import Editor


class DocumentsWindow(QtWidgets.QDialog):
    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setWindowTitle("Documets list")

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 461, 461))
        self.listWidget.setObjectName("listWidget")
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 81, 23))
        self.pushButton.clicked.connect(self.showRedactor)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("переход к редактору")

    def showRedactor(self):
        self.editor_win = Editor()
        self.editor_win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    docs_win = DocumentsWindow()
    docs_win.show()

    sys.exit(app.exec_())