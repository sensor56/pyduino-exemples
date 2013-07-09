#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test appui BP 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui
LED=3 # declare broche utilise pour la LED

#--- setup --- 
def setup():
  pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 2 est en entree avec rappel au plus actif !")
	
	pinMode(LED,OUTPUT) # broche en sortie
	Serial.println("La broche " + str(LED)+" est en sortie. ")

# -- fin setup -- 

# -- loop -- 
def loop():
	
	if(digitalRead(BP)==APPUI): # si appui
		digitalWrite(LED,HIGH) # allume la LED
	else: 
		digitalWrite(LED,LOW)  # eteint la LED

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin




