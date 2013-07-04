#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test toggle

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=2 # broche utilisee pour le LED

#--- setup --- 
def setup():
	pinMode(LED,OUTPUT) # met la LED en sortie
	
# -- fin setup -- 

# -- loop -- 
def loop():
	toggle(LED) # inverse la LED
	delay(1000)
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




