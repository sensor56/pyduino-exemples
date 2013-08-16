#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
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
	print("********* Lancer une application par reconnaissance vocale *********" )
	print ("===> Quelle application lancer ? ")
	print ("parmi : terminal , nagivateur, fichier, webcam, programmer, python, ..")
	print ("> Enregistrement du fichier voix (2 sec.) ...")
	
	recordSound(filepathAudio+filename,2) # enregistre son fichier voulu et duree voulue en secondes
	
	#playSound(filepathAudio+filename)
	
	chaine=analyzeVoice(filepathAudio+filename) # reconnaissance vocale 
	
	if chaine=="":
		#speak("Vous n'avez rien dit.")
		print("Vous n'avez rien dit.")
	else:
		#speak("Vous avez dit " + chaine)
		print("Vous avez dit " + chaine)
		
		# analyse chaine 
		chaine=chaine.lower() # met en minuscule 
		
		if "terminal" in chaine:
			executeCmdWait("lxterminal") # lance lxterminal 
		elif "navigateur" in chaine or "internet" in chaine:
			executeCmdWait("midori ") # lance midori
		elif "fichier" in chaine :
			executeCmdWait("pcmanfm") # lance pcmanfm
		elif "webcam" in chaine :
			executeCmdWait("guvcview") # lance guvcview
		elif "programm" in chaine :
			executeCmdWait("geany") # lance geany
		elif "python" in chaine :
			executeCmdWait("dreampie") # lance dreampie
		else:
			print("Chaine non valide")

	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




