#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test playvideo

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
#noLoop=True

#--- setup --- 
def setup():
	
	# exemples de video :  
	# cd home/ubuntu/sources/video
	# wget -4 http://www.mon-club-elec.fr/mes_videos/plancton_cnrs_fr.mp4
	# wget -4 http://www.mon-club-elec.fr/mes_videos/incendium_vimeo.mp4

	filepathVideo=homePath()+sourcesPath(VIDEO)
	filename="plancton_cnrs_fr.mp4"
	#filename="incendium_vimeo.mp4"
	print filepathVideo+filename
	
	playVideo(filepathVideo+filename)
	
# -- fin setup -- 

# -- loop -- 
def loop():
	delay(1000)
	Serial.println(".")
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
