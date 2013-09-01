#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juillet 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Tester l'envoi d'une requete Ajax, l'envoi d'une reponse et la gestion d'une reponse Ajax

from pyduino import * # importe les fonctions Arduino pour Python

import numpy as np

# entete declarative
compt=0 # variable de comptage 
ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
 
#ipLocale='192.168.1.25' # manuel - attention : utiliser la meme IP qu'une interface reseau du systeme
# pour connaitre les interfaces reseau sur le systeme : utiliser la commande $ ifconfig

print ipLocale # affiche l'adresse IP 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) # crée un objet serveur utilisant le port 8080 = port HTTP > 1024

data=None # Tableau Numpy  global des donnees

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
	
	# code Python a executer avant envoyer page 
	
	# donnees types
	global data
	
	nombreValeurs=10; 
	
	data=np.zeros((nombreValeurs,2)) # tableau de 1000 lignes x 2 colonnes
	data[:,0] = np.arange(0,nombreValeurs,1) # remplissage 1ere colonne = les x

	#data[:,1] = np.arange(0,1000,1) # remplissage 2eme colonne = les y
	data[:,1] = np.random.normal(0,1,size=nombreValeurs)  # remplissage 2eme colonne = les y1 
	
	#dataStr=",".join(data )   # pour convertir list en str avec elements separes par , 
	dataGraph="" # initialise chaine 
	dataStr=str(data.tolist()) # convertit tableau numpy pour affichage dygraph ++
	dataGraph=dataGraph+dataStr 

	# Note : lors envoi page initiale : donnees envoyees au sein code JS
	# lors envoi reponse ajax : donnees envoyees en tant que chaine texte

	# options du graphique Dygraph a utiliser
	optionsGraph="""
	labels: [ "x", "y="], // labels series
	width : 800, // largeur
	// height: 400, // hauteur
	showRangeSelector: true // affiche l'outil de selection plage voulue 
	"""
	
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
			//js.src = " http://www.mon-club-elec.fr/mes_javascripts/dygraphs/"+jsFileNameIn; // <=== serveur externe - modifier chemin ++ si besoin
			//js.src = "http://127.0.0.1/javascript/dygraphs/"+jsFileNameIn; // serveur local
			//js.src = "javascript/rgraph/"+jsFileNameIn; // chemin local  - fichier doit etre a la racine serveur
			js.src = "http://"+window.location.hostname+":80"+"/javascript/dygraphs/"+jsFileNameIn; // si utilisation server http local port 80

			document.head.appendChild(js);                                  
			//alert(js.src); // debug

		} // fin fonction path

		//---- fichiers a charger ---                            
		path('dygraph-combined.js'); // fichier simplifiant acces a tous les fichiers de la librairie dygraph
                             

        // variables / objets globaux
        var textInputDygraphs=null;
        
        var delai=100; // delai en ms entre 2 requetes AJAX
		var val=0;
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
			textInputDygraphs=document.getElementById("valeurDygraphs");
			
			g = new Dygraph( // cree l'objet du graphique

			// containing div
			document.getElementById("graphdiv"), // objet div utilise appele par son nom

			// CSV ou chemin fichier CSV.

			// donnees valides au format x,y1, y2, ..., yn \n
			// x = horodatage ou chiffre
			// horodatages valides : voir http://dygraphs.com/data.html#csv
"""
	+ 
	dataGraph 
	+
""",

			//-- parametres a utiliser pour le graphique
			{
"""
	+ 
	optionsGraph
	+
"""
			} // fin parametres


			); // fin declaration Dygraph
			
			
			setTimeout(function () {requeteAjax(manageReponseAjaxServeur);}, delai); // setTimeOut avec fonction inline : 1er appel de la fonction requete Ajax
			// nb : setTimeout() n'applique delai qu'une fois
			

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
			
			// ici la fonction assure actualise le graphique
			
			
			// met a jour donnees a partir chaine recue
			g.updateOptions( { 'file': stringDataIn } ); // met a jour les donnees du graphique
			
			// recupere derniere valeur
			textInputDygraphs.value=Number(g.getValue(0,g.numColumns()-1) ); // derniere valeur du graphique
			// voir : http://dygraphs.com/jsdoc/symbols/Dygraph.html
			
			// reinitialise delai rappel requete
			setTimeout(function () {requeteAjax(manageReponseAjaxServeur);}, delai); // relance delai avant nouvelle requete Ajax
			
		} // fin fonction gestion de la reponse Ajax
		
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

    <body>  
      
   <div id="graphdiv"></div>
	<br/>
	Valeur courante = <input type="text" id="valeurDygraphs" />
	
	<br/>
	Serveur Pyduino : Test Dygraphs avec reponse de requete Ajax 
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
	global data
	
	# operations sur tableau de donnees
	#data[:,1]=data[:,1]*2
	
	data[:,1]=np.roll(data[:,1],-1)  #fait defiler y 
	
	# envoi du tableau en reponse Ajax
	#dataGraph=""
	#dataStr=str(data.tolist()) # convertit tableau numpy pour affichage dygraph ++
	#dataGraph=dataGraph+dataStr 

	# attention : envoyer une chaine car la fonction JS recoit une chaine : c'est pas du code JS qu'on envoie
	# donnees sous forme d'une chaine
	# format "x,y\n"
	
	dataGraph=""
	
	# attention - ici le formatage est la chaîne brute, pas la chaîne au sein de code JS.. subtil.. !
	for i in range(len(data)-1):
		# format "x,y\n"
		dataGraph=dataGraph+str(data[i,0])+","+str(data[i,1]) + "\n" # le 2eme \n est dans la page HTML, le premier dans la chaine des donnees

	dataGraph=dataGraph+str(data[-1,0])+","+str(data[-1,1]) + "\n" # derniere ligne sans le plus

	print dataGraph
	
	# la reponse 
	reponseAjax=( # debut page reponse AJAX
#"""123, 456, 789""" 
dataGraph
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
