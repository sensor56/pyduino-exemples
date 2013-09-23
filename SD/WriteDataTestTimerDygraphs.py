#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Aout 2013- Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Creer un fichier de donnees horodatees sur 24H avec enregistrement auto

from pyduino import * # importe les fonctions Arduino pour Python
import datetime # pour operations facilitees sur date/heure

# entete declarative
noLoop=True

filepath=""
filename=""
today0=""

compt=0
refTime=None

#--- setup --- 
def setup():
	
	global filepath, filename, today0, refTime
	
	myDataPath=("data/text/")
	
	today0=today() # memorise jour courant 
	
	path=homePath()+myDataPath  # chemin du répertoire à utiliser
	filename="data"+today0+".txt" # nom du fichier
	filepath=path+filename # chemin du fichier
	
	print filepath
	
	# creation fichier au besoin 
	if exists(filepath):
		print "Le fichier existe"
	else :
		print "Le fichier n'existe pas : creation du fichier"
		myFile=open(filepath,'w') # création du fichier
		myFile.close()
		

	loop() # premier appel loop
	
	# NB : on peut aussi ouvrir le fichier dans l'editeur pour verifier son contenu 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepath, filename, today0, refTime, compt
	
	myFile=open(filepath,'a') # ouverture pour ajout de texte
	#myFile=open(filepath,'w') # ouverture pour ecriture avec effacement contenu
	
	#-- ajout de chaines au fichier 
	dataValue=str(random(0,1023)) # genere une valeur aleatoire entiere
	
	# format de donnees utilise : JJ/MM/YYYY hh:mm:ss , val \n
	dataLine=today('/') + " " + hour()+":"+minute() + ":" + second()+","+dataValue+"\n"
	print dataLine # debug
	
	myFile.write(dataLine) # ecrit la ligne dans le fichier
	
	myFile.close() # fermeture du fichier en ecriture
	
	# auto rappel de loop
	compt=compt+1 # incrémente compteur
	
	timer(1000, loop) # auto appel de loop toutes les secondes
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




