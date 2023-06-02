from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from assets.personnes import *



# Connect to the database
conn = sqlite3.connect('./assets/projet.db')


# Create a cursor object
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS  "maladie" (
	"CODE"	INTEGER NOT NULL UNIQUE,
	"CIN"	INTEGER NOT NULL,
	"Nom_maladie"	TEXT NOT NULL,
	"Nb_annees"	INTEGER NOT NULL,
	PRIMARY KEY("CIN","Nom_maladie")
)''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()


# clear the inputs 
def clear_ajouter_maladie(self):
        self.le_2.setText("")
        self.le_3.setText("")
        self.sb_4.setValue(0)
        self.error_2.setText("")
        
def verifier (CODE):
    #connect to db
    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()
    # sélectionner une table et récupérer une colonne
    c.execute(f"SELECT (CODE) FROM maladie")
    colonne = c.fetchall()
    
    # afficher les données de la colonne
    
    i=len(colonne)
    if i==0  :
        return 1
    else:
        if CODE != colonne[i-1][0] + 1:
            return 0
    return 1
    

# Add new maladie
def ajouter_maladie(self):
    CODE=int(self.sb_1.text())
    code=int(self.sb_1.text())
    CIN=self.le_2.text()
    Nom_maladie=self.le_3.text()
    Nb_annees=int(self.sb_4.text())

    #controle_de_saisie
    if not((len(CIN)==8 and CIN.isdigit())):
        open_error(self,"taper correctement la cin")
        
        return 0
    
    elif ((verifier(CODE))==0):
        
        open_error(self,"taper correctement le code")
        return 0
    
    elif not((3<=len(Nom_maladie)) ):
        
        open_error(self,"taper correctement la maladie")
        return 0
    
    elif (Nb_annees==0):
        
        open_error(self,"taper correctemant le nombres d\'annees")
        return 0
    
    else:
        try :
            #connect to db
            conn=sqlite3.connect('./assets/projet.db')

            c=conn.cursor()
            self.error_2.setText("done!")

            #insert the data into db 
            c.execute(f"INSERT INTO maladie VALUES('{CODE}','{CIN}','{Nom_maladie}','{Nb_annees}')")

            #save close db
            conn.commit()
            conn.close()

            #reload the table of maladie
            show_maladie(self,self.tableWidget_3)
            print("Done")
            
            self.statusBar().showMessage('Nouveau maladie est ajoutée')
        except  :
            open_error(self,"taper correctement la cin")
            open_error(self,"CIN, Nom_maladie,CODE deja exist")
    return code
           

# show all the maladie in the Table
def show_maladie(self,Widget):
    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()
    c.execute("select CODE,CIN,Nom_maladie,Nb_annees from maladie")
   
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


# Delete maladie from data base
def Supprimer_maladie(self):
        
            
    #connect to db
    conn=sqlite3.connect('./assets/projet.db')

    c=conn.cursor()

    # get data from inputs
    combo_valeur=self.cb_1.currentText()
    data=self.le_4.text()
    print (combo_valeur)

    if combo_valeur == "CIN" :
        req="CIN"
    else :
        req=combo_valeur
    
    if req== "CIN":
        if not((len(data)==8 and data.isdigit())):
            open_error(self,"taper correctement la cin")
            return 0
            
    elif req== "Nom_maladie":
        if not((3<=len(data) and data.isalpha())):
            open_error(self,"taper correctement la maladie")
            return 0
            
    
    #request for delete the maladie
    c.execute(f"DELETE FROM maladie WHERE {req} = ?", (data,))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

    #CHECK IF the maladie was deleted successfully
    if (c.rowcount >0):

        #inisialize the input to empty string
        self.le_4.setText("")

        if req=="CIN":
            open_error(self,'la maladie a été supprimer avec succès')
        else :
            open_error(self,'la maladie a été supprimer avec succès')
        
        #reload the table of maladie
        show_maladie(self,self.tableWidget_3)
        

    else : 
        open_error(self,'ce personne est introuvable')

def modifier_maladie(self):

        # get data from inputs
    CIN=self.le_5.text()
    Nom_maladie=self.le_6.text()
    Nb_annees=self.le_7.text()
    
    if not((len(CIN)==8 and CIN.isdigit())):
        open_error(self,"taper correctement la cin")
        return 0
    
    
    if CIN!="":

        #connect to db
        conn=sqlite3.connect('./assets/projet.db')

        c=conn.cursor()
        if Nom_maladie=="" and Nb_annees=="":
            open_error(self,'s\'il vous plait entrer les données')
        elif Nb_annees=="":
            if not((Nom_maladie=="" or len(Nom_maladie)>3)and Nom_maladie.isalpha()):
                open_error(self,"taper correctemant le nom de maladie")
                return 0
            else:
                c.execute("UPDATE maladie SET Nom_maladie= ? WHERE CIN = ?", (Nom_maladie, CIN))
                open_error(self,'le Nom de maladie est modifié avec succès')
        elif Nom_maladie=="" :
            if not(Nb_annees.isdigit() and int(Nb_annees) > 0):
                open_error(self,"taper correctemant le nombres d\'annees")
                return 0
            else:
                c.execute("UPDATE maladie SET Nb_annees = ? WHERE CIN = ?", (Nb_annees, CIN))
                open_error(self,'le  Nombres d\'annees est modifié avec succès')
        else:
            if not((Nom_maladie=="" or len(Nom_maladie)>3)and Nom_maladie.isalpha()):
                open_error(self,"taper correctemant le nom de maladie")
                return 0
            if not(Nb_annees.isdigit() and int(Nb_annees) > 0):
                open_error(self,"taper correctemant le nombres d\'annees")
                return 0
            else:
                c.execute("UPDATE maladie SET NB_annees = ?, Nom_maladie = ? WHERE CIN = ?", (Nb_annees,Nom_maladie, CIN))
                open_error(self,'le Nombres d\'annees le Nom de maladie sont modifiés avec succès')

         # commit the changes
        conn.commit()

        # close the connection
        conn.close()

        #reload the table of persons
        show_personnes(self,self.tableWidget)
        #reload the table of maladie
        show_maladie(self,self.tableWidget_3)

def modifier_maladie_1(self):
    # get data from inputs
    CIN=self.le_8.text()
    if not((len(CIN)==8 and CIN.isdigit())):
        open_error(self,"taper correctement la cin")
        return 0
    if (self.radioButton_4.isChecked() ):
        decede="oui"

    if CIN!="":

        #connect to db
        conn=sqlite3.connect('./assets/projet.db')

        c=conn.cursor()
        if decede=="":
            open_error(self,'s\'il vous plait entrer les données')
        else:
            c.execute("UPDATE personne SET decede= ? WHERE Cin = ?", (decede, CIN))
            open_error(self,'l\'état est modifié avec succès')
        
        
        # commit the changes
        conn.commit()

        # close the connection
        conn.close()

        #reload the table of persons
        show_personnes(self,self.tableWidget)

def show_rech_personnes(self, Widget, data):
    if data:
        Widget.setRowCount(0)
        if isinstance(data, tuple):
            data = [data]
        for form in (data):  # Reverse the order of tuples in data
            row_position = Widget.rowCount()
            Widget.insertRow(row_position)  # Insert the row at the bottom
            for column, item in enumerate(form):
                Widget.setItem(row_position, column, QTableWidgetItem(str(item)))

def show_rech_personnes2(self, Widget, data):
    Widget.setRowCount(0)  # Move this outside the loop to clear the table before adding new data
    for sublist in data:  # Loop through the list of lists
        for i in sublist:
            if isinstance(i, tuple):  # Check if the element is a tuple
                row_position = Widget.rowCount()
                Widget.insertRow(row_position)
                for column, item in enumerate(i):
                    Widget.setItem(row_position, column, QTableWidgetItem(str(item)))




def maladie_rech1(self):
    # Connect to SQLite database
    conn = sqlite3.connect('./assets/projet.db')

    c = conn.cursor()
    disease_name = self.le_12.text()
    if not((disease_name=="" or len(disease_name)>3)and disease_name.isalpha()):
        open_error(self,"taper correctemant le nom de maladie")
        return 0
    # Search for disease in maladie table
    req = f"SELECT CIN FROM maladie WHERE Nom_maladie='{disease_name}'"
    c.execute(req)
    disease_id = c.fetchall()
    
    l=[]
    if disease_id:
        for disease in disease_id:
            
            # Fetch persons with the disease from personne table
            req = f"SELECT * FROM personne WHERE CIN='{disease[0]}'"
            c.execute(req)
            data = c.fetchall()
            l.append(data)       
    else:
        open_error(self,"cette maladie  introuvable dans le tableau des maladies")
    if len(l)>0:
        show_rech_personnes2(self, self.tableWidget_6, l)
    else:
        open_error(self,f"Aucune personne trouvée avec cette maladie ")
    # Close the database connection
    conn.close()



def maladie_rech2(self):
    # Connect to SQLite database
    conn = sqlite3.connect('./assets/projet.db')

    c = conn.cursor()
    id=self.le_13.text()
    if not((len(id)==8 and id.isdigit())):
        open_error(self,"taper correctement la cin")
        return 0
    # Search for disease in maladie table
    c.execute("SELECT CODE, CIN, Nom_maladie, Nb_annees FROM maladie WHERE CIN=?", (id,))
    disease = c.fetchall()
    if disease:
        show_rech_personnes(self, self.tableWidget_7, disease)
    else:
        open_error(self,"Ce personne  introuvable dans le tableau des maladies")
    # Close the database connection
    conn.close()

def maladie_rech3(self):
    x=0
    s=0
    # Connect to SQLite database
    conn = sqlite3.connect('./assets/projet.db')

    c = conn.cursor()
    id=self.le_14.text()
    if not((id=="" or len(id)>3)and id.isalpha()):
        open_error(self,"taper correctemant le nom de maladie")
        return 0
    c.execute("SELECT * FROM maladie ")
    all = c.fetchall()
    if all:
        s=len(all)
    
    c.execute("SELECT CODE, CIN, Nom_maladie, Nb_annees FROM maladie WHERE Nom_maladie=?", (id,))
    disease = c.fetchall()
    if disease:
        x=len(disease)
    p=(x*100)/s
    self.progressBar.setValue( int(p))
    # Close the database connection
    conn.close()


def maladie_rech4(self):
    # Connect to SQLite database
    conn = sqlite3.connect('./assets/projet.db')

    c = conn.cursor()
    id=self.le_15.text()
    if not((len(id)==8 and id.isdigit())):
        open_error(self,"taper correctement la cin")
        return 0
    # Search for disease in maladie table
    c.execute("SELECT CODE, CIN, Nom_maladie, Nb_annees FROM maladie WHERE CIN=?", (id,))
    disease = c.fetchall()
    if disease:
        show_rech_personnes(self,self.tableWidget_9,disease)
    else:
        open_error(self,f"Ce personne n'est pas trouvable dans le table de maladie")
    
    # Search for person in person table
    c.execute("SELECT Cin, Nom, Prenom, Age, Adresse, Nationalité, Tel, Date, decede FROM personne WHERE CIN=?", (id,))
    person = c.fetchone()
    if person:
        show_rech_personnes(self,self.tableWidget_8,person)
        open_error(self,"Ce personne est connu")
    else:
        open_error(self,"Ce personne n'est pas trouvable dans le table de personne")
    # Close the database connection
    conn.close()

    