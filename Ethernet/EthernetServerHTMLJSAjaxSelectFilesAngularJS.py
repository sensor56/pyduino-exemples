#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Tester l'envoi d'une requete Ajax, l'envoi d'une reponse et la gestion d'une reponse Ajax avec Angular JS 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
compt=0 # variable de comptage 
ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crée un objet serveur utilisant le port 8080 = port HTTP > 1024

files=None # liste des fichiers

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
	
	print requete # affiche requete recue
	
	# analyse de la requete
	
	#====== si requete ajax ======
	if requete.startswith("GET /ajax"): # si la requete recue est une requete ajax
		
		lignesRequete=requete.splitlines() # recupere la requete est list de lignes
		print lignesRequete[0]  # premiere ligne = la requete utile
		
		params=lignesRequete[0].split('=') # isole la valeur - requete de la forme /ajax=val= donc split "=" isole la valeur
		param=int(params[1]) # 2eme valeur est la valeur recue avec requete ajax
		print param
		
		#--- reponse serveur requete formulaire --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu reponse AJAX
		+
		
		reponseAJAX(param) # voir la fonction separee - pour clarte du code - ici on passe le parametre 
		
				+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "
		#print (bytes(reponse))
		print (reponse) # affiche la reponse envoyee

	#====== si requete GET simple = premiere requete => envoi page HTML+JS initiale ======
	elif requete.startswith("GET"): # si la requete commence par GET seul = premiere page 
		
		print "Requete GETrecue valide"
		
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
		print (reponse) # affiche la reponse envoyee
		
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

#========== fonction fournissant la page HTML + JS initiale incluant code javascript AJAX ======
def pageInitialeHTMLJS():
	
	global files
	
	dirPath=homePath()+"data/text"
	print dirPath
	
	files=listfiles(dirPath)
	print files
	
	# creation chaine forme "Faites votre choix","Choix1", "Choix2", "Choix3", "Choix4", "Choix5"
	
	# ajoute en premier option choisir - indice 0 
	optionsFiles="\"Choisir un fichier\","
	
	for filename in files[:-1]:
		print filename
		
	#optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
		optionsFiles=optionsFiles+" \""+filename+"\","
	
	optionsFiles=optionsFiles+" \""+files[-1]+"\""# dernier sans la ,
		
	print optionsFiles # debug
		
	contenuPageInitialeHTMLJS=( # debut page HTML 
"""
<!DOCTYPE html>
<html ng-app> <!-- Cette page est un code application angularjs --> 

    <head>
        <meta charset="utf-8" />
        <title>Test reponse Ajax</title>
        
		<!-- Insertion lib AngularJS --> 
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/angularjs/1.2.0-rc.2/angular.min.js"></script> 
		
        <!-- Debut du code Javascript  -->
        <script language="javascript" type="text/javascript">
        <!-- 
        
		function mainCtrl($scope, $http){ // fonction controleur principal recevant $scope et $http
		 
			
			//--- liste fichier dans liste deroulante 
			$scope.choixPossibles=["""
			+
			optionsFiles
			+
			"""];   // liste des choix 
			$scope.choixSelect=0; // choix par defaut 
			
			//--- requete Ajax
			
			$scope.dataText="Aucunes donnees"; 
			
			$scope.onChangeSelect=function(){
			
				$http({method: 'GET', url: '/ajax='+$scope.choixSelect+'='}) // definition requete AJAX format GET /ajax=index=
					.success(function(data, status, headers, config) { // gestion reception 
						$scope.dataText=data; 
					})
					.error(function(data, status, headers, config) { // gestion erreur
						$scope.dataText="Probleme";
					});						
			}// fin onChangeSelect
			
		} // fin function mainCtrl 
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

	<body ng-controller="mainCtrl"> <!-- controleur associe au body-->

		<select ng-model="choixSelect" ng-options="choixPossibles.indexOf(choix) as choix for choix in choixPossibles" ng-change="onChangeSelect()"> 
		<!-- ng-options pour sortie par index --!>
		</select>
		<br/>
		
		<textarea id="text" rows="30" cols="100">{{dataText}}</textarea>
	
	</body>

</html>
"""

)  # fin page HTML+JS initiale
	return contenuPageInitialeHTMLJS # la fonction renvoie la page HTML

#===================== Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX
def reponseAJAX(indexIn):
	
	# definition des variables a uiliser dans la reponse
	global files
	
	if indexIn==0:
		return "Sélectionner un fichier" # si choix "Choisir" 
	
	dirPath=homePath()+"data/text/"
	filename=files[indexIn-1] # -1 pour prendre compte option choisir
	filepath=dirPath+filename
	
	print filepath
	
	#-- lecture du fichier -- pour debug
	myFile=open(filepath,'r') # ouverture en lecture
	print ("Contenu du fichier : ")
	myFile.seek(0) # se met au debut du fichier
	fileContent= myFile.read() # lit le fichier
	print fileContent
	
	myFile.close() # fermeture du fichier
	
	# la reponse
	reponseAjax=( # debut page reponse AJAX
	
	#filename # renvoie le nom du fichier 
	#+"\n"
	fileContent  # contenu du fichier
	
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML
        
#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
