#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Serveur TCP générant une page HTML avec code Javascript simple.

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crée un objet serveur utilisant le port 8080 = port HTTP > 1024

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
		<title>JavaScript: Trac&eacute; de courbe dans un Canva </title> <!-- Titre de la page --> 

		<!-- Debut du code Javascript  --> 
		<script language="javascript" type="text/javascript"> 
		<!--			 

		// variables / objets globaux - a declarer avant les fonctions pour eviter problemes de portee 
		var canvas= null; // pour objet Canvas 
		var contextCanvas = null; // pour objet context Canvas 
		var textInputX=null; 		 
		var textInputY=null; 
		 
		var delai=10; // intervalle a utiliser en ms 
		var compt=0; // variable de comptage 
		var x=0; // variable position 
		var y=0; // variable position 
		var xo=0; // variable position n-1 
		var yo=0; // variable position n-1 
		
		
		window.onload = function() { // fonction au lancement 
 			 
			canvas = document.getElementById("nomCanvas"); // declare objet canvas a partir id = nom 
			textInputX= document.getElementById("valeurX"); // declare objet champ text a partir id = nom 
			textInputY= document.getElementById("valeurY"); // declare objet champ text a partir id = nom 
			 
			canvas.width = 360; // largeur canvas 
			canvas.height = 300; // hauteur canvas 
			 
			textInputX.value=x; // fixe la valeur du champ 
			textInputY.value=y; // fixe la valeur du champ 
			 
			if (canvas.getContext){ // la fonction getContext() renvoie True si canvas accessible 

 				contextCanvas = canvas.getContext("2d"); // objet context global permettant acces aux fonctions de dessin 

				// le code graphique ci-dessous 

				// carre  de la taille du canvas 
				contextCanvas.fillStyle = "rgb(255,255,200)"; // couleur de remplissage rgb 0-255 
				contextCanvas.fillRect (0, 0, canvas.width, canvas.height); // rectangle 
				 
				// position initiale 
				contextCanvas.fillStyle = "rgb(0,0,255)"; // couleur de remplissage rgb 0-255 
				contextCanvas.fillRect (x,canvas.height-y-1, 1,1); // context.fillRect(x,y,width,height) - dessine 1 pixel 

				// parametres graphique 
				contextCanvas.lineWidth=1; // largeur ligne avec lineTo() 
				contextCanvas.strokeStyle = "rgb(0,0,255)"; // couleur de pourtour rgb 0-255 
				 
 				// intervalle de rafraichissement 
 				//interval=window.setInterval(draw, 100); // fixe intervalle en ms et fonction a executer 
 				window.setTimeout(draw, delai); // fixe intervalle en ms et fonction a executer - alternative 
 	 
			} // fin si canvas existe 

			else { 
				window.alert("Canvas non disponible")// code si canvas non disponible 
			} // fin else 

		} // fin window.onload


		function draw() { // fonction qui est appelee  a intervalle regulier 
		 
			if (contextCanvas!=null) { 

				// -- coordonnees x,y courantes 
				x=x+1; // incremente x 
				if (x>canvas.width)x=0; // RAZ x 
				 
				y=(canvas.height-1)/2+ (Math.cos(2*x * Math.PI/180) * (canvas.height-1)/2) ; // valeur de y = cos (x) 
				y=Math.round(y); // valeur entiere 
				 
				if (x==0) { // reinitialisation dessin si x a ete reinitialise 
					 
					contextCanvas.moveTo(x,y); // deplace sans trace 

					// rect plein  de la taille du canvas = efface canvas pour nouveau trace 
					contextCanvas.fillStyle = "rgb(255,255,200)"; // couleur de remplissage rgb 0-255 
					contextCanvas.fillRect (0, 0, canvas.width, canvas.height); // rectangle 

					xo=0; // RAZ xo point n-1					 
					 
				} // fin if x==0 
				 
				else { // si x diff 0 : on trace la ligne jusqu'au point courant 
					contextCanvas.beginPath(); // reinitialise trace - sinon toutes les actions de dessins sont reexecutees 
					contextCanvas.moveTo(xo,canvas.height-1-yo); // trace virtuellement la ligne 
					contextCanvas.lineTo(x,canvas.height-1-y); // trace virtuellement la ligne 
					contextCanvas.closePath(); // reinitialise trace - sinon toutes les actions de dessins sont reexecutees 
					 
					contextCanvas.stroke(); // trace le pourtour - ne pas oublier 

					textInputX.value=x; // fixe la valeur du champ 
					textInputY.value=y; // fixe la valeur du champ 	 
					xo=x; // memorise n-1 
					yo=y; // memorise n-1 

				} // fin else 
				 				 
				window.setTimeout(draw, delai); // fixe nouvel intervalle en ms et fonction a executer 
				 
			}	// fin if context !=null 
		 
		} // fin draw	

		//--> 
		</script> 
		<!-- Fin du code Javascript -->     

	</head> 
	<!-- Fin entete --> 
     
	<!-- Debut Corps de page HTML --> 
	<body > 
 
 		<canvas id="nomCanvas" width="300" height="300"></canvas> 

		<br /> 

 		X=<input type="text" id="valeurX" /> 
 		Y=<input type="text" id="valeurY" />			 
			 
		<br /> 
		Exemple de courbe avec un Canvas
		 
	</body> 
	<!-- Fin de corps de page HTML  --> 
     	 
</html> 
<!-- Fin de la page HTML  -->
"""
)  # fin page HTML
	return pageHTML # la fonction renvoie la page HTML



#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
