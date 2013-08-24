#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits rÃ©servÃ©s - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Serveur TCP generant une page HTML avec code Javascript generant un vumetre simple

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crÃ©e un objet serveur utilisant le port 8080 = port HTTP > 1024

#--- setup --- 
def setup():
	global serverHTTP, ipLocale, port
	
	#serverHTTP.begin(10) # initialise le serveur - fixe nombre max connexion voulu
	serverHTTP.begin() # initialise le serveur - nombre max connexion par defaut = 5
	
	print ("Serveur TCP actif avec ip : " + ipLocale + " sur port : " + str(port) )
#--- fin setup

# -- loop -- 
def loop():
	
	global serverHTTP
	
	print ("Attente nouvelle connexion entrante...")
	clientDistant, ipDistante = serverHTTP.clientAvailable() # attend client entrant 
	# code bloque ici tant que pas client ! Si present, on recupere d'un coup objet client ET son ip
	
	print "Client distant connecte avec ip :"+str(ipDistante) # affiche IP du client

	#--- requete client ---
	requete=serverHTTP.readDataFrom(clientDistant) # lit les donnees en provenance client d'un coup
	
	print requete # affiche requete recue
	
	#--- reponse serveur --- 
	reponse=( # ( ... ) pour permettre multiligne.. 
	httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
	
	# contenu page - ici date / heure du serveur et mesure nalogique A2
	+
	
	pageHTML() # voir la fonction separee - pour clarte du code
	
	+"\n") # fin reponse 
	
	serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
	
	print "Reponse envoyee au client distant : "
	#print (bytes(reponse))
	print (reponse) # affiche la reponse envoyee
	
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
<!DOCTYPE HTML> 

<!-- Debut de la page HTML  --> 
<html> 
	<!-- Debut entete --> 
	<head> 
		<meta charset="utf-8" /> <!-- Encodage de la page  --> 
		<title>JavaScript: Test Canva </title> <!-- Titre de la page --> 

		<!-- Debut du code Javascript  --> 
		<script language="javascript" type="text/javascript"> 
		<!--
				// code javascript par X. HINAULT - www.mon-club-elec.fr - tous droits reserves - GPL v3  			 			 
		window.onload = function() { 

			var canvas = document.getElementById("nomCanvas"); // declare objet canvas a partir id 

			canvas.width = 300; // largeur canva 
			canvas.height = 300; // hauteur canva 

			if (canvas.getContext){ // la fonction getContext() renvoie True si canva accessible 

				var ctx = canvas.getContext("2d"); // objet contexte permettant acces aux fonctions de dessin 

				ctx.fillStyle = "rgb(1000,1000,1000)"; // couleur de remplissage 
				ctx.fillRect (0, 0, canvas.width, canvas.height); // rectangle de la taille du canva 

				//-- variables utiles 
				var largeur=40; 
				var hauteur=250; 
				var espacement=10; 

				// le code graphique ci-dessous 
				for (var i=0; i<6; i++) { // boucle pour 6 rectangles 

					// vu-metre 
					ctx.fillStyle = "rgb(127,127,127)"; // couleur remplissage - gris 
					ctx.fillRect (10+(i*largeur)+(i*espacement), canvas.height-10, largeur, -hauteur); // 6 rectangles gris 

					ctx.fillStyle = "rgb(255,0,0)"; // couleur remplissage - rouge 
					ctx.fillRect (10+(i*largeur)+(i*espacement), canvas.height-10, largeur, -hauteur/(i+1)); // 6 rectangles rouges 

				} // fin for 

			} // fin if getContext 
 			else { 

				// si trace non supporte 
			} // fin else 

		} // fin window.onload
		
		
		//--> 
		</script> 
		<!-- Fin du code Javascript -->     
	</head> 
	<!-- Fin entete --> 

		<!-- Debut Corps de page --> 
	<body > 
		<canvas id="nomCanvas" width="300" height="300"></canvas> 	 
		<br /> 
		Exemple de Vumetre basique dans un Canvas 

	</body> 
	<!-- Fin de corps de page   --> 

</html> 
<!-- Fin de la page  -->


"""
)  # fin page HTML
	return pageHTML # la fonction renvoie la page HTML



#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
