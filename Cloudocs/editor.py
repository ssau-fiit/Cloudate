from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
from PyQt6 import QtCore

import sys

class Editor(QtWidgets.QDialog):
    def __init__(self):
        super(Editor, self).__init__()

        self.filename = None

        self.setWindowTitle("Редактор")
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.createMenuBar()


    def createMenuBar(self):
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        fileMenu = QMenu("&Файл", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction("Открыть", self.action_clicked)
        fileMenu.addAction("Сохранить", self.action_clicked)


    def action_clicked(self):
        action = self.sender()

        if action.text() == "Открыть":
            self.filename = QFileDialog.getOpenFileName(self)[0]


            if len(self.filename) > 0:
                with open(self.filename, "r") as f:
                    data = f.read()
                    self.text_edit.setText(data)
            else:
                print("Файл не найден")

        elif action.text() == "Сохранить":
            self.filename = QFileDialog.getSaveFileName(self)[0]

            if len(self.filename) > 0:
                with open(self.filename, "w") as f:
                    text = self.text_edit.toPlainText()
                    f.write(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Editor()
    window.show()
    
    sys.exit(app.exec())