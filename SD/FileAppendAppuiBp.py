#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Ajout d'une ligne dans un fichier lors appui sur un BP

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

filepath="" # variable globale chemin fichier

#--- setup --- 
def setup():
  
	global filepath # variable globale 
	
	# configuration du BP 
	pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche "+str(BP)+" est en entree avec rappel au plus actif !")
	
	# configuration fichier a utiliser 
	path=homePath()+ dataPath(TEXT)  # chemin du répertoire à utiliser 
	filename="test.txt" # nom du fichier
	filepath=path+filename # chemin du fichier
	
	print ("Fichier utilise : " + filepath )
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	if digitalRead(BP)==APPUI : # si appui BP
		
		# pas a pas :
		"""
		dataFile=open(filepath,'a') # ouvre le fichier en ecriture pour ajout
		dataFile.write("Appui BP : " + nowdatetime() +"\n")
		dataFile.close()
		"""
		
		# ajout dans fichier en 1 ligne 
		appendDataLine(filepath, "Appui BP : " + nowdatetime())
		
		# message console 
		Serial.println ("Ajout ligne : "+ "Appui BP : " + nowdatetime() +" dans fichier " + filepath) 
		
		delay (250) # anti-rebond
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




