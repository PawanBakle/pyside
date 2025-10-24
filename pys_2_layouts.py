import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout,QHBoxLayout

from layout_color_widget import Color


        # grid_layout = QGridLayout()

        # grid_layout.addWidget(Color('green'),0,1)
        # grid_layout.addWidget(Color('white'),0,2)
        # grid_layout.addWidget(Color('cyan'),0,3)
        # grid_layout.addWidget(Color('red'),0,6)
        
        # grid_layout.addWidget(Color('pink'),1,3)
        # grid_layout.addWidget(Color('purple'),2,3)
        # grid_layout.addWidget(Color('blue'),2,1)

        # widgets = QWidget()
        # widgets.setLayout(grid_layout)
        # self.setCentralWidget(widgets)






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        parent = QVBoxLayout()
        child1 = QHBoxLayout()
        child2 = QHBoxLayout()
        child3 = QHBoxLayout()
        layout3 = QVBoxLayout()
        
        child1.addWidget(Color("green"))
        child1.addWidget(Color("green"))
        child1.addWidget(Color("green"))

        child2.addWidget(Color("red"))
        child2.addWidget(Color("red"))
        child2.addWidget(Color("red"))

        child3.addWidget(Color("yellow"))
        child3.addWidget(Color("yellow"))
        child3.addWidget(Color("yellow"))

        parent.addLayout(child1)
        parent.addLayout(child2)
        parent.addLayout(child3)

        widget_red = Color("red")
        widget_blue = Color("blue")
        widget_yellow = Color("yellow")
        
        # layout.addWidget(widget)
        # layout.addWidget(widget_blue)
        # layout.addWidget(widget_yellow)
        # layout.addWidget(widget_red)
        # # layout.addLayout(layout1)

        # layout1.addWidget(Color("green"))
        # layout1.addWidget(Color("white"))
        # layout3.addWidget(Color('pink'))
        # layout3.addWidget(Color('purple'))
        
        # # adding to the horizontal layout 
        # # layout.addLayout( layout3 )
        # layout1.addLayout( layout )

        # # adding to the vertical layout which is part of Horizontal layout
        # layout1.addLayout( layout3 )
        # make and empty widget and set it has central widget so other Color widgets can be attached to the layout
        widget = QWidget()
        # here layout1 is the parent. depends if i make layout the parent. ONLY layout can add other layouts(VBox or Hbox)
        # because there can only be 1 parent (which is attached to widget) once attached to widget IT BECOMES THE PARENT
        # widget.setLayout(layout1)
        widget.setLayout(parent)
          # attaching the widget to the frame (QMainWindow)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()