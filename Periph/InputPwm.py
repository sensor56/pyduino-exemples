#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# la saisie d'une valeur fixe l'impulsion pwm

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return  # si vide 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	# try.. except.. permet d'éviter le blocage si erreur de saisie
	try: 
		reponse=input("Veuillez saisir une valeur entre 0 et 100% ")  # attention : encadrer chaine avec "" 
		# sinon elle sera consideree comme le nom d'une variable - voir raw_input pour saisie de chaine
	except: # erreur
		print ("Veuillez recommencer !")
		return  # sort de la fonction loop
	
	print ("Vous avez saisi : " + str(reponse) ) 
	
	pwmValue=constrain(reponse,0,100)
	print "Valeur pwm = " + str(pwmValue) + "%"
	
	analogWritePercent(PWM0,pwmValue) # largeur impulsion en 0-100% sur PWM0 = broche 3 pcduino
	

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




