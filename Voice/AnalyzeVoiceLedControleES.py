#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# broches E/S controlees par la voix

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
#noLoop=True

ledTemoin=0  # LED témoin ok pour parler

#--- setup --- 
def setup():
  
	# broche de led temoin
	pinMode(ledTemoin, OUTPUT) # broche en sortie
	digitalWrite(ledTemoin, LOW) # eteint LED
	
	# broches ES utilisees
	for pin in range (1,8): # defile broche 1-7 
		pinMode(pin, OUTPUT) # broche sortie
		digitalWrite(pin, LOW) # eteint LED
# -- fin setup -- 

# -- loop -- 
def loop():
	
	# fichier d'enregistrement a utiliser
	filepathAudio=homePath()+dataPath(AUDIO)
	filename="test.wav"
	print (filepathAudio+filename)
	
	#speak("Test de reconnaissance vocale. Dites quelque chose")
	
	digitalWrite(ledTemoin,HIGH) # LED pour OK parler
	
	recordSound(filepathAudio+filename,3) # enregistre son fichier voulu et duree voulue en secondes
	
	digitalWrite(ledTemoin,LOW) # LED Stop parler
	
	#playSound(filepathAudio+filename)
	
	chaine=analyzeVoice(filepathAudio+filename) # reconnaissance vocale 
	
	if chaine=="": # si rien dit
		#speak("Vous n'avez rien dit.")
		pass
	else: # si dit quelque chose 
		speak("Vous avez dit " + chaine)
		
		# analyse de la chaine recue
		chaine=chaine.lower() # met en minuscule 
		
		print chaine # affiche chaine reconnue
		
		# analyse chaine reconnue et met LED dans etat voulu
		if "allum" in chaine:
			if "1" in chaine or "un" in chaine : digitalWrite(1,HIGH)
			if "2" in chaine or "deux" in chaine : digitalWrite(2,HIGH)
			if "3" in chaine or "trois" in chaine : digitalWrite(3,HIGH)
			if "4" in chaine or "quatre" in chaine : digitalWrite(4,HIGH)
			if "5" in chaine or "cinq" in chaine : digitalWrite(5,HIGH)
			if "6" in chaine or "six" in chaine : digitalWrite(6,HIGH)
			if "7" in chaine or "sept" in chaine : digitalWrite(7,HIGH)
			if "tou" in chaine :
				for i in range(1,8):digitalWrite(i,HIGH)
		
		elif "éteindre" in chaine:
			if "1" in chaine or "un" in chaine : digitalWrite(1,LOW)
			if "2" in chaine or "deux" in chaine : digitalWrite(2,LOW)
			if "3" in chaine or "trois" in chaine : digitalWrite(3,LOW)
			if "4" in chaine or "quatre" in chaine : digitalWrite(4,LOW)
			if "5" in chaine or "cinq" in chaine : digitalWrite(5,LOW)
			if "6" in chaine or "six" in chaine : digitalWrite(6,LOW)
			if "7" in chaine or "sept" in chaine : digitalWrite(7,LOW)
			if "tou" in chaine :
				for i in range(1,8):digitalWrite(i,LOW)

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




