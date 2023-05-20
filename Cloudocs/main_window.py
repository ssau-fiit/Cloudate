import sys
from PySide6.QtWidgets import QApplication
from registration_window import RegistrationWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        * {
            font-family: "SF Pro Display", Arial, sans-serif;
        }
        
        QWidget {
            background-color: whitesmoke;
            color: white;
        }
        QPushButton {
            border-radius: 10px;
            font-size: 18px;
            background-color: #FFD95A;
            color: #3e3e3e;
            font-weight: 600;
            padding: 15px 20px;
        }
        QPushButton:hover {
            background-color: #ffd65d;
        }
        QLineEdit {
            padding: 20px 25px;
            border-radius: 10px;
            font-size: 2rem;
            font-weight: 400;
            line-height: 1.6;
            color: #495057;
            background-color: #fff;
            background-clip: padding-box;
            border: 1px solid #ced4da;
        }
        
        QListWidget {
            color: black;
            font-size: 18px;
        }
        
        QListWidgetItem {
            padding: 10px 15px;
        }
    """)

    w = RegistrationWindow()
    w.setMinimumHeight(400)
    w.setMinimumWidth(400)
    w.show()

    sys.exit(app.exec())