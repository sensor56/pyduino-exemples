#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Aout 2013- Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Creer un fichier de donnees horodatees de duree voulue avec enregistrement auto

from pyduino import * # importe les fonctions Arduino pour Python
import datetime # pour operations facilitees sur date/heure

# entete declarative
noLoop=True

filepath=""
filename=""
today0=""

compt=0
refTime=None
intervalle=1 # intervalle en sec entre 2 mesures
nombreMesures=1000 # nombre de mesures

# duree = intervalle x (nombreMesure-1)

#--- setup --- 
def setup():
	
	global filepath, filename, today0, refTime
	
	myDataPath=("data/text/")
	
	today0=today() # memorise jour courant 
	
	path=homePath()+myDataPath  # chemin du répertoire à utiliser
	filename="data"+today0+".txt" # nom du fichier
	filepath=path+filename # chemin du fichier
	
	print filepath
	
	# creation fichier au besoin 
	if exists(filepath):
		print "Le fichier existe"
	else :
		print "Le fichier n'existe pas : creation du fichier"
		myFile=open(filepath,'w') # création du fichier
		myFile.close()
		
	# memorise temps de reference
	refTime=datetime.datetime(int(year()), int(month()), int(day())) # date a utiliser - heure 00:00:00 si pas precise
	print refTime

	loop() # premier appel loop
	
	# NB : on peut aussi ouvrir le fichier dans l'editeur pour verifier son contenu 
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global filepath, filename, today0, refTime, compt
	
	myFile=open(filepath,'a') # ouverture pour ajout de texte
	#myFile=open(filepath,'w') # ouverture pour ecriture avec effacement contenu
	
	#-- ajout de chaines au fichier 

	#for t in range(1440) : # defile 1440 minutes theoriques
	dataValue=str(random(0,1023)) # genere une valeur aleatoire entiere
	
	#dataTime=refTime+datetime.timedelta(0, t*60) # jours, secondes - ici toutes les minutes
	dataTime=refTime+datetime.timedelta(0, compt*intervalle) # jours, secondes - ici toutes les minutes
	#dataTime=datetime.timedelta(0, t*60) # jours, secondes - ici toutes les minutes - sans refTime
	
	#print dataTime
	
	# format de donnees utilise : JJ/MM/YYYY hh:mm:ss , val \n
	#dataLine=today('/') + " " + hh +":"+mm + ":" + str(t)+","+dataValue+"\n"
	dataLine=str(dataTime)+","+dataValue+"\n" # format datetime JJ-MM-AAAA hh:mm:ss
	print dataLine # debug
	myFile.write(dataLine) # ecrit la ligne dans le fichier
	
	myFile.close() # fermeture du fichier en ecriture
	
	"""
	#-- lecture du fichier -- pour debug
	myFile=open(filepath,'r') # ouverture en lecture
	print ("Contenu du fichier : ")
	myFile.seek(0) # se met au debut du fichier
	print myFile.read() # lit le fichier
	
	myFile.close() # fermeture du fichier
	"""
	
	# auto rappel de loop
	compt=compt+1 # incrémente compteur
	if compt>nombreMesures: exit() # stop si assez de mesure 
	
	timer(intervalle*1000, loop) # auto appel de loop toutes les secondes
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
