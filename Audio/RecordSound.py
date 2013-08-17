#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test recordSound

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
	
	filepathAudio=homePath()+dataPath(AUDIO)
	filename="test.wav"
	print (filepathAudio+filename)
	
	print "Enregistrement d'un son pendant 5 secondes : veuillez parler !"
	recordSound(filepathAudio+filename,5) # enregistre son fichier voulu et duree voulue en secondes
	
	playSound(filepathAudio+filename) # lecture du fichier son 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
