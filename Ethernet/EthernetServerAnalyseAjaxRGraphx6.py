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
		
		reponseAJAXServeur() # voir la fonction separee - pour clarte du code
		
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
        
	   // code javascript par X. HINAULT - www.mon-club-elec.fr - tous droits reserves - 2013 - GPL v3

		function path(jsFileNameIn) { // fonction pour fixer chemin absolu                               
				var js = document.createElement("script");
				js.type = "text/javascript";
				// js.src = \" http://www.mon-club-elec.fr/mes_javascripts/rgraph/\"+jsFileNameIn; // pour test si pas RGraph locale...
				js.src = "http://"+window.location.hostname+":80"+"/javascript/rgraph/"+jsFileNameIn; // si utilisation server http local port 80
				document.head.appendChild(js);                                   
				//alert(js.src); // debug
		}

		//---- fichiers a charger ---                            
		path('RGraph.common.core.js');
		path('RGraph.common.dynamic.js');
		path('RGraph.common.effects.js');
		path('RGraph.gauge.js');                                 

        // variables / objets globaux
        var canvas= null; 
        var contextCanvasRGraph = null;
        
        var gauge= null;
        
        var textInputRGraph=null;
        
        var delai=50; // delai en ms entre 2 requetes AJAX
		var val=0;
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
			// parametres sont : nom du canva, min, max, valeur courante
			
			gauge=new Array();
			
			gauge[1] = new RGraph.Gauge('CanvasRGraph1', 0, 1023, 100); // declare widget graphique
			gauge[1].Draw(); // dessine le widget graphique dans le canvas

		   gauge[2] = new RGraph.Gauge('CanvasRGraph2', 0, 1023, 200); // declare widget graphique
			gauge[2].Draw(); // dessine le widget graphique dans le canvas

		   gauge[3] = new RGraph.Gauge('CanvasRGraph3', 0, 1023, 300); // declare widget graphique
			gauge[3].Draw(); // dessine le widget graphique dans le canvas

		   gauge[4] = new RGraph.Gauge('CanvasRGraph4', 0, 1023, 400); // declare widget graphique
			gauge[4].Draw(); // dessine le widget graphique dans le canvas

		   gauge[5] = new RGraph.Gauge('CanvasRGraph5', 0, 1023, 500); // declare widget graphique
			gauge[5].Draw(); // dessine le widget graphique dans le canvas

		   gauge[6] = new RGraph.Gauge('CanvasRGraph6', 0, 1023, 600); // declare widget graphique
			gauge[6].Draw(); // dessine le widget graphique dans le canvas

			textInputRGraph= new Array(); 
			
			textInputRGraph[1]= document.getElementById("valeurRGraph1");
			textInputRGraph[1].value=val;

			textInputRGraph[2]= document.getElementById("valeurRGraph2");
			textInputRGraph[2].value=val;

			textInputRGraph[3]= document.getElementById("valeurRGraph3");
			textInputRGraph[3].value=val;

			textInputRGraph[4]= document.getElementById("valeurRGraph4");
			textInputRGraph[4].value=val;

			textInputRGraph[5]= document.getElementById("valeurRGraph5");
			textInputRGraph[5].value=val;

			textInputRGraph[6]= document.getElementById("valeurRGraph6");
			textInputRGraph[6].value=val;
			
			canvasRGraph=new Array(); 
			canvasRGraph[1] = document.getElementById("CanvasRGraph1");
			canvasRGraph[2] = document.getElementById("CanvasRGraph2");
			canvasRGraph[3] = document.getElementById("CanvasRGraph3");
			canvasRGraph[4] = document.getElementById("CanvasRGraph4");
			canvasRGraph[5] = document.getElementById("CanvasRGraph5");
			canvasRGraph[6] = document.getElementById("CanvasRGraph6");
			
			//canvasRGraph.width = 360;
			//canvasRGraph.height = 300;
			
			contextCanvasRGraph=new Array() ; 
			
			if (canvasRGraph[1].getContext){ // si canvas 1 existe 
				
				for (var i=1; i<=6; i++) {
					contextCanvasRGraph[i] = canvasRGraph[i].getContext("2d");
				}

				setTimeout(function () {requeteAjax(manageReponseAjaxServeur);}, delai); // setTimeOut avec fonction inline : 1er appel de la fonction requete Ajax
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
		function manageReponseAjaxServeur(stringDataIn) { // la fonction recoit en parametre la chaine de texte de la reponse Ajax
			
			// ici la fonction assure actualise le dessin de widget RGraph et autre
			
			valuesString=stringDataIn.split(",") // valeurs separees par ,
			
			var values = new Array(); // declare tableau 
			
			// attention : objet index 1 a 6 et values de 0 a 5
			for (var i=0; i<6; i++) {
				values[i]=Number(valuesString[i]); // recupere chaine dans tableau numerique
				textInputRGraph[i+1].value=values[i]; // met a jour champ
				gauge[i+1].value = values[i];

				//-- si mise a jour directe --
				contextCanvasRGraph[i+1].fillStyle = "rgb(255,255,255)"; // fond canvas
				contextCanvasRGraph[i+1].fillRect (0, 0, canvasRGraph[i+1].width, canvasRGraph[i+1].height);
				gauge[i+1].Draw();

				//-- si mise a jour progressive -- 
				//RGraph.Effects.Gauge.Grow(gauge[i+]);

			} // fin for 
			
			
			
			
			// reinitialise delai rappel requete
			setTimeout(function () {requeteAjax(manageReponseAjaxServeur);}, delai); // relance delai avant nouvelle requete Ajax
			
		} // fin fonction gestion de la reponse Ajax
		
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

    <body>  
      
                       <table>
                                <tr>

                                        <td>
                        <canvas id="CanvasRGraph1" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 1 (0-1023) = </div> <input type="text" id="valeurRGraph1" />               
                                        </td>

                                        <td>
                                        <canvas id="CanvasRGraph2" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 2 (0-1023) = </div> <input type="text" id="valeurRGraph2" />               
                                        </td>

                                        <td>
                                        <canvas id="CanvasRGraph3" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                          <div style="text-align: center">Valeur 3 (0-1023) = </div> <input type="text" id="valeurRGraph3" />               
                                       </td>

                                </tr>

                                <tr>

                                        <td>
                                        <canvas id="CanvasRGraph4" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                          <div style="text-align: center">Valeur 4 (0-1023) = </div> <input type="text" id="valeurRGraph4" />               
                                       </td>

                                        <td>
                                        <canvas id="CanvasRGraph5" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 5 (0-1023) = </div> <input type="text" id="valeurRGraph5" />               
                                        </td>

                                        <td>
                                        <canvas id="CanvasRGraph6" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 6 (0-1023) = </div> <input type="text" id="valeurRGraph6" />               
                                        </td>

                                </tr>


                        </table>


                  <br />

	<br/>
	Serveur Pyduino : Test RGraph x6 avec reponse de requete Ajax 
	<br/>

    </body>

</html>
"""

)  # fin page HTML+JS initiale
	return contenuPageInitialeHTMLJS # la fonction renvoie la page HTML

#===================== Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX
def reponseAJAXServeur():
	
	# definition des variables a uiliser dans la reponse
	global compt
	compt=compt+10
	if compt>1023: compt=0 # RAZ compt
	
	# la reponse 
	reponseAjax=( # debut page reponse AJAX
#"""123, 456, 789""" 
""+str(compt) +","+str(compt) +","+str(compt)  +","+str(compt)  +","+str(compt)  +","+str(compt)
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
