#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# LED clignote sans delay avec millis()

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=2  # declare la broche a utiliser

millis0=millis()# variable memorise millis()
delai=1000 # pause

#--- setup --- 
def setup():
  pinMode(LED,OUTPUT) # met la broche en sortie
	Serial.println("La broche " +str(LED)+ " est en sortie !")

# -- fin setup -- 

# -- loop -- 
def loop():
	
	global millis0 # variable globale
	
	if millis()-millis0>delai : # si delai ecoule
		toggle(LED)  # inverse etat de la LED
		millis0=millis() # memorise millis courant
	
	# autres instructions ici 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin


