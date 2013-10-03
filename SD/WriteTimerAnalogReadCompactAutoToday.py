#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# enregistrer une mesure analogique dans un fichier a intervalle regulier avec journalisation automatique - format horodate
# top : lancer ce code suffit pour creer un fichier de data par jour !

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True # pour utilisation auto appel de loop

path="" # rep enregistrement fichiers data
filepath="" # n
today0="" # variable memorisation dernier jour pris en compte

#--- setup --- 
def setup():
	
	global path, filepath, today0
	
	# initialisation rep data
	path=homePath()+dataPath(TEXT)  # chemin du répertoire à utiliser /home/user/data/text par defaut
	print path # debug 
	
	#today0="2013_09_24" # pour test changement de date 
	
	loop() # premier appel loop
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global path, filepath, today0
	
	# MAJ nom fichier si changement de jour ou premier passage
	if today0!=today("_",-1) : # si on change de jour - vrai au premier passage ! 
		today0=today("_",-1)  # memorise jour courant  au format AAAA_MM_JJ
		filename="data_"+today0+".txt" # nom du fichier au format data_AAAA_MM_JJtxt
		filepath=path+filename # chemin du fichier
		
		print filepath  # debug
	
	# dans tous les cas : 
	
	#mesure analogique 
	mesure=analogRead(A2) # mesure sur voie A2
	
	# definition ligne de donnee 
	#out=today("/",-1) +" "+ hour()+":"+minute()+":"+second() +", " + str(mesure) # format today inversé... 
	out=nowdatetime(-1) + ","+ str(mesure) # équivalent
	print (out) # debug 
	
	#-- ajout de chaines au fichier 
	myFile=open(filepath,'a') # ouverture pour ajout de texte
	myFile.write(out+"\n") # ecriture d'une ligne
	myFile.close() # fermeture du fichier en ecriture
	
	# auto rappel de loop 
	timer(60000, loop) # auto appel de loop toutes les minutes = 60000 ms
	
	# NB : ouvrir le fichier dans l'editeur pour verifier son contenu 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin

	"""
	Les formats possibles dygraphs sont :
	
	2009-07-12
	2009/07/12
	2009/07/12 12
	2009/07/12 12:34
	2009/07/12 12:34:56
	voir : http://dygraphs.com/data.html
	"""
	



