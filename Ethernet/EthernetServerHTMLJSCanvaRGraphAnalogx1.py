#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Serveur TCP generant une page HTML avec code Javascript utilisant un widget graphique RGraph

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
	
	# code a executer avant envoi page 
	value=str(analogRead(A2)) # mesure broche A2
	
	pageHTML=( # debut page HTML 
"""

<!DOCTYPE html >
<html>
        <head>

        <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> <!-- Encodage de la page  -->
		<META HTTP-EQUIV="Refresh" CONTENT="1">
		
                        <script language="javascript" type="text/javascript">
                        <!-- 
                                // code javascript par X. HINAULT - www.mon-club-elec.fr - tous droits reserves - 2013 - GPL v3

                                function path(jsFileNameIn) { // fonction pour fixer chemin absolu                               
                                        var js = document.createElement("script");
                                        js.type = "text/javascript";
                                        js.src = "http://"+window.location.hostname+":80"+"/javascript/rgraph/"+jsFileNameIn; // si utilisation server http local port 80
                                        document.head.appendChild(js);                                   
                                        //alert(js.src); // debug
                                }

                                //---- fichiers a charger ---                            
                                path('RGraph.common.core.js');
                                path('RGraph.gauge.js');                                 

                                window.onload = function () { // fonction executee apres chargement de la page HTML

                                        //--- code graphique ---

                                        // parametres sont : nom du canva, min, max, valeur courante
                                        var gauge = new RGraph.Gauge('nomCanvas', 0, 4095,"""+ value +  """); // declare widget graphique
                                        gauge.Draw(); // dessine le widget graphique dans le canvas

                                } // fin fonction onload 
                                -->      
                        </script>  

                 <title>Test RGraph simple</title>

        </head>

        <body>

        <canvas id="nomCanvas" width="250" height="250">[Canvas non disponible]</canvas>
        <br />
                Test d'affichage d'une mesure analogique dans widget analogique avec aiguille


        </body>
</html>          

"""
)  # fin page HTML
	return pageHTML # la fonction renvoie la page HTML



#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
