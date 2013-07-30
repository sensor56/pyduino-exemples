#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test raw_input

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
  for i in range(0,8):  # defile broches
		pinMode(i, OUTPUT) # met la broche en sortie
		digitalWrite(i,LOW) # eteint les broches
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	# try.. except.. permet d'éviter le blocage si erreur de saisie
	try: 
		reponse=raw_input("Selectioner broche (+/- suivi numero suivi enter) : ")
	except: # erreur
		print ("Veuillez recommencer !")
		return  # sort de la fonction loop
	
	print ("Vous avez saisi : " + str(reponse) ) 
	
	pin = abs(int(reponse))
	
	if pin<=7 :   # si valeur entre 0 et 7
		if str(reponse)[0]=="-" : 
			digitalWrite(pin,LOW) # eteint la LED si negatif
		else : 
			digitalWrite(pin,HIGH) # allume la LED
			
	elif pin==99: # toutes les broches a la fois
		if str(reponse)[0]=="-" : 
			for i in range(0,8):  # defile broches
				digitalWrite(i,LOW) # eteint les LED si negatif
		else : 
			for i in range(0,8):  # defile broches
				digitalWrite(i,HIGH) # allume les LED

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




