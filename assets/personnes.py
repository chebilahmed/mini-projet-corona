from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3

from assets.error_widget import open_error

# Connect to the database
conn = sqlite3.connect('./assets/projet.db')


# Create a cursor object
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS  "personne" (
	"Cin"	INTEGER NOT NULL,
	"Nom"	TEXT NOT NULL,
	"Prenom"	TEXT,
	"Age"	INTEGER,
	"Adresse"	TEXT,
	"Nationalité"	TEXT NOT NULL,
	"Tel"	TEXT NOT NULL,
	"Date"	Date,
	"decede"	TEXT NOT NULL,
	PRIMARY KEY("Cin")
)''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()



# clear the inputs 
def clear_Ajouter_person_func(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.spinBox.setValue(0)
        self.lineEdit_7.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_4.setText("")
        self.error_1.setText("")




# Add new person
def Ajouter_person_func(self):
    
    #get the data from inputs
    Cin=self.lineEdit.text()
    Nom=self.lineEdit_2.text()
    Prenom=self.lineEdit_3.text()
    Age=int(self.spinBox.text())
    Adresse=self.lineEdit_7.text()
    Nationalite=self.lineEdit_6.text()
    Tel=self.lineEdit_4.text()
    Date=self.dateEdit.text()
    if (self.radioButton.isChecked() ):
        decede= "oui"
    else: 
        decede="non"

    #check the data
    if not((len(Cin)==8 and Cin.isdigit())):
        open_error(self,"taper correctement la cin")

        return 0
    
    elif not((3<=len(Nom)<=20) and (3<=len(Prenom)<=20)):
        open_error(self,"taper correctement le Nom et le prenom")

        return 0
    
    elif (Age == 0):
        open_error(self,"aper correctement l'age ")

        return 0
    
    elif not((3<=len(Nationalite)) ):
        open_error(self,"taper correctement la nationalité ")
        return 0
    
    elif not((3<=len(Tel)) ):
        open_error(self,"taper correctement la telephone")
        return 0
    
    else:
        try :
            #connect to db
            conn=sqlite3.connect('./assets/projet.db')

            c=conn.cursor()
            
            

            #insert the data into db 
            c.execute(f"INSERT INTO personne VALUES('{Cin}','{Nom}','{Prenom}','{Age}','{Adresse}','{Nationalite}','{Tel}','{Date}','{decede}')")

            #save close db
            conn.commit()
            conn.close()

            #reload the table of persons
            
            
            show_personnes(self,self.tableWidget)
            self.statusBar().showMessage('Nouveau personne est ajoutée')
            self.error_1.setText("done!")
        except  :
            open_error(self,"Cin deja exist")

         




# show all the persons in the Table
def show_personnes(self,Widget):
    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()
    c.execute("select * from personne")
    data=c.fetchall()
    if data :
        Widget.setRowCount(0)
        Widget.insertRow(0)
        for row , form in enumerate(data) :
            for column , item in enumerate(form):
                Widget.setItem(row, column,QTableWidgetItem(str(item)))
                
                column+=1
            row_position=Widget.rowCount()
            
            Widget.insertRow(row_position)

    else :
        Widget.setRowCount(0)
        Widget.insertRow(0)




# Delete person from data base
def Supprimer_person_func(self):
        
    #connect to db
    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()

    # get data from inputs
    combo_valeur=self.comboBox.currentText()
    data=self.lineEdit_5.text()


   
    
    #request for delete the person
    c.execute(f"DELETE FROM personne WHERE {combo_valeur} = ?", (data,))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

    #CHECK IF the person was deleted successfully
    if (c.rowcount >0):

        #inisialize the input to empty string
        self.lineEdit_5.setText("")

        if combo_valeur=="Cin":
            self.statusBar().showMessage('la personne a été supprimer avec succès')
        else :
            self.statusBar().showMessage('les personnes ont été supprimer avec succès')
        
        #reload the table of persons
        
        

    else : 
        self.statusBar().showMessage('ce personne est introuvable')



def modifier_personne_func(self):
    

    # get data from inputs
    cin=self.lineEdit_10.text()
    tel=self.lineEdit_8.text()
    adress=self.lineEdit_9.text()

    if cin!="":

        #connect to db
        conn=sqlite3.connect('./assets/projet.db')

        c=conn.cursor()

        if tel=="" and adress =="":
            self.statusBar().showMessage("s'il vous plait entrer les données")
        elif adress=="":
           
            c.execute("UPDATE personne SET Tel = ? WHERE Cin = ?", (tel, cin))
            self.statusBar().showMessage("Tel est modifié avec succès")
        elif tel=="" :
            c.execute("UPDATE personne SET Adresse = ? WHERE Cin = ?", (adress, cin))
            self.statusBar().showMessage('Adresse  est modifiée avec succès')
        else:
            c.execute("UPDATE personne SET Adresse = ? ,Tel = ? WHERE Cin = ?", (adress,tel, cin))
            self.statusBar().showMessage('Adresse et Tel  sont modifiés avec succès')

         # commit the changes
        conn.commit()

        # close the connection
        conn.close()

        self.lineEdit_10.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        #reload the table of persons
        

def show_rech_personnes(self,Widget,data):
    
    if data :
        Widget.setRowCount(0)
        Widget.insertRow(0)
        for row , form in enumerate(data) :
            for column , item in enumerate(form):
                Widget.setItem(row, column,QTableWidgetItem(str(item)))
                
                column+=1
            row_position=Widget.rowCount()
            
            Widget.insertRow(row_position)

    else :
        Widget.setRowCount(0)
        Widget.insertRow(0)


def Recherche_func(self):
    rech_combo=self.comboBox_2.currentText()
    decedes=self.comboBox_3.currentText()
    data=self.lineEdit_11.text()

    

    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()
    req=""
    if(rech_combo== "Tout" and decedes == "Tout"):
        show_personnes(self,self.tableWidget_2)
    elif (decedes == "Tout"):
        req=f"select * from personne where {rech_combo}='{data}'"
        print(req)
        c.execute(req)
        
    elif (decedes=="Décédés"):
        if (rech_combo != "Tout"):
            req=f"select * from personne where {rech_combo}='{data}' and decede='oui'"
        else:
            req=f"select * from personne where  decede='oui'"
        print(req)
        c.execute(req)

    else:
        if (rech_combo != "Tout"):
            req=f"select * from personne where {rech_combo}='{data}' and decede='non'"
        else:
            req=f"select * from personne where  decede='non'"

        print(req)
        c.execute(req)
    data=c.fetchall()
    
    # commit the changes
    conn.commit()

    # close the connection
    conn.close()
   
    if req :
        show_rech_personnes(self,self.tableWidget_2,data)
    self.lineEdit_11.setText("")
