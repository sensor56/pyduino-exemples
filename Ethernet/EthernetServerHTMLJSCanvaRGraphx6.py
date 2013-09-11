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
	
	pageHTML=( # debut page HTML 
"""

<!DOCTYPE html >
<html>
        <head>

        <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> <!-- Encodage de la page  -->

                        <script language="javascript" type="text/javascript">
                        <!-- 

                                       // code javascript par X. HINAULT - www.mon-club-elec.fr - tous droits reserves - 2013 - GPL v3

                                function path(jsFileNameIn) { // fonction pour fixer chemin absolu                              
                                        var js = document.createElement("script");
                                        js.type = "text/javascript";
                                        js.src = " http://www.mon-club-elec.fr/mes_javascripts/rgraph/"+jsFileNameIn; // <=== serveur externe - modifier chemin ++ si besoin
                                        //js.src = "http://127.0.0.1/javascript/rgraph/"+jsFileNameIn; // serveur local
                                        //js.src = "javascript/rgraph/"+jsFileNameIn; // chemin local  - fichier doit etre a la racine serveur
                                        document.head.appendChild(js);                                  
                                        //alert(js.src); // debug
                                }

                                //---- fichiers a charger ---                            
                                path('RGraph.common.core.js');
                                path('RGraph.gauge.js');                                

                                window.onload = function () { // fonction executee apres chargement de la page HTML

                                        //--- code graphique ---

                                        // parametres sont : nom du canva, min, max, valeur courante
                                        var gauge1 = new RGraph.Gauge('Canvas1', 0, 1023, 100); // declare widget graphique
                                        gauge1.Draw(); // dessine le widget graphique dans le canvas

                                       var gauge2 = new RGraph.Gauge('Canvas2', 0, 1023, 200); // declare widget graphique
                                        gauge2.Draw(); // dessine le widget graphique dans le canvas

                                       var gauge3 = new RGraph.Gauge('Canvas3', 0, 1023, 300); // declare widget graphique
                                        gauge3.Draw(); // dessine le widget graphique dans le canvas

                                       var gauge4 = new RGraph.Gauge('Canvas4', 0, 1023, 400); // declare widget graphique
                                        gauge4.Draw(); // dessine le widget graphique dans le canvas

                                       var gauge5 = new RGraph.Gauge('Canvas5', 0, 1023, 500); // declare widget graphique
                                        gauge5.Draw(); // dessine le widget graphique dans le canvas

                                       var gauge6 = new RGraph.Gauge('Canvas6', 0, 1023, 600); // declare widget graphique
                                        gauge6.Draw(); // dessine le widget graphique dans le canvas

                                } // fin fonction onload 

                                -->      
                        </script>  

                 <title>Test RGraph simple</title>

        </head>

        <body>

                      <table>
                                <tr>

                                        <td>
                        <canvas id="Canvas1" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 1</div>                
                                        </td>

                                        <td>
                                        <canvas id="Canvas2" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 2</div>
                                        </td>

                                        <td>
                                        <canvas id="Canvas3" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 3</div>
                                        </td>

                                </tr>

                                <tr>

                                        <td>
                                        <canvas id="Canvas4" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 4</div>
                                        </td>

                                        <td>
                                        <canvas id="Canvas5" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 5</div>
                                        </td>

                                        <td>
                                        <canvas id="Canvas6" width="250" height="250">[Canvas non disponible]</canvas>
                         <br />
                         <div style="text-align: center">Valeur 6</div>
                                        </td>

                                </tr>


                        </table>


                  <br />

                  Test simple de 6 afficheurs analogiques avec aiguille

        </body>
</html>          

"""
)  # fin page HTML
	return pageHTML # la fonction renvoie la page HTML



#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
