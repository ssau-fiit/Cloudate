from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
from PyQt5 import QtCore

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Охуенный редактор")
        self.setGeometry(300, 250, 350, 200)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text_edit)


        self.createMenuBar()

    def createMenuBar(self):
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        fileMenu = QMenu("&Залупа", self)
        self.menuBar.addMenu(fileMenu)

        fileMenu.addAction("Расчехлить", self.action_clicked)
        fileMenu.addAction("Сохранить", self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()

        if action.text() == "Расчехлить":
            fname = QFileDialog.getOpenFileName(self)[0]

            if len(fname) > 0:
                with open(fname, "r") as f:
                    data = f.read()
                    self.text_edit.setText(data)
            else:
                print("Файл не найден")

        elif action.text() == "Сохранить":
            fname = QFileDialog.getSaveFileName(self)[0]

            if len(fname) > 0:
                with open(fname, "w") as f:
                    text = self.text_edit.toPlainText()
                    f.write(text)

            


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()