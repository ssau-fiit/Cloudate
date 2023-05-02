import sys
from PySide6.QtWidgets import QApplication
from registration_window import RegistrationWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = RegistrationWindow()
    w.show()

    sys.exit(app.exec())