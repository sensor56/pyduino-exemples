#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Serveur TCP générant une page HTML affichant une liste déroulante listant les fichiers d'un repertoire

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
	#print (reponse) # affiche la reponse envoyee
	
	#serverHTTP.close()
	# remarque : le socket = serveur doit rester ouvert
	
	# quand on quitte l'application: la connexion TCP reste active un peu donc erreur si re-execution trop rapide du code
	# on peut utiliser un port voisin dans ce cas... 

	delay(10) # entre 2 loop()
	
# -- fin loop --

#--- fonction fournissant la page HTML --- 
def pageHTML():
	
	dirPath=homePath()+"data/text"
	print dirPath
	
	files=listfiles(dirPath)
	print files
	
	optionsFiles=""
	
	for filename in files:
		print filename
		
		optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
		print optionsFiles
	
	pageHTML=( # debut page HTML 
"""
<!DOCTYPE HTML> 

<!-- Debut de la page HTML  --> 
<html> 
	<!-- Debut entete --> 
	<head>    
		<meta charset="utf-8" /> <!-- Encodage de la page  --> 
		<title>JavaScript: Test </title> <!-- Titre de la page --> 

		<!-- Debut du code Javascript  --> 
		<script language="javascript" type="text/javascript"> 
		<!--	

                        // code Javascript

                        //--- variables globales ---
                        var myselect=null; // objet global

                        //--- fonction appelee au chargement de la page
                         window.onload = function () { // au chargement de la page        

                                        // code Javascript ici, avec sa syntaxe specifique...

                                        print("Javascript OK")

                                        myselect=document.getElementById("liste")

                                        for (var i=0; i<myselect.options.length; i++){

                                                        print("Option index "+i + ":" + myselect.options[i].text + " (" + myselect.options[i].value + ")") // affiche la liste des options

                                        } // fin for                  

            // fonction de gestion d'un changement select - ici placee dans le code JS initial
                                myselect.onchange=function () {

                                        var index=this.selectedIndex
                                        print ("Index courant ="+index + " soit : " + this.options[index].text); // this represent myselect

                                } // fin fonction onchangeSelect

           } // fin onload

                                //---- fonctions utiles ---

                                function print(textIn) { // fonction pour ajouter un element a la page - utile ++ pour debug

                         // Ajouter un element a la page sans effacer le reste
                                        //var txt = 'Hello';

                                        var txt=textIn;

                                        var newtext = document.createTextNode(txt);
                                        document.body.appendChild(newtext);

                                        document.body.appendChild(document.createElement("br")); // ajoute saut de ligne

                                        document.body.appendChild(newtext);  

                                } // fin print

		//--> 
		</script> 
		<!-- Fin du code Javascript --> 

	</head> 
	<!-- Fin entete --> 

	<!-- Debut Corps de page HTML --> 
	<body > 
	
		<select  style="width: 300px" id="liste" >
"""
+

optionsFiles

+
"""
		</select>

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
