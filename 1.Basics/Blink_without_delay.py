#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# LED clignote - sans delay - avec timer

from pyduino import * # importe les fonctions Arduino pour Python

from threading import Timer

# entete declarative
LED=2  # declare la broche a utiliser
etatLED=LOW # memorise etat LED

#--- setup --- 
def setup():
	
	pinMode(LED,OUTPUT) # met la broche en sortie
	#Serial.println("La broche " +str(LED)+ " est en sortie !")

	Timer(0.1, timerLEDEvent).start() # lance timer
	
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
		#Serial.println("La LED est allumée !") 
		etatLED=HIGH # memorise etat LED
		#Timer(0.00010, timerLEDEvent).start() # relance le timer - essai PWM soft

	else:	
		digitalWrite(LED,LOW) # eteint la LED
		#Serial.println("La LED est éteinte !") 
		etatLED=LOW # memorise etat LED
		#Timer(0.00100, timerLEDEvent).start() # relance le timer - essai PWM soft

	Timer(0.1, timerLEDEvent).start() # relance le timer
		
	
#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	#while(1): loop() # appelle fonction loop sans fin




