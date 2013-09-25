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
	
	# code Python a executer avant envoyer page 
	
	#chemin fichier initial - celui du jour voir aucun 
	
	myDataPath=("data/text/")
	
	path=homePath()+myDataPath  # chemin du répertoire à utiliser
	#filename="testdata.txt" # nom du fichier
	filename="data"+today("_",-1)+".txt" # nom du fichier du jour 
	filepath=path+filename # chemin du fichier
	
	#-- lecture du fichier -- 
	myFile=open(filepath,'r') # ouverture en lecture
	print ("Contenu du fichier : ")
	myFile.seek(0) # se met au debut du fichier
	
	linesList=myFile.readlines() # lit le fichier - renvoie list
	
	myFile.close() # fermeture du fichier

	print linesList
	
	# donnees sous forme d'une chaine
	# format ligne data dans la page HTML "x,y\n"
	dataGraph=""
	
	for dataLine in linesList[:-1]: # defile lignes sauf la derniere
		dataGraph=dataGraph+"\""+dataLine.rstrip('\n')+" \\n \" +" + "\n" # dataLine.rstrip('\n') = enleve \n de la ligne
	
	dataGraph=dataGraph+"\""+linesList[-1].rstrip('\n')+" \\n \" " # derniere ligne sans le +

	# Note : lors envoi page initiale : donnees envoyees au sein code JS
	# lors envoi reponse ajax : donnees envoyees en tant que chaine texte

	 # l'envoi initial d'un tableau de valeurs permet de fixer la largeur du graphique
	
	
	# chargement de la liste des fichiers dans la liste déroulante 
	
	global files
	
	dirPath=homePath()+"data/text"
	print dirPath
	
	files=listfiles(dirPath)
	print files
	
	optionsFiles=""
	
	for filename in files:
		print filename
		
		optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
		print optionsFiles
		
	# options du graphique Dygraph a utiliser
	optionsGraph="""
	labels: [ "x", "y="], // labels series
	//width : 800, // largeur
	// height: 400, // hauteur
	//valueRange: [0,4095], // plage valeurs Y
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
		
        //--- variables globales ---
        var myselect=null; // objet global
        var mytextarea=null; // objet global 
        
        var textInputDygraphs=null; // objet global 
        
        //var delai=1000; // delai en ms entre 2 requetes AJAX - pas utilise ici 
		var val=0;
        
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
        
			// dygraphs 
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
			
			// liste deroulante 
			
			myselect=document.getElementById("liste");
			mytextarea=document.getElementById("text");
			
			mytextarea.value="Selectionner un fichier"; 
			
			for (var i=0; i<myselect.options.length; i++){

				//println("Option index "+i + ":" + myselect.options[i].text + " (" + myselect.options[i].value + ")") // affiche la liste des options - debug

			} // fin for                  

            // fonction de gestion d'un changement select - ici placee dans le code JS initial
			myselect.onchange=function () {

				var index=this.selectedIndex
				//println ("Index courant ="+index + " soit : " + this.options[index].text); // this represent myselect - debug
				
				requeteAjax(index,manageReponseAjax);
				//println("Envoi requete Ajax"); - debug
				
				} // fin fonction onchangeSelect
        
        
            //setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // setTimeOut avec fonction inline : 1er appel de la fonction requete Ajax
            // nb : setTimeout() n'applique delai qu'une fois
        } // fin onload
        
        //---- fonctions utiles ---

         function println(textIn) { // fonction pour ajouter un element a la page - utile ++ pour debug

        // Ajouter un element a la page sans effacer le reste
        //var txt = 'Hello';

                                        var txt=textIn;

                                        var newtext = document.createTextNode(txt);
                                        document.body.appendChild(newtext);

                                        document.body.appendChild(document.createElement("br")); // ajoute saut de ligne

                                        document.body.appendChild(newtext);  

                                } // fin println
                                
        //---------- fonction de requete AJAX -----
        function requeteAjax(chaineIn, callback) { // la fonction recoit en parametre la fonction de callback qui gere la reponse Ajax
			// la fonction de callback appelee sera celle definie dans setTimeOut : manageAjaxData
			var xhr = XMLHttpRequest(); // declare objet de requete AJAX  - OK Firefox
			
			xhr.open("GET", "/ajax="+chaineIn+"=", true); // definition de la requete envoyee au serveur ici : GET /ajax
			xhr.send(null); // envoi de la requete
			
			xhr.onreadystatechange = function() { // fonction de gestion de l'evenement onreadystatechange
				if (xhr.readyState == 4 && xhr.status == 200) { // si reponse OK
					callback(xhr.responseText); // appel fonction gestion reponse en passant texte reponse en parametre
				} // fin if 
			}; // fin function onreadystatechange
			
		} // fin fonction requeteAjax
		
		//------ fonction qui sera utilisee en fonction de callback = gestion de la reponse Ajax
		function manageReponseAjax(stringDataIn) { // la fonction recoit en parametre la chaine de texte de la reponse Ajax
			
			
			//println (stringDataIn) // debug
			
			mytextarea.value=stringDataIn; // affiche le contenu du fichier dans le champ
			
			// ici la fonction assure actualise le graphique
			
			
			// met a jour donnees a partir chaine recue
			g.updateOptions( { 'file': stringDataIn } ); // met a jour les donnees du graphique
			
			// recupere derniere valeur
			textInputDygraphs.value=Number(g.getValue(0,g.numColumns()-1) ); // derniere valeur du graphique
			// voir : http://dygraphs.com/jsdoc/symbols/Dygraph.html
			
			//setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // relance delai avant nouvelle requete Ajax
			
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
	
	
		<select  style="width: 300px" id="liste" >
"""
+

optionsFiles

+
"""
		</select>
		
		<br/>
	
	<textarea id="text" rows="30" cols="100"></textarea>
	
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
	
	dirPath=homePath()+"data/text/"
	filename=files[indexIn]
	filepath=dirPath+filename
	
	print filepath
	
	#-- lecture du fichier -- pour debug
	myFile=open(filepath,'r') # ouverture en lecture
	print ("Contenu du fichier : ")
	myFile.seek(0) # se met au debut du fichier
	fileContent= myFile.read() # lit le fichier
	print fileContent
	
	myFile.close() # fermeture du fichier
	
	# attention - ici le formatage est la chaîne brute, pas la chaîne au sein de code JS.. subtil.. !
	# donc en fait ici, on peut envoyer le contenu du fichier as is
	
	# la reponse
	reponseAjax=( # debut page reponse AJAX
	
	#filename # renvoie le nom du fichier 
	#+"\n"
	#+ 
	fileContent  # contenu du fichier
	
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML
        
#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
