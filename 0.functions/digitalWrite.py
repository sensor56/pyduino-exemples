#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# voir : https://github.com/sensor56/pyDuino

# test digitalWrite

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=2  # declare la broche a utiliser

#--- setup --- 
def setup():
	pinMode(LED,OUTPUT) # met la broche en sortie
	Serial.println("La broche 2 est en sortie !")
	
	digitalWrite(LED,HIGH) # allume la LED
	Serial.println("La broche 2 est allumée !")


# -- fin setup -- 

# -- loop -- 
def loop():
	return 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin




