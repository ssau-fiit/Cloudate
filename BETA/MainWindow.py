import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from registration_form import RegistrationWindow
from docs_list import DocumentsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')

    def showRegistration(self):
        self.reg_win = RegistrationWindow()
        self.reg_win.pushButton.clicked.connect(self.showFiles)
        self.reg_win.pushButton.clicked.connect(self.reg_win.close)
        self.reg_win.show()

    def showFiles(self):
        self.docs_win = DocumentsWindow()
        self.docs_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = MainWindow()
    w.showRegistration()
    
    sys.exit(app.exec_())