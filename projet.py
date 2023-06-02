from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


from assets.personnes import *
from assets.maladie import *
from assets.calcule_et_affichage import *
from assets.enregistrement import *

from PyQt5.uic import loadUiType



 
ui,_ = loadUiType(r'corona-project.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.Handle_ui_Changes()
        
        show_personnes(self,self.tableWidget)
        show_personnes(self,self.tableWidget_2)
        show_personnes(self,self.tableWidget_6)
        show_personnes(self,self.tableWidget_8)

     
        show_maladie(self,self.tableWidget_3)
        show_maladie(self,self.tableWidget_7)
        show_maladie(self,self.tableWidget_9)


    def Handle_ui_Changes(self):
        self.tableWidget_5.setVisible(False)
        self.tabWidget.tabBar().setVisible(False)
       
        self.tabWidget_2.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(1)


        self.tabWidget.currentChanged.connect(self.tab_changed_personne)
        self.tabWidget_3.currentChanged.connect(self.tab_changed_maladie)
        self.progressBar.setValue(0)
        self.combo_changed()
        self.setWindowTitle("Clean Virus")
        self.setWindowIcon(QIcon("img\logo.png"))




####################################################################################


    def Handle_Buttons(self):
        
        
        #################### Tabs #########################
        #################### home bnt Tabs #########################
        
        self.personnes_btn_2.clicked.connect(self.Open_Personnes)
        self.maladie_btn_2.clicked.connect(self.Open_Maladies)
        self.calc_btn_2.clicked.connect(self.Open_clacule_et_affichage)
        self.enrg_btn_2.clicked.connect(self.Open_enrigestrement_et_recuperation)
        #################### page 2 Tabs #########################
        self.Home_btn.clicked.connect(self.Open_home)
        self.personnes_btn.clicked.connect(self.Open_Personnes)
        self.maladie_btn.clicked.connect(self.Open_Maladies)
        self.calc_btn.clicked.connect(self.Open_clacule_et_affichage)
        self.enrg_btn.clicked.connect(self.Open_enrigestrement_et_recuperation)

        ################## Personne  ############################
        #-------------------- Ajouter personne --------------
        self.pushButton_6.clicked.connect(lambda: Ajouter_person_func(self))
        self.pushButton_7.clicked.connect(lambda: clear_Ajouter_person_func(self))

        #-------------------- Supprimer person -------------------- 
        self.pushButton_8.clicked.connect(lambda: Supprimer_person_func(self))
        self.pushButton_9.clicked.connect(lambda: modifier_personne_func(self))

        #--------------------- recherche personnes --------------------
        self.pushButton_10.clicked.connect(lambda: Recherche_func(self))

        
################## Maladie  ############################
        #-------------------- Ajouter maladie --------------
        self.pb_1.clicked.connect(lambda: ajouter_maladie(self))
        self.pb_3.clicked.connect(lambda: clear_ajouter_maladie(self))

        #-------------------- Supprimer maladie -------------------- 
        self.pb_2.clicked.connect(lambda: Supprimer_maladie(self))
        self.pb_4.clicked.connect(lambda: modifier_maladie(self))
        self.pb_5.clicked.connect(lambda: modifier_maladie_1(self))

        #---------------------- recherche maladie ---------------
        self.pb_6.clicked.connect(lambda:maladie_rech1(self))
        self.pb_7.clicked.connect(lambda:maladie_rech2(self))
        self.pb_8.clicked.connect(lambda:maladie_rech3(self))
        self.pb_9.clicked.connect(lambda:maladie_rech4(self))

        #reload table 
        self.reload1.clicked.connect(lambda:show_personnes(self,self.tableWidget_6))
        self.reload2.clicked.connect(lambda:show_maladie(self,self.tableWidget_7))
        self.reload3.clicked.connect(lambda:show_personnes(self,self.tableWidget_8))
        self.reload3.clicked.connect(lambda:show_maladie(self,self.tableWidget_9))



################## calcule_et_affichage ##############################
        self.pushButton_11.clicked.connect(lambda:calcule_et_affichage(self))

################## enregistrement ###########################
        self.save_p.clicked.connect(lambda: Export(self,"personne"))
        self.save_M.clicked.connect(lambda: Export(self,"maladie"))





    ######### open Tabs ##################
    def Open_home(self):
        self.tabWidget.setCurrentIndex(1)
    def Open_Personnes(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        
    def Open_Maladies(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)

    def Open_clacule_et_affichage(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(2)
    def Open_enrigestrement_et_recuperation(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(3)
    


####################################################################################

    #if the user open the "ajouter_personne" the table will be updated 
    def tab_changed_personne(self,index):
        
        if index == 0:
            show_personnes(self,self.tableWidget)
    def tab_changed_maladie(self,index):
        
        if index == 0:
            show_maladie(self,self.tableWidget_3)
            
    #this code created for hide the input field of "affichage et recherche" 
    # and show it only when i need it
    def combo_changed(self):

############ rech et aff personne ###################
        self.lineEdit_11.setVisible(False)
        self.comboBox_2.currentIndexChanged.connect(self.rech_et_aff_personne_combo_changed)

        ############# calc et aff ###################
        self.lineEdit_12.setVisible(False)
        self.comboBox_4.currentIndexChanged.connect(self.calc_et_aff_combo_changed)

    def rech_et_aff_personne_combo_changed(self,index):
        if index == 0 :
            self.lineEdit_11.setVisible(False)
            self.pushButton_10.move(660, 84)
        else :
            self.pushButton_10.move(850, 84)
            
            self.lineEdit_11.setVisible(True)
            

    def calc_et_aff_combo_changed(self,index):
        if index == 1 :
            self.pushButton_11.move(880, 119)
            self.lineEdit_12.setVisible(True)
        else :
            self.lineEdit_12.setVisible(False)
            self.pushButton_11.move(700, 119)

    def open_error(self):
        ui1,_ = loadUiType(r'error.ui')
        error_text="eeee"
        class MainApp1(QMainWindow , ui1):
            def __init__(self,error_text):
                QMainWindow.__init__(self)
                self.setupUi(self)
                self.label_2.setText(error_text)
       
        self.window1=MainApp1(error_text)
        
        self.window1.show()

        
    

def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
