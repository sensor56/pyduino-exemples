#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test digitalRead

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
		
		Serial.println ("Adresse ip du systeme : " + Ethernet.localIP() ) # affiche l'adresse IP locale
		
		ipSystem=Ethernet.localIP().split(".") # recupere l'ip sous forme d'une list 
		speak("L'adresse I P du systaime est la suivante : ")
		speak (ipSystem[0] + ". point. " + ipSystem[1] + ". point. " + ipSystem[2] + ". point. " + ipSystem[3] )
		# les "." permettent de ralentir la diction...
		
		delay(250)  # anti-rebond
	
	delay(100) # pause entre 2 lecture du BP
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
