#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# annoncer l'adresse IP du système en synthèse vocale 

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
	
	Serial.println ("L'adresse IP du systeme est : " + Ethernet.localIP()) # affiche l'adresse IP du systeme

	ipSystem=Ethernet.localIP().split(".") # recupere l'ip sous forme d'une list 
	
	# message console 
	print ("Message en synthese vocale :")
	print ("L'adresse I P du systaime est la suivante : ")
	print (ipSystem[0] + ". point. " + ipSystem[1] + ". point. " + ipSystem[2] + ". point. " + ipSystem[3] )

	# synthese vocale 
	speak("L'adresse I P du systaime est la suivante : ")
	speak (ipSystem[0] + ". point. " + ipSystem[1] + ". point. " + ipSystem[2] + ". point. " + ipSystem[3] )
	
	# les "." permettent de ralentir la diction...
	

#--- fin setup

# -- loop -- 
def loop():
	return # si vide 
	
# -- fin loop --



#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
