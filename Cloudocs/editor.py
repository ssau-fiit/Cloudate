from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
import requests as rq

import sys


class Editor(QtWidgets.QMainWindow):
    def __init__(self, name: str, ID: int):
        super().__init__()

        self.name = name
        self.ID = ID
        print(self.ID)

        self.menuBar = None
        self.filename = None

        self.setWindowTitle(self.name)
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = QtWidgets.QTextEdit(self)
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
            doc_text = self.text_edit.toPlainText()

            resp = rq.post("http://api.cloudocs.parasource.tech:8080" + "/api/v1/documents/" + str(self.ID),
                           json = {"text": doc_text})

            if resp.status_code == 200:
                QtWidgets.QMessageBox.information(self, "All is good", "Changes saved!")
            else:
                QtWidgets.QMessageBox.critical("Sending text error", f"Status code: {resp.status_code}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Editor()
    window.show()

    sys.exit(app.exec())
