#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test analyzeVoice avec LED de visualisation enregistrement

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
#noLoop=True

ledTemoin=0  # LED témoin ok pour parler

#--- setup --- 
def setup():
	
	pinMode(ledTemoin, OUTPUT) # broche en sortie
	digitalWrite(ledTemoin, LOW) # eteint LED
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	filepathAudio=homePath()+dataPath(AUDIO)
	filename="test.wav"
	print (filepathAudio+filename)
	
	#speak("Test de reconnaissance vocale. Dites quelque chose")
	
	digitalWrite(ledTemoin,HIGH) # OK parler
	
	recordSound(filepathAudio+filename,3) # enregistre son fichier voulu et duree voulue en secondes
	
	digitalWrite(ledTemoin,LOW) # Stop parler
	
	#playSound(filepathAudio+filename)
	
	chaine=analyzeVoice(filepathAudio+filename) # reconnaissance vocale 
	
	if chaine=="":
		#speak("Vous n'avez rien dit.")
		pass
	else:
		speak("Vous avez dit " + chaine)
	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




