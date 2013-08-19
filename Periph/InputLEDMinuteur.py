#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# la saisie d'une valeur fixe la duree d'allumage d'une LED

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=3  # broche utilisée pour la LED

#--- setup --- 
def setup():
	
	pinMode(LED,OUTPUT) # met la broche en sortie 
	
	Serial.println("------------------")
# -- fin setup -- 

# -- loop -- 
def loop():
	
	# try.. except.. permet d'éviter le blocage si erreur de saisie
	try: 
		reponse=input("Veuillez saisir une valeur en secondes (0-100) :")  # attention : encadrer chaine avec "" 
		# sinon elle sera consideree comme le nom d'une variable - voir raw_input pour saisie de chaine
	except: # erreur
		print ("Veuillez recommencer !")
		return  # sort de la fonction loop
	
	print ("Vous avez saisi : " + str(reponse) ) 
	
	duree=constrain(reponse,0,100)
	print "Duree = " + str(duree) + " secondes"
	
	# allumage de la LED
	Serial.println("Allume la LED")
	digitalWrite(LED,HIGH) #allume la LED
	
	Serial.println("Attente de " + str(duree) + " secondes...")
	delay(duree*1000)  # pause (en ms !!)
	
	Serial.println("Eteint la LED")
	digitalWrite(LED,LOW) # eteint la LED
	
	Serial.println("------------------")
	

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




