from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import pandas as pd
import sqlite3



def Export(self,table_name):
    try :
        option=QFileDialog.Options()
        file=QFileDialog.getSaveFileName(self.tabWidget_2,"Save","untitled","All Files (*)",options=option)
        print(file[0])
        connection = sqlite3.connect("projet.db")
        print(table_name)
    
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, connection)
        if ".xlsx" in file[0]:
            df.to_excel({file[0]})
        else :
            df.to_excel(f"{file[0]}.xlsx")
    except :
        pass
