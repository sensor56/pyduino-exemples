#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test Serial.println()

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
  Serial.begin(115200) # emulation Serial.begin - pas indispensable
	
	Serial.println("Salut")
	
	Serial.println(12)
	Serial.println(12,DEC)
	Serial.println(12,BIN) # 0b1100
	Serial.println(12,OCT)
	Serial.println(12,HEX) # 0xc
	
	Serial.println(str("%.4f" % pi)) # pi avec 4 décimales
	
	Serial.println(today("/")) # 09/07/2013
	
	Serial.println(nowtime(":")) # 14:35:13
	
	Serial.println(homePath()) # /home/ubuntu/
	
	chaineMulti="""
HTTP/1.0 200 OK
Content-Type: text/html
Connnection: close

"""
	Serial.println(chaineMulti)
	
	
# -- fin setup -- 

# -- loop -- 
def loop():
	#Serial.println("Coucou")
	#delay(1000)
	return # si vide 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




