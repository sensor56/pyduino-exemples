!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# executer une commande systeme lors appui bouton poussoir

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

#--- setup --- 
def setup():
  pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 2 est en entree avec rappel au plus actif !")

# -- fin setup -- 

# -- loop -- 
def loop():
	
	if(digitalRead(BP)==APPUI): # si appui
		Serial.println("Appui BP!")
		
		# se place dans le repertoire voulu
		#path=homePath() # chemin utilisateur
		path="/home/ubuntu/"
		changedir(path) # se place dans le repertoire voulu
		
		# afficher le contenu du repertoire avec la commande ls 
		Serial.println("Contenu du repertoire " + path ) 
		executeCmd("ls") # execute la commande
		
		delay(250)  # anti-rebond
	
	delay(100) # pause entre 2 lecture du BP
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
