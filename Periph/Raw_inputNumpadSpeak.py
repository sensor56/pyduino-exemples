#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test raw_input

#from pyduino import * # importe les fonctions Arduino pour Python
from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return  # si vide 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	# try.. except.. permet d'éviter le blocage si erreur de saisie
	try: 
		speak("Veuillez saisir une valeur : ")
		reponse=raw_input("Veuillez saisir une valeur : ")
	except: # erreur
		print ("Veuillez recommencer !")
		return  # sort de la fonction loop
	
	print ("Vous avez saisi : " + reponse ) 
	speak("Vous avez saisi : " + reponse)
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
