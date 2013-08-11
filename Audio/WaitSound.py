#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Aout 2013 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test WaitSound

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python + Multimedia

# entete declarative

#--- setup --- 
def setup():
  return # si vide
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	Serial.println("Ecoute bruit... ")
	#waitSound() # attend un son... fonction bloquante - seuil detection par defaut = 10% pendant 0.1sec
	waitSound(25,0.1) # attend un son... fonction bloquante - seuil detection 25% pendant 0.1sec
	Serial.println("Detection de bruit ! Il est " + nowtime(":"))
	
	# lancer simultanement <pulse audio volume control> et regler les niveaux si besoin
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




