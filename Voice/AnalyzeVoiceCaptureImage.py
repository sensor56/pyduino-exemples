#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Capturer une image par commande vocale 

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

filepathVoice=""
filenamVoice=""

filepathAudio=""
filepathImage=""
compt=0

#--- setup --- 
def setup():
	
	global filepathImage, filepathAudio, filepathVoice, filenameVoice 
	
	# exemples de sons :  wget -4 http://www.mon-club-elec.fr/mes_downloads/pyduino_sons.tar.gz
	
	filepathAudio=homePath()+sourcesPath(AUDIO)+"photo/"
	print filepathAudio
	
	filepathImage=homePath()+dataPath(IMAGE)
	print filepathImage
	
	filepathVoice=homePath()+dataPath(AUDIO)
	filenameVoice="test.wav"
	print (filepathVoice+filenameVoice)
	
	# initialisation webcam
	initWebcam(0,640,480) # la resolution doit etre supportee par la webcam !
	
	loop() # premier appel loop()
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepathVoice, filenameVoice, filepathAudio, filepathImage, compt
	
	print ("--------------------------------")
	print("********* Capturer une image par commande vocale *********" )
	print ("===> Dites \"photo\" quand vous etes pret ! ")
	print ("> Enregistrement du fichier voix (2 sec.) ...")
	
	recordSound(filepathVoice+filenameVoice,2) # enregistre son fichier voulu et duree voulue en secondes
	
	#playSound(filepathAudio+filename)
	
	chaine=analyzeVoice(filepathVoice+filenameVoice) # reconnaissance vocale 
	
	if chaine=="":
		#speak("Vous n'avez rien dit.")
		print("Vous n'avez rien dit.")
	else:
		#speak("Vous avez dit " + chaine)
		print("Vous avez dit " + chaine)
		
		# analyse chaine 
		chaine=chaine.lower() # met en minuscule 
		
		if "photo" in chaine:
			playSound(filepathAudio+"camera-click-1.wav") # joue le son
			
			closeImage() # ferme visionneur image precedente
			
			# capture image
			filename="photo"+str(compt)+".jpg"
			print filepathImage+filename
			captureImage(filepathImage+filename) # charge une image dans le buffer a partir webcam
			compt=compt+1
			
			#addTextOnImage(today("/")+"@"+nowtime(":"), 10,height()-30, green) # ajoute texte sur image 
			#addTextOnImage(nowdatetime(), 10,height()-20, yellow,0.75) # ajoute texte sur image 
			
			saveImage(filepathImage+filename) # enregistre l'image 
			delay(500)
			
			showImage(filepathImage+filename) # affiche l'image 
			
			exit(0) # sort de l'exécution
		
		else:
			print("Chaine non valide")
			
	timer(2000, loop) # relance timer - la fonction loop s'auto-appelle 
	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




