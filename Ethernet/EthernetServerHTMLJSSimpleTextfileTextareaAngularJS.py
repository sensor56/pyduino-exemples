#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Serveur TCP générant une page HTML avec code Javascript simple : ouvrir fichier dans textarea avec Angular JS 

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
	
	# code Python a executer avant envoyer page 
	
	#chemin fichier 
	filename="test.txt" # nom du fichier
	#filename="data_"+today("_",-1)+".txt" # nom du fichier
	filepath=homePath()+dataPath(TEXT)+filename# chemin du fichier
	
	#-- lecture du fichier -- 
	myFile=open(filepath,'r') # ouverture en lecture
	myFile.seek(0) # se met au debut du fichier
	
	linesList=myFile.readlines() # lit le fichier en 1 ligne !! - renvoie list
	
	myFile.close() # fermeture du fichier
	
	# affiche contenu fichier - debug 
	print ("Contenu du fichier : ")
	print linesList # debug
	
	# donnees sous forme d'une chaine pour integration dans pagee HTML
	# format ligne data dans la page HTML "x,y <br\>"
	dataText="\"" # guillemet de debut chaine JS
	
	for dataLine in linesList: # defile lignes 
		dataText=dataText+dataLine.rstrip('\n')+" \\n" # dataLine.rstrip('\n') = enleve \n de la ligne et rajoute avec echappement
	
	dataText=dataText+"\"" # guillemet de fin chaine JS
	
	pageHTML=( # debut page HTML 
"""
<!DOCTYPE HTML> 

<!-- Debut de la page HTML  --> 
<html ng-app> 
	<!-- Debut entete --> 
	<head>    
		<meta charset="utf-8" /> <!-- Encodage de la page  --> 
		<title>JavaScript: Test </title> <!-- Titre de la page --> 
		
		<!-- Insertion lib AngularJS --> 
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/angularjs/1.2.0-rc.2/angular.min.js"></script> 
		
		<!-- Debut du code Javascript  --> 
		<script language="javascript" type="text/javascript"> 
		<!--	
		
					function mainCtrl($scope){ // fonction controleur principal 
					 
							$scope.textData="""
				+
				dataText
				+
							"""; // le contenu de la balise input est accessible comme une variable 
						 
			 
					} // fin function mainCtrl
				

		//--> 
		</script> 
		<!-- Fin du code Javascript --> 

	</head> 
	<!-- Fin entete --> 

	<!-- Debut Corps de page HTML --> 
	<body ng-controller="mainCtrl"> 
	
	Mes donn&eacute;es dans une zone de texte par code Javascript + Angular JS : 
	<br />   
	<textarea id="text" rows="15" cols="50">{{textData}}</textarea> 

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
