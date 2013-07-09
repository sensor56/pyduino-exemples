#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# LED clignote - sans delay - avec timer

from pyduino import * # importe les fonctions Arduino pour Python

from threading import Timer # importe l'objet Timer du module threading

# entete declarative
LED=2  # declare la broche a utiliser
etatLED=LOW # memorise etat LED
delai=0.25 # pause   a utiliser en secondes

#--- setup --- 
def setup():
	
	pinMode(LED,OUTPUT) # met la broche en sortie
	Serial.println("La broche " +str(LED)+ " est en sortie !")

	Timer(delai, timerLEDEvent).start() # lance timer
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return # si vide	

# -- fin loop --

# timerEvent : appelé lors survenue evenement timer
def timerLEDEvent():
	
	global etatLED # traiter etatLED comme variable globale
	
	if etatLED==LOW:
		digitalWrite(LED,HIGH) # allume la LED
		Serial.println("La LED est allumee !") 
		etatLED=HIGH # memorise etat LED

	else:	
		digitalWrite(LED,LOW) # eteint la LED
		Serial.println("La LED est eteinte !") 
		etatLED=LOW # memorise etat LED

	Timer(delai, timerLEDEvent).start() # relance le timer
		
	
#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	#while(1): loop() # appelle fonction loop sans fin




