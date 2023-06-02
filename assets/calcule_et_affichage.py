from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3




from assets.personnes import show_rech_personnes 


def calc_risque_maladie(cin,maladie,risque):
	
	for ligne in maladie:
		
		if str(ligne[1])== str(cin) :
			
			
			if ligne[2].lower() in ["diabete" , "diabéte"] :
				
				risque += 15
			if ligne[2].lower() == "hypertension" :
				risque += 20
			if ligne[2].lower() == "asthme" :
				risque += 20
			
	return risque


def calc_risque_age(age,risque):
	
	if age > 70 :
		risque += 20
	if 50 <= age <=70 :
		
		risque += 15
	
	return risque

def calc_rique_total(c,Widget):
	maladie=[]
	c.execute("select * from maladie ")
		
	#get data from db
	data=c.fetchall()

	for row , form in enumerate(data) :
		m=[]
		for column , item in enumerate(form):
			m.append(item)
			
		maladie.append(m)

	

	c.execute("select * from personne ")
	
	e={
		"cin":"",
		"nom":"",
		"prenom":"",
		"age":0
	}
	#get data from db
	data=c.fetchall()

	if data :
		Widget.setRowCount(0)
		Widget.insertRow(0)
		for row , form in enumerate(data) :
			risque=0
			
			for column , item in enumerate(form):
				if column == 0 :
					e["cin"]=item
					Widget.setItem(row, column,QTableWidgetItem(str(item)))
				elif column == 1 :
					e["nom"]=item
					Widget.setItem(row, column,QTableWidgetItem(str(item)))
				elif column == 2 :
					e["prenom"]=item
					Widget.setItem(row, column,QTableWidgetItem(str(item)))
				elif column == 3 :
					e["age"]=int(item)
					Widget.setItem(row, column,QTableWidgetItem(str(item)))
				else :
					break
				
				column+=1
			
			risque=calc_risque_age(e["age"],risque)
			
			risque=calc_risque_maladie(e["cin"],maladie,risque)
			
			Widget.setItem(row, column,QTableWidgetItem(str(risque)+"%"))
			row_position=Widget.rowCount()
			Widget.insertRow(row_position)
			
			
	else :
		Widget.setRowCount(0)
		Widget.insertRow(0)
######################################

def calcule_et_affichage(self):
	# get data from inputs
	combo_valeur=self.comboBox_4.currentText()
	data=self.lineEdit_12.text()

	#connect to db
	conn=sqlite3.connect('./assets/projet.db')

	c=conn.cursor()
	if combo_valeur == "Nationalité" :
		#show persons have the same nationality
		req=f"select * from personne where Nationalité='{data}'"

	elif combo_valeur == "quarantaine":
		#show persons in the last 14 day
		req=f"select * from personne  where ((julianday(date('now')) - julianday(strftime(DATE(Date))))+1) <= 14  "
		
	elif combo_valeur == "décédés":
		req=f"select * from personne where  decede='oui'"
		#count the number of all the persons
		c.execute("select count(*) from personne ")
		nbreTotal=(c.fetchall())[0][0]

		#count the number of persons decedes
		c.execute("select count(*) from personne where  decede='oui'")
		nbreDeces=(c.fetchall())[0][0]
		
		#calculate the percentage 
		pourcentage=(nbreDeces*100)/nbreTotal
	   
	
	else :
		#show all the persons
		req=f"select * from personne "
	
	if combo_valeur != "à risque":
		self.tableWidget_4.setVisible(True)
		self.tableWidget_5.setVisible(False)
		#send request
		c.execute(req)
		
		#get data from db
		data=c.fetchall()
		
		
		
		
			
		#show the data in the table
		show_rech_personnes(self,self.tableWidget_4,data)
	else :
		self.tableWidget_4.setVisible(False)
		self.tableWidget_5.setVisible(True)
		calc_rique_total(c,self.tableWidget_5)
	# commit the changes
	conn.commit()

	# close the connection
	conn.close()
	if (combo_valeur == "décédés"):
		self.label_18.setText(f"Nombre Totale :{nbreTotal}")
		self.label_19.setText(f"Nombre de décès :{nbreDeces}")
		self.label_20.setText("la pourcentage de décès :{0:.2f}%".format(pourcentage))
	else :
		#clear the labels
		self.label_18.setText("")
		self.label_19.setText("")
		self.label_20.setText("")
