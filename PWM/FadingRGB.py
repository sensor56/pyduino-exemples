#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# La luminosite d'une LED RGB varie (PWM) 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
rgb=[PWM0, PWM1, PWM2] # list des broches pwm utilisee - doit être une broche PWM (3,5,6,9,10 ou 11)

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	
	for couleur in rgb :
		
		for impuls in range(0,255):
			analogWrite(couleur, impuls) # applique la largeur 
			Serial.println ("PWM= "+str(impuls))
			delay(5)# entre 2 changements
		
		for impuls in range(0,255):
			analogWrite(couleur, 255-impuls) # applique la largeur 
			Serial.println ("PWM= "+str(255-impuls))
			delay(5)# entre 2 changements
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
