#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# appui sur un BP declenche capture image webcam

#from pyduino import * # importe les fonctions Arduino pour Python
from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

filepathAudio=""
filepathImage=""
compt=0

#--- setup --- 
def setup():
  pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 2 est en entree avec rappel au plus actif !")
	
	global filepathAudio, filepathImage
	
	
	# exemples de sons :  wget -4 http://www.mon-club-elec.fr/mes_downloads/pyduino_sons.tar.gz
	
	filepathAudio=homePath()+sourcesPath(AUDIO)+"photo/"
	print filepathAudio
	
	filepathImage=homePath()+dataPath(IMAGE)
	print filepathImage
	
	# initialisation webcam
	initWebcam(0,640,480) # la resolution doit etre supportee par la webcam !
	
	loop() # premier appel loop()

# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepathAudio, filepathImage, compt
	
	if(digitalRead(BP)==APPUI): # si appui
		Serial.println("Appui BP!")
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
		delay(250)  # anti-rebond
	
	timer(200, loop) # relance timer - la fonction loop s'auto-appelle 
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




