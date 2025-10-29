import sys


from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,QVBoxLayout,
  QHBoxLayout,QGridLayout,QPushButton,QFormLayout,
  QLineEdit,QLabel,QTextEdit,QListView,
)
from PySide6.QtCore import QObject,Signal,QTimer,QAbstractListModel,Qt,QModelIndex
# from layout_color_widget import Color

class MenuModal(QAbstractListModel):
    def __init__(self,parent = None):
        super().__init__(parent)
        self._data = []
    # # data = []
    #     self.data = []
    def rowCount(self, parent = QModelIndex()):
        return len(self._data)
    # def add_task_item(self,item):
    #     # self.beginInsertW
        
    #     self.beginInsertRows(QModelIndex(),0,0)
    #     self.data.append(item)
    #     self.endInsertRows()

    def data(self, index, role):
        if not index.isValid():
            return None

        # We only care about the display role (the text content)
        if role == Qt.ItemDataRole.DisplayRole:
            # Look up the text based on the row number
            return self._data[index.row()]
        
        # Optional: Add a simple color role for demonstration
        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 == 0:
                return Qt.GlobalColor.lightGray
            return Qt.GlobalColor.white

        return None # Return None for all other roles

    # Slot called by the MainWindow to add an item
    def add_task_item(self, item):
        # FIX 3: Resetting self.data = [] here would delete the whole list.
        # We need the current length to calculate the insertion row.
        
        # 1. Calculate the new row index (which is the current length)
        row_to_insert = len(self._data)
        
        # 2. Notification: Tell the View we are inserting one row 
        #    starting and ending at the calculated index.
        self.beginInsertRows(QModelIndex(), row_to_insert, row_to_insert)
        
        # 3. Data Change: Perform the actual Python list manipulation.
        self._data.append(item)
        
        # 4. Notification: Tell the View the data is ready.
        self.endInsertRows()
        return True # Return success

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = MenuModal()
        # model
        # self.data = []
        self.list_view = QListView()

        # connect List with MenuModel
        self.list_view.setModel(self.model)



        # View
        self.horizontal_layout = QHBoxLayout()
        # self.form_inpt = QFormLayout()
        self.label = QLabel('New Task')
        self.task_inpt = QLineEdit()
        self.add_btn = QPushButton('Add Task')

        # self.form_inpt.addRow('New Task',self.task_inpt)
        self.horizontal_layout.addWidget(self.label)
        self.horizontal_layout.addWidget(self.task_inpt)
        self.horizontal_layout.addWidget(self.add_btn)

        # Main Layout (Vertical Stack)
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.horizontal_layout)
        main_layout.addWidget(self.list_view) 
        # connecting signals to the QListView
        self.add_btn.clicked.connect(self.get_text)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget) 

    def get_text(self):
            
        new_task = self.task_inpt.text().strip()
        if new_task:
            # Call the Model method to perform the data change and notification
            self.model.add_task_item(new_task)
            self.task_inpt.clear()
            self.task_inpt.setFocus()

       


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()



# class ModelTsk():
#     # hold data, i.e states/variables
#     pass

# class ViewUI():
#     # Main Window, TaskList Widgets
#     pass


# class PresenterTsk():
#     # connect UI to Model via signals-slots, model updates
#     pass