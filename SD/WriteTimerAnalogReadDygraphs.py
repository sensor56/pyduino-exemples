#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# enregistrer une mesure analogique dans un fichier a intervalle regulier _ format dygraphs

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

compt=0  # compteur 

filepath=""

#--- setup --- 
def setup():
	
	global filepath
	
	myDataPath=("data/text/")
	
	path=homePath()+myDataPath  # chemin du répertoire à utiliser
	filename="data"+today()+".txt" # nom du fichier
	filepath=path+filename # chemin du fichier
	
	print filepath
	
	if exists(filepath):
		print "Le fichier existe"
	else :
		print "Le fichier n'existe pas : creation du fichier"
		myFile=open(filepath,'w') # création du fichier
		myFile.close()
	
	loop() # premier appel loop
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepath, compt
	
	#mesure analogique 
	mesure=analogRead(A2) # mesure sur voie A2
	mesuremV=analogReadmV(A2) # mesure en Mv sur voie A2
	
	myFile=open(filepath,'a') # ouverture pour ajout de texte
	
	#-- ajout de chaines au fichier 
	
	#out=(str(compt)+":"+nowdatetime()+": "+ str(mesure) + " soit " + str(mesuremV) + " millivolts.")
	out=today('/')+" "+ hour()+":"+minute()+":"+second() +" " + str(mesure) 
	
	myFile.write(out+"\n") # ecriture d'une ligne
	
	myFile.close() # fermeture du fichier en ecriture
	
	print (out) # debug 
	
	compt=compt+1 # incrémente compteur
	
	timer(1000, loop) # auto appel de loop toutes les secondes
	
	# NB : ouvrir le fichier dans l'editeur pour verifier son contenu 
	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




