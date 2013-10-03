#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyduino-exemples

# enregistrer une mesure analogique dans un fichier a intervalle regulier

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True # bloque loop auto

compt=0  # compteur 
nombreMesures=10 # nombre de mesure
intervalMesure=1 # intervalle entre 2 mesure en secondes
filepath="" # nom fichier 

#--- setup --- 
def setup():
	
	global filepath
	
	# definition chemin - nom fichier
	filepath=homePath()+dataPath(TEXT)+"data_"+today("_",-1)+".txt" # nom fichier format data_aaaa_mm_jj.txt
	print filepath # debug
	
	loop() # premier appel loop
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepath, compt
	
	# mesure analogique 
	mesure=analogRead(A2) # mesure sur voie A2
	
	# definition chaine data
	#out=today('/', -1)+" "+ hour()+":"+minute()+":"+second() +", " + str(mesure) # format today inversé... 
	out=nowdatetime(-1) + ","+ str(mesure) # équivalent
	print (out) # debug 
	
	#-- ajout de chaines au fichier 
	myFile=open(filepath,'a') # ouverture pour ajout de texte
	myFile.write(out+"\n") # ecriture d'une ligne
	myFile.close() # fermeture du fichier en ecriture
	
	# finalisation
	compt=compt+1 # incrémente compteur
	if compt>=nombreMesures:exit()  # stop quand nombre de mesures atteint
	
	timer(intervalMesure*1000, loop) # auto appel de loop toutes les n secondes
	
# -- fin loop --

# NB : ouvrir le fichier dans l'editeur pour verifier son contenu 

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin



