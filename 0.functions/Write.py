#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test Write

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
	
	myDataPath=("data/text/")
	
	#path=homePath()+myDataPath  # chemin du répertoire à utiliser
	path=homePath()+dataPath(TEXT) # chemin repertoire a utiliser - equivalent 
	filename="test.txt" # nom du fichier
	filepath=path+filename # chemin du fichier
	
	print filepath
	
	# -- test existence fichier 
	if exists(filepath):
		print "Le fichier existe"
	else : 
		print "Le fichier n'existe pas : creation du fichier"
	
	# ouverture fichier
	myFile=open(filepath,'a') # ouverture/creation pour ajout de texte
	# note : en mode 'a' : le fichier est cree si n'existe pas
	
	#-- ajout de chaines au fichier 
	myFile.write('a'+"\n") # ecriture d'un caractere
	myFile.write("coucou") # ecriture de plusieurs caractere - equivalent print()
	myFile.write("\n") # ecriture saut de ligne 
	myFile.write("Une ligne de texte "+"\n") # une ligne avec saut de ligne final - equivalent println()
	
	strMulti="""
Je suis bavard et
j'aime bien parler
c'est pourquoi
je dis toutes ces choses
et bien d'autres encore.
"""
	myFile.write(strMulti) # ajout d'une bloc de texte multiligne au fichier
	
	myFile.close() # fermeture du fichier en ecriture
	
	#-- lecture du fichier -- 
	myFile=open(filepath,'r') # ouverture en lecture
	print ("Contenu du fichier : ")
	myFile.seek(0)  # se positionne au debut du fichier
	print myFile.read() # lit le contenu du fichier entier
	
	myFile.close() # fermeture du fichier
	
	
	# NB : ouvrir le fichier dans l'editeur pour verifier son contenu 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
