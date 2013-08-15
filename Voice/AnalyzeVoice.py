#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test analyzeVoice 

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
#noLoop=True

#--- setup --- 
def setup():
	
	return
# -- fin setup -- 

# -- loop -- 
def loop():
	
	filepathAudio=homePath()+dataPath(AUDIO)
	filename="test.wav"
	#print (filepathAudio+filename)
	
	print ("--------------------------------")
	print("********* Test de reconnaissance vocale *********" )
	print ("===> Dites quelque chose !")
	print ("> Enregistrement du fichier voix (3 sec.) ...")
	
	recordSound(filepathAudio+filename,3) # enregistre son fichier voulu et duree voulue en secondes
	
	#playSound(filepathAudio+filename)
	
	chaine=analyzeVoice(filepathAudio+filename) # reconnaissance vocale 
	
	if chaine=="":
		#speak("Vous n'avez rien dit.")
		print("Vous n'avez rien dit.")
	else:
		#speak("Vous avez dit " + chaine)
		print("Vous avez dit " + chaine)
	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




