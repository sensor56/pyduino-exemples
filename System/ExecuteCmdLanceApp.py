#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test execute commande système 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
compt=0
app=None

#--- setup --- 
def setup():

  # executeCmd()
	app=executeCmd("midori") # execute commande et renvoie processus

	delay(20000) # pause 20 secondes
	
	app.terminate()  # stoppe proprement le processus créé précédemment
	print ("application stoppee")
	
# -- fin setup -- 

# -- loop -- 
def loop():
	print("loop")
	delay(1000)
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
