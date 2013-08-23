#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Controler une LED a partir bouton d'un formulaire HTML

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=3 # broche utilisee pour la LED
etatLED=LOW # reflet etat de la LED - eteinte au depart

ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crée un objet serveur utilisant le port 8080 = port HTTP > 1024

#--- setup --- 
def setup():
	
	#-- LED -- 
	pinMode(LED,OUTPUT) # broche en sortie
	digitalWrite(LED,etatLED)  # met la LED dans l'etat voulu - eteinte au debut
	Serial.println("Broche " + str(LED) + " en sortie mise au niveau bas.")
	
	# -- serveur TCP -- 
	global serverHTTP, ipLocale, port
	
	#serverHTTP.begin(10) # initialise le serveur - fixe nombre max connexion voulu
	serverHTTP.begin() # initialise le serveur - nombre max connexion par defaut = 5
	
	print ("Serveur TCP actif avec ip : " + ipLocale + " sur port : " + str(port) )
#--- fin setup

# -- loop -- 
def loop():
	
	global serverHTTP, LED, etatLED
	
	print ("Attente nouvelle connexion entrante...")
	clientDistant, ipDistante = serverHTTP.clientAvailable() # attend client entrant 
	# code bloque ici tant que pas client ! Si present, on recupere d'un coup objet client ET son ip
	
	print "Client distant connecte avec ip :"+str(ipDistante) # affiche IP du client

	#--- requete client ---
	requete=serverHTTP.readDataFrom(clientDistant) # lit les donnees en provenance client d'un coup
	
	print requete # affiche requete recue
	
	# analyse de la requete
	
	if requete.startswith("GET"): # si la requete commence par GET seul = premiere page 
		
		print "Requete recue valide"
		
		# extraction requete utile = la premiere ligne
		lignesRequete=requete.splitlines() # recupere la requete est list de lignes
		requeteUtile=lignesRequete[0]  # premiere ligne = la requete utile
		print requeteUtile
		
		# analyse requete utile
		if "LED=ON" in requeteUtile: # la requete contient LED=ON cad si case cochee
			Serial.println("La chaine LED=ON est valide !")
			etatLED=HIGH # memorise etat LED pour renvoie reponse adaptee
		else:
			Serial.println("La chaine LED=ON est absente !")
			etatLED=LOW  # memorise etat LED pour renvoi reponse adaptee
		
		digitalWrite(LED,etatLED)  # met la LED dans l'etat voulu
		
		#--- reponse serveur requete initiale --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu page HTML initiale
		+
		
		pageHTML() # voir la fonction separee - pour clarte du code
		
		+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "
		#print (bytes(reponse))
		#print (reponse) # affiche la reponse envoyee
		
	#====== si requete pas valide ======
	else : # sinon requete pas valide
		
		print ("Requete pas valide")
		
	
	#====== une fois la page envoyée ======
	#serverHTTP.close()
	# remarque : le socket = serveur doit rester ouvert
	
	# quand on quitte l'application: la connexion TCP reste active un peu donc erreur si re-execution trop rapide du code
	# on peut utiliser un port voisin dans ce cas... 

	delay(10) # entre 2 loop()
	
# -- fin loop --

#--- fonction fournissant la page HTML --- 
def pageHTML():
	
	pageHTML=( # debut page HTML 
"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Controler une LED </title>
    </head>

    <body>
        
        Formulaire HTML de controle d'une LED
        <br>
        <img src="http://www.mon-club-elec.fr/mes_images/communs/led_rouge_5mm.gif"> </CENTER>
        <br>
        
        <form method=get action="http://"""+ Ethernet.localIP()+""":8080">
            <INPUT type="checkbox" value="ON" name="LED" """) # fin premiere partie

	if etatLED==HIGH : pageHTML=pageHTML+ """ checked """
	
	pageHTML=(pageHTML+"""> Allumer/Eteindre la LED
            <br> 
            <INPUT type="submit" value="Envoi" name="Envoi">
        </form>
        
        """)  # fin suite page HTML
	
	# insertion selon etat LED 
	if etatLED==HIGH : 
		pageHTML=(pageHTML+ """
        <br>
        LED ON 
    """)
	else:
		pageHTML=(pageHTML+ """
        <br>
        LED OFF 
	""")
	
	# fin de la page HTML 
	pageHTML=(pageHTML+"""
        </body>

</html>
"""

)  # fin suite page HTML


	return pageHTML # la fonction renvoie la page HTML

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
