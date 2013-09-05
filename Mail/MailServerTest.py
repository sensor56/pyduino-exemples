#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test envoi mail 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup --- 
def setup():
	
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
	
	print ""
	
	# contenu du mail 
	mailServer.setSubject("Mail de test")
	mailServer.setMsg("Coucou. Nous sommes le " + today("/") + ". Il est " + nowtime(":")+".")
	
	# affiche le header 
	print mailServer.getHeader()
	
	# envoi message 
	mailServer.sendMail()
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return  # si vide
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin



