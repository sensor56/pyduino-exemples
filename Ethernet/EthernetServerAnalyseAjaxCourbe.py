#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Tester l'envoi d'une requete Ajax, l'envoi d'une reponse et la gestion d'une reponse Ajax

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
compt=0 # variable de comptage 
ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crée un objet serveur utilisant le port 8080 = port HTTP > 1024

#--- setup --- 
def setup():
	
	# -- serveur TCP -- 
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
	
	#print requete # affiche requete recue - debug
	
	# analyse de la requete
	
	#====== si requete ajax ======
	if requete.startswith("GET /ajax"): # si la requete recue est une requete ajax
		
		lignesRequete=requete.splitlines() # recupere la requete est list de lignes
		print lignesRequete[0]  # premiere ligne = la requete utile
		
		#--- reponse serveur requete formulaire --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu reponse AJAX
		+
		
		reponseAJAX() # voir la fonction separee - pour clarte du code
		
				+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "
		#print (bytes(reponse))
		print (reponse) # affiche la reponse envoyee

	#====== si requete GET simple = premiere requete => envoi page HTML+JS initiale ======
	elif requete.startswith("GET"): # si la requete commence par GET seul = premiere page 
		
		print "Requete GETrecue valide"
		
		#-- code Pyduino a executer au besoin 
		global compt
		compt=0 # RAZ compt
		
		#--- reponse serveur requete initiale --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu page HTML+ JS initiale
		+
		
		pageInitialeHTMLJS() # voir la fonction separee - pour clarte du code
		
		+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "
		#print (bytes(reponse))
		#print (reponse) # affiche la reponse envoyee - debug
		
	#====== si requete pas valide ======
	else : # sinon requete pas valide
		
		print ("Requete pas valide")
		
	
	#====== une fois la page envoyée ======
	#serverHTTP.close()
	# remarque : le socket = serveur doit rester ouvert
	
	# quand on quitte l'application: la connexion TCP reste active un peu donc erreur si re-execution trop rapide du code
	# on peut utiliser un port voisin dans ce cas... 

	delay(50) # entre 2 loop()
	
# -- fin loop --

#========== fonction fournissant la page HTML + JS initiale incluant code javascript AJAX ======
def pageInitialeHTMLJS():
	
	contenuPageInitialeHTMLJS=( # debut page HTML 
"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Test reponse Ajax</title>
        
        <!-- Debut du code Javascript  -->
        <script language="javascript" type="text/javascript">
        <!-- 
        
        // variables / objets globaux
        var canvas= null; 
        var contextCanvas = null;
        var textInputX=null;
        var textInputY=null;
        
        var delai=100; // en ms 
        var compt=0;
        var x=0;
        var y=0;
        var xo=0;
        var yo=0;
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
			canvas = document.getElementById("nomCanvas");
			canvas.width = 360;
			canvas.height = 300;
			
			textInputX= document.getElementById("valeurX");
			textInputY= document.getElementById("valeurY");
			textInputX.value=x;
			textInputY.value=y;
			
			if (canvas.getContext){ // si canvas existe 
				contextCanvas = canvas.getContext("2d");
				contextCanvas.fillStyle = "rgb(255,255,200)";
				contextCanvas.fillRect (0, 0, canvas.width, canvas.height);
				
				// 1er pixel
				contextCanvas.fillStyle = "rgb(0,0,255)";
				contextCanvas.fillRect (x,canvas.height-y-1, 1,1);
				
				// parametres graphiques
				contextCanvas.lineWidth=1;
				contextCanvas.strokeStyle = "rgb(0,0,255)";
				
				setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // setTimeOut avec fonction inline : 1er appel de la fonction requete Ajax
				// nb : setTimeout() n'applique delai qu'une fois
			
			} // fin si canvas existe
			
			else {
				window.alert("Canvas non disponible");
			} // fin else 
			
        } // fin window.onload
        
        //---------- fonction de requete AJAX -----
        function requeteAjax(callback) { // la fonction recoit en parametre la fonction de callback qui gere la reponse Ajax
			// la fonction de callback appelee sera celle definie dans setTimeOut : manageAjaxData
			var xhr = XMLHttpRequest(); // declare objet de requete AJAX  - OK Firefox
			
			xhr.open("GET", "/ajax", true); // definition de la requete envoyee au serveur ici : GET /ajax
			xhr.send(null); // envoi de la requete
			
			xhr.onreadystatechange = function() { // fonction de gestion de l'evenement onreadystatechange
				if (xhr.readyState == 4 && xhr.status == 200) { // si reponse OK
					callback(xhr.responseText); // appel fonction gestion reponse en passant texte reponse en parametre
				} // fin if 
			}; // fin function onreadystatechange
			
		} // fin fonction requeteAjax
		
		//------ fonction qui sera utilisee en fonction de callback = gestion de la reponse Ajax
		// cette fonction est executee cote client suite reception de la chaine de reponse ajax en provenance serveur
		function manageReponseAjax(stringDataIn) { // la fonction recoit en parametre la chaine de texte de la reponse Ajax
			
			// ici la fonction assure le trace de la courbe en utilisant la donnee recue
			
			//--- debut dessin courbe -- 
			
			if (contextCanvas!=null) { // si canva disponible
				//-- coord x,y courantes
				x=x+5;
				if (x>canvas.width)x=0;
				
				y=Number(stringDataIn)
				y=y/1023*(canvas.height-1)
				
				// -- trace courbe -- 
				// RAZ courbe si x==0 
				if (x==0) {
					contextCanvas.moveTo(x,y);
					contextCanvas.fillStyle = "rgb(255,255,200)";
					contextCanvas.fillRect (0, 0, canvas.width, canvas.height);
					xo=0;
					} // fin if x==0 
				
				// sinon trace ligne point courant 
				else {
					contextCanvas.beginPath();
					contextCanvas.moveTo(xo,canvas.height-yo-1);
					contextCanvas.lineTo(x,canvas.height-y-1);
					contextCanvas.closePath();
					contextCanvas.stroke();
					
					textInputX.value=x;
					textInputY.value=Number(stringDataIn);
					
					xo=x;
					yo=y;
					
				} // fin else
			
			}// fin if context !=null 
			
			// -- fin dessin courbe -- 
			
			// reinitialise delai rappel requete
			setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // relance delai avant nouvelle requete Ajax
			
		} // fin fonction gestion de la reponse Ajax
		
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

    <body>  
      
	<canvas id="nomCanvas" width="300" height="300"></canvas>
	<br/>
	X=<input type="text" id="valeurX" />
	Valeur (0-1023) = <input type="text" id="valeurY" />
	
	<br/>
	Serveur Pyduino : Test courbe avec reponse de requete Ajax 
	<br/>
	
    </body>

</html>
"""

)  # fin page HTML+JS initiale
	return contenuPageInitialeHTMLJS # la fonction renvoie la page HTML

#===================== Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX
def reponseAJAX():
	
	# definition des variables a uiliser dans la reponse
	global compt
	compt=compt+1
	if compt>1023: compt=0 # RAZ compt
	
	# la reponse 
	reponseAjax=( # debut page reponse AJAX
#"""123, 456, 789""" 
str(compt)
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
