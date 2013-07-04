#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test pinMode pullup

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	pinMode(2,PULLUP) # met la broche en entrée avec "rappel au plus" actif
	Serial.println("La broche 2 est en entrée avec rappel au plus actif!")

# -- fin setup -- 

# -- loop -- 
def loop():
	return

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin




