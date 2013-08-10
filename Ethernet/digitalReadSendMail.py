#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Aout 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# l'appui sur un bouton poussoir envoie un mail !

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
BP=2  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

mailServer=None

#--- setup --- 
def setup():
  
	# config BP
	pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 2 est en entree avec rappel au plus actif !")
	
	# config serveur mail 
	global mailServer
	mailServer=MailServer()
	
	#-- parametres du serveur smtp
	mailServer.setName("serveurmail.expediteur.fr")
	mailServer.setPort(25)
	
	#-- expediteur
	mailServer.setFromMail("adresse@expediteur.fr")
	mailServer.setFromPassword("motdepasseexpediteur")
	
	#-- destinataire
	mailServer.setToMail("adresse@destinataire.fr")
	
	# affiche parametres 
	print "serveur smtp : "
	print "nom : " + mailServer.name
	print "port : " + str(mailServer.port)
	print "expediteur :"
	print "adresse mail : " + mailServer.fromMail
	print "mot de passe : " + mailServer.fromPassword
	print "destinataire : "
	print "adresse mail : " + mailServer.toMail
	
	print "-----------------"

# -- fin setup -- 

# -- loop -- 
def loop():
	
	global mailServer
	
	if(digitalRead(BP)==APPUI): # si appui
		Serial.println("Appui BP!")
		Serial.println("Mail en cours d'envoi...")
		
		# contenu du mail 
		mailServer.setSubject("Envoi mail par Pyduino")
		mailServer.setMsg("Appui sur bouton poussoir le " + nowdatetime()+".")
		
		# envoi message 
		mailServer.sendMail()
		
		Serial.println("Fin d'envoi du mail.")
		Serial.println("")
		
		delay(250)  # anti-rebond
	
	delay(100) # pause entre 2 lecture du BP
	
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin



