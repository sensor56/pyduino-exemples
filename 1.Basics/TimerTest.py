#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# code minimal avec Timer (décharge CPU) 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True # bloque loop automatique

#--- setup --- 
def setup():
  
	# instructions setup ici 
	
	loop() # premier appel de la fonction loop
	
# -- fin setup -- 

# -- loop -- 
def loop(): # la fonction loop s'auto-appelle a intervalles reguliers
	
	# instructions loop ici 
	
	timer(100, loop) # appelle fonction loop apres intervalle en ms
	
	# resultats sur pcduino avec htop : 
	# en mode loop auto permanent : usage CPU = 100%
	# 100 ms ~10 appels par seconde = 5% usage CPU 
	# 10 ms ~ 100 appels par seconde = 20% usage CPU 
	# 5 ms ~ 200 appels par seconde = 30% usage CPU => bon compromis
	# 1 ms ~ 1000 appels par seconde = 60% usage CPU
	# 0.5ms ~ 2000 appels par seconde = 75% usage CPU
	# 0.1ms ~ 10 000 appels par seconde = 95% usage CPU

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
