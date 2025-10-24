from PySide6.QtWidgets import QApplication, QWidget,QPushButton,QMainWindow,QLabel,QMenu,QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize,Qt
from random import choice
# Only needed for access to command line arguments
import sys



# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('QT-APPS')
#         # functions of QMainWindow
#         size = QSize(600,350)
#         self.setFixedSize(size)
        
#         button = QPushButton('Push')
#         self.setCentralWidget(button)

# # You need one (and only one) QApplication instance per application.
# # Pass in sys.argv to allow command line arguments for your app.
# # If you know you won't use command line arguments QApplication([]) works too.
# app = QApplication(sys.argv)
# # Create a Qt widget, which will be our window.
# window = MainWindow()
# window.show()  # IMPORTANT!!!!! Windows are hidden by default.
# # Start the event loop.
# app.exec()

window_title_choice = [
    "My App",
    "My App",
    "Still My App",
    "Still My App",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong",
]

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
# number = 0
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,600)
        self.number = 0
        self.mainui = QWidget()

        # this is where UI is gonna be visible
        self.setCentralWidget(self.mainui)
        # a layout where i manage my widgets, for NOW its a vertical layout
        self.layouts = QVBoxLayout(self.mainui)
        
        # attaching layout to the widget
        # self.mainui.setLayout(layout)
        # UIs are label, increment, decrement, reset, checkbox, input
        self.inpt = QLineEdit()
        # get the data and every time its changed. update the variable(state)
        self.inpt.textChanged.connect(self.update_number)
        self.layouts.addWidget(self.inpt)

        self.data = QLabel('')
        self.layouts.addWidget(self.data)

        self.increment = QPushButton('+')
        self.increment.setFixedSize(160,60)
        
        self.increment.clicked.connect(self.increase_num)
        self.layouts.addWidget(self.increment)

        self.decrement = QPushButton('-')
        self.decrement.setFixedSize(160,60)
        self.decrement.clicked.connect(self.decrease_num)
        self.layouts.addWidget(self.decrement)


        self.reset = QPushButton('RESET')
        self.reset.setFixedSize(160,60)
        self.reset.clicked.connect(self.reset_num)
        self.layouts.addWidget(self.reset)

        self.toggle_to_increase = QPushButton('Double The Value')
        self.toggle_to_increase.setFixedSize(160,60)
        self.toggle_to_increase.setCheckable(True)
        self.layouts.addWidget(self.toggle_to_increase)
        
    def update_number(self):
        # global number
        try:
            self.number = int(self.inpt.text())
            # number = inpt_data
        except:
            self.number = 0
    def reset_num(self):
        self.number = 0
        self.data.setNum(self.number)
    
    def decrease_num(self):
      # get data using QLineEdit()
        # inpt_data = self.inpt.text()
        # sub = self.number*2
        if self.toggle_to_increase.isChecked():
           
            self.number = self.number - 2
            self.data.setNum(self.number)
            print(self.number)
        else:
            self.number -= 1
            self.data.setNum(self.number)
        if self.number < 0:
            self.data.setStyleSheet('color:blue; background-color: yellow;')
        elif self.number > 0:
            self.data.setStyleSheet("color:red; background-color: cyan")
        # self.data.setNum(self.number)
        
        # self.data.setText(get_data)
        # self.layouts.addWidget(inpt)

    def increase_num(self):

        # the moment i click on increment, it is again taking the value of QlineEdit so obv it will read again and again and not once
        # global number
        if self.toggle_to_increase.isChecked():
            self.number = self.number + 2
            self.data.setNum(self.number)
        else:
            self.number += 1
            self.data.setNum(self.number)

        if self.number < 0:
            self.data.setStyleSheet('color:violet; background-color: yellow;')
        elif self.number > 0:
            self.data.setStyleSheet("color:green; background-color: cyan")



class CounterModel:
    def __init__(self):
        self.number = 0
    
    def increment(self):
        self.number += 1

    def decrement(self):
        self.number -= 1
    
    def reset(self):
        self.number = 0 

    
class CounterView:
    def __init__(self):


        # create container
        
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        # self.layout = QVBoxLayout()


        self.inpt = QLineEdit()
        self.layout.addWidget(self.inpt)

        self.label = QLabel()
        self.layout.addWidget(self.label)
        
        self.increment = QPushButton('+')
        self.layout.addWidget(self.increment)

        self.decrement = QPushButton('-')
        self.layout.addWidget(self.decrement)

        self.reset_btn = QPushButton('RESET')
        self.layout.addWidget(self.reset_btn)


class CounterPresenter:
    def __init__(self,model, view):
        self.model = model
        self.view = view
        self.connect_signals()
        # make it a callback and not a immediate function update_number()
        # self.view.inpt.textChanged.connect(self.update_number())
        self.view.inpt.textChanged.connect(self.update_number)
        

    def update_number(self):
        self.model.number = int(self.view.inpt.text())
        if self.model.number < 0:
            self.view.label.setStyleSheet('color:blue; background-color: yellow;')
        elif self.model.number > 0:
            self.view.label.setStyleSheet("color:red; background-color: cyan")


    def connect_signals(self):
        # connect model(data) with view(UI)
        self.view.increment.clicked.connect(self.increase)
        self.view.decrement.clicked.connect(self.decrease)


    def increase(self):
        # update the data from model and update the view
        self.model.increment()
        # update the view
        self.view.label.setNum(self.model.number)

    def decrease(self):
        # update the data from model and update the view
        self.model.decrement()
        # update the view
        self.view.label.setNum(self.model.number)
        #attach model(data) to view(UI)


app = QApplication(sys.argv)

model = CounterModel()
view = CounterView()
presenter = CounterPresenter(model,view)

main_window = MainWindow()

# widget is in CounterPresenter class since window attaches widget to the main-window
main_window.setCentralWidget(view.widget)
main_window.show()

app.exec()

    # increment, decrement, reset, 

























# app where main python Application runs
app = QApplication(sys.argv)

# then i create a window 
window = MainWindow()
window.show()

app.exec()






#  ------------------------------- NOTES-----------------------
'''
- right now the widgets are positioned in the left corner of the screen, i have set widgets in central(of QMainWindow())

- Obv since i am getting input only once it is stored in get_data so it wont update any further
i need a way to increment and 

- okay i need to connect input data to the increment or decrement. i need to read once then according to signal ... send it to respective
(increase or decrease)slots

- Done with increment, double increment/decrement.now the only thing work with colors

- update label- green color if number is positive and red color if number is negative

- if i dont set any size naturally it takes entire space of the window

'''