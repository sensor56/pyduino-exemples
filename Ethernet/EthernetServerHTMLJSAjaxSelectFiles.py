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
	
	optionsFiles=""
	
	for filename in files:
		print filename
		
		optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
		print optionsFiles
		
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
        
        //--- variables globales ---
        var myselect=null; // objet global
        var mytextarea=null; // objet global 
        
        var delai=1000; // delai auto entre 2 requete Ajax en ms
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
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
			
			//setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // relance delai avant nouvelle requete Ajax
			
		} // fin fonction gestion de la reponse Ajax
		
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

    <body>  
      
		<select  style="width: 300px" id="liste" >
"""
+

optionsFiles

+
"""
		</select>
	
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
	
	# la reponse
	reponseAjax=( # debut page reponse AJAX
	
	filename # renvoie le nom du fichier 
	+"\n"
	+ fileContent  # contenu du fichier
	
)  # fin page reponse AJAX
	return reponseAjax# la fonction renvoie la page HTML
        
#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
