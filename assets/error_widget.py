from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

def open_error(self,error_text):
        ui1,_ = loadUiType(r'error.ui')
        class MainApp1(QMainWindow , ui1):
            def __init__(self,error_text):
                QMainWindow.__init__(self)
                self.setupUi(self)
                self.label_2.setText(error_text)
       
        self.window1=MainApp1(error_text)
        
        self.window1.show()
        