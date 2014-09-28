#Scanner de port TCP simple par Daniel Roger 28/09/2014
#Le programme pourrait être optimisé en ajoutant des fonctions 

import socket
import sys
from datetime import datetime
import time
import os

def restart(): # Méthode pour redémarrer le script (appelée en cas d'erreur)
    restart = sys.executable 
    os.execl(restart, restart, * sys.argv)


while True:
    
    ipaddr = str(input("Entrez une adresse ip ou un nom : "))

    try:
        ipfromdns = socket.gethostbyname(ipaddr)
    except socket.gaierror:   #Si le nom entré est incorrect
        print("Le nom est incorrect")
        restart()
  
    port = str(input("Entrez le(s) port(s) à tester séparés par une virgule ou un rang par un tiret:\n"))
    

    #------------------------------------------------------REMARQUES---------------------------------------------------------------------------------------------

    # Note à propos de la méthode 'connect_ex':
    # Cette méthode retourne une exception, si le port est ouvert, il n'y aura pas d'exception (résultat = 0).
    # Dans le cas contraire, le résultat sera 1.

    # Les socket sont toujours initilisées en début de boucles car elles sont fermées (sock.close()) si le port est ouvert, il faut donc en initialiser une autre.
    # Le délai maximum de connexion est de 3 secondes. Si cela est trop court, changez sock.settimeout(3) par une autre valeur. 

    #------------------------------------------------------------------------------------------------------------------------------------------------------------


    try:
  
        if(","in port): #Si l'on souhaite scanner plusieurs ports séparés par une virgule
            ports = port.split(',')
            for i in range(len(ports)): #Récupération du nombre de port à scanner puis boucle
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(3)
                portscan = int(ports[i]) #Les ports sont des string,conversion en int
                resultat = sock.connect_ex((ipfromdns,portscan))
                if(resultat == 0):
                    print("Port ",portscan," ouvert")
                    
                else:
                    print("Port ",portscan," fermé")
            sock.close()

         
        elif("-" in port): #Scan d'un rang de port
            a = port.split("-")  # Permet de supprimer le caractère '-' et assigner les valeurs avant et après ce caractère dans un tableau
            rang1 = int(a[0])    # La variable rang1 récupére la première valeur du tableau (celle à gauche de '-') puis est convertie en int.
            rang2 = int(a[1])    # La variable rang2 récupére la seconde valeur du tableau (celle à droite de '-') puis est convertie en int.

            for portlist in range(rang1,rang2+1):
                
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(3)
                resultat = sock.connect_ex((ipfromdns,portlist))
                
                if(resultat == 0):
                    print("Port ",portlist," ouvert")
                    sock.close()
                else:
                    print("Port ",portlist," fermé")
                    
        else:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(3)
            resultat = sock.connect_ex((ipfromdns,int(port)))
            
            
            if(resultat == 0):
                    print("Port ",port," ouvert")
                    sock.close()
            else:
                    print("Port ",port," fermé")


        print("\nLe scan est terminé - ", datetime.now(),"\n")
    
    except socket.error:
        print("Impossible de se connecter à l'hôte")
        restart()
    

