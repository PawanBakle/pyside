import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,QVBoxLayout,
                               QHBoxLayout,QGridLayout,QPushButton,QFormLayout,
                               QLineEdit

)

from layout_color_widget import Color
def tr(text):
    return QApplication.translate("MyForm", text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        forms = QFormLayout()
        nameLine = QLineEdit()
        emailLine = QLineEdit()

        login_btn = QPushButton('Login')
        number = QLineEdit()
        forms.addRow(tr('Name'),nameLine)
        forms.addRow(tr('Email'),emailLine)
        forms.addRow(tr('Number'),number)
        forms.addRow(login_btn)

        widget = QWidget()
        widget.setLayout(forms)
        self.setCentralWidget(widget)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()