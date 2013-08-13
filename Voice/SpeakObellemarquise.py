#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test speak dans la langue de moliere !

from pyduinoMultimedia import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
	
	speak(""" je ne veux que ce que je vous ai dit : 
	Belle Marquise, vos beaux yeux me font mourir damour.""", ESPEAK)
	
	speak("""Il faut bien étendre un peu la chose.
	""",PICO)
	
	speak(""" Non, vous dis-je, je ne veux que ces seules paroles-la 
	dans le billet ; mais tournez a la mode ; bien arrangez comme il faut. 
	Je vous prie de me dire un peu, pour voir, les diverses maniaires dont on les peut mettre.
	""", ESPEAK)
	
	speak("""On les peut mettre premiairement comme vous avez dit.
	Belle Marquise, vos beaux yeux me font mourir damour. 
	Ou bien : damour mourir me font, belle Marquise, vos beaux yeux. 
	Ou bien : Vos yeux beaux damour me font, belle Marquise, mourir. 
	Ou bien : Mourir vos beaux yeux, belle Marquise, damour me font. 
	Ou bien : Me font vos yeux beaux mourir, belle Marquise, damour.
	""",PICO)
	
	speak(""" Mais de toutes ces fassons-la, 
	laquelle est la meilleure ?""", ESPEAK)
	
	speak("""Celle que vous avez dite : Belle Marquise, vos beaux yeux me font mourir damour.""", PICO)
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
