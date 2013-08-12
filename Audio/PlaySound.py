#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test playsound

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
  
	# exemples de sons :  wget -4 http://www.mon-club-elec.fr/mes_downloads/pyduino_sons.tar.gz
	
	filepathAudio=homePath()+sourcesPath(AUDIO)+"star_wars/"
	filename="r2d2.mp3"
	print filepathAudio+filename
	
	playSound(filepathAudio+"r2d2.mp3") # joue le son

	playSound(filepathAudio+"r2d2_5.mp3") # joue le son
	
	setSourcesPath(AUDIO, "sources/audio/star_wars/") # fixe le chemin sources audio courant relatif à main/ 
	print sourcesPath(AUDIO) # affiche le chemin audio courant
	playSound("r2d2_3.mp3") # utilise le chemin sources audio courant

	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
