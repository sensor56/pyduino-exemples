#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test analogRead

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	
	#voie A0
	mesuremV=analogReadmV(A0) # mesure la voie A2 - résultat en mV
	Serial.println("Voie A0 = " + str(mesuremV) + " mV.")

	#voie A2
	mesuremV=analogReadmV(A2) # mesure la voie A2 - résultat en mV
	Serial.println("Voie A2 = " + str(mesuremV) + " mV.")
	
	delay(1000)# entre 2 mesures 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin




