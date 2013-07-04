#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test date et unixtime

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	print "Annee = " + year()
	print "Mois = " + month()
	print "Jour = " + day() 
	print "Jour de la semaine =  " +dayOfWeek() # Lundi = 1 ..Dimanche = 7
	print "-------" 
	
	print "Heures = " + hour() 
	print "Minutes = " + minute() 
	print "Secondes = " + second() 
	print "-------" 
	
	print "Unixtime = " + unixtime() 
 

	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




