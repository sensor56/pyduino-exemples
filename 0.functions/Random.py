#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test Random

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	randomSeed(0) # initialisation générateur de valeurs aléatoires
	
	print random(10) # un nombre aléatoire entre 0 et 10
	print random(4, 12) # un nombre aléatoire entre 4 et 12 
	
	for i in range(0,10): # 10  passages
		print random(10) # un nombre aléatoire entre 0 et 10
		# modifier randomSeed et voir que le série est modifiée

# -- fin setup -- 

# -- loop -- 
def loop():
	return

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




