#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# appui BP annonce resultat mesure analogique

#from pyduino import * # importe les fonctions Arduino pour Python
from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

#--- setup --- 
def setup():
  pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 2 est en entree avec rappel au plus actif !")

# -- fin setup -- 

# -- loop -- 
def loop():
	
	if(digitalRead(BP)==APPUI): # si appui
		
		Serial.println("Appui BP!")
		mesure=analogRead(A2) # mesure analogique sur la broche A2
		Serial.println("Mesure brute A2 = " + str(mesure))
		
		mesuremV=analogReadmV(A2)  # mesure en millivolts.
		Serial.println("Mesure mV A2 = " + str(mesuremV))
		
		# message synthese vocale 
		message=("La mesure analogique sur la broche A2 vaut  " + str(mesure)
		+ ". Sur une plage de mesure 12 bits. qui ses tend de 0 a 4095."
		+" soit une tension de " + str(mesuremV) + " millivolts.")
		
		print ("\nMessage en synthese vocale : ")
		print message
		
		speak(message) # synthese vocale 
		
		delay(250)  # anti-rebond
	
	delay(100) # pause entre 2 lecture du BP
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin
