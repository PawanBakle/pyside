# Goal: Learn to connect many signals with one slot function (like multiple buttons doing different actions).import sys
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,QVBoxLayout,
                               QHBoxLayout,QGridLayout,QPushButton,QFormLayout,
                               QLineEdit,QLabel,QTextEdit

)
from PySide6.QtCore import Qt
from layout_color_widget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.textinpt = QLabel('hel',self)
        horizontal_layout = QHBoxLayout()
        
        # a_button = ["Tea","Coffee","Drinks"]
        t_btn = QPushButton('Tea')
        t_btn.clicked.connect(self.show_order)
        c_btn = QPushButton('Coffee')
        d_btn = QPushButton('Drinks')
        # horizontal_layout.addWidget(self.textinpt)
        horizontal_layout.addWidget(t_btn)
        horizontal_layout.addWidget(c_btn)
        horizontal_layout.addWidget(d_btn)

        widget = QWidget()
        widget.setLayout(horizontal_layout)
        widget.setFixedSize(600,600)
        self.setCentralWidget(widget)
        
    
    def show_order(self):
        self.textinpt.setText('Tea')
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()