from math import sqrt
import tkinter as tk
import sys
import random
import pandas as pd
from itertools import permutations
import time



class Lieu ():
    # Classe de création de lieux entendus comme des points de coordonnées x et y
    def __init__(self, x, y) :
        """Instanciation d'un point avec ses attributs coordonnées"""
        self.x = x
        self.y = y
    
    def calcul_distance(self, point):
        """Calcul de la distance entre le point self et une autre instance de Lieu appelée point."""
        distance = sqrt((self.x-point.x)**2 +(self.y-point.y)**2)
        return distance


class Route ():
    def __init__(self, ordre, matrice):
        """Instanciation d'une route, ordre est une liste de points (objets Lieu)"""
        self.ordre = ordre
        self.distance = 0
        self.verification_formatage(ordre)
        self.calcul_distance_route(matrice)

    def __repr__(self):
        return self.__dict__

    def verification_formatage(self,ordre):
        """Vérification du bon formatage de la liste ordre passée au init de Route"""
        if ordre[0] != 0:
            raise ValueError ("Le lieu d'index zéro doit être présent en première et en dernière position dans l'ordre.")
        elif ordre[-1] != 0:
            raise ValueError ("Le lieu d'index zéro doit être présent en première et en dernière position dans l'ordre.")
        else :
            set_ordre = set(ordre[1:-1]) # On compare la liste débarassée des zéro à son équivalent en set
            if len(set_ordre) != len(ordre[1:-1]): # Si le set est plus petit, ça veut dire qu'il y a des doublons dans la liste
                raise ValueError ("La liste ordre ne doit pas présenter d'indices en double à part le départ et l'arrivée à 0.")
        
    def calcul_distance_route(self, matrice):
        """Chercher les distances dans la matrice origine-destination"""
        distances = [] # toutes nos distances pour la route
        distance_route = 0 # la distance totale pour la route
        for point1, point2 in zip(self.ordre, self.ordre[1:]):
            distances.append(matrice.loc[point1,point2])
        distance_route = sum(distances)
        self.distance = distance_route

class Graph ():

    

    def __init__(self, largeur, hauteur, nombre) :
        self.largeur= largeur
        self.hauteur = hauteur
        self.nombre = nombre
        self.liste_lieux = []
        #on appelle la fonction qui génère une liste d elieux, et permet de remplir la liste
        self.listelieux()
        self.matricedesdistances= []
        self.calcul_matrice_cout_od()
    


    #création aléatoire des  liste de lieux
    def listelieux(self ) : 

        
        for i in range(self.nombre+1):
            x = random.randint(0,self.largeur)
            y = random.randint(0,self.hauteur)
            
            lieu = Lieu(x,y)

            self.liste_lieux.append(lieu)


            print(x,y)



    # calculer une matrice de distances entre chaque lieu du graphe et stocker ce résultat dans une variable de classe matrice_od.
    def calcul_matrice_cout_od(self):
        for i in range (len(self.liste_lieux)):
            listedesdistances=[]          
            for e in range (len(self.liste_lieux)):
                d=self.liste_lieux[i].calcul_distance(self.liste_lieux[e])
                listedesdistances.append(d)
            self.matricedesdistances.append(listedesdistances)
        #transformer les listes en tableau panda   
        self.matricedesdistances = pd.DataFrame(self.matricedesdistances)
        self.plus_proche_voisin()

    





    #Le graph disposera également d'une fonction nommée plus_proche_voisin permettant de renvoyer le plus proche voisin d'un lieu en utilisant la matrice de distance
    def plus_proche_voisin(self):
        self.matricedesdistances["indexmin"]=self.matricedesdistances[self.matricedesdistances>0].idxmin(axis=1)

    #sauvergarder le fichier
    def sauvergarder_graph(self):
        listex = []
        listey = []
        for lieu in self.liste_lieux:
            listex.append(lieu.x)
            listey.append(lieu.y)
        pd.DataFrame([listex, listey]).to_csv("graph.csv")
        
    #charger le csv
    def charger_graph(self, path):
        data = pd.read_csv(path)
        x=data.loc[:,0]
        y=data.loc[:,-1]
        nouveauxpoints = []
        for x0, y0 in zip(x,y):
            nouveauxpoints.append(Lieu(x0, y0))
        self.liste_lieux = nouveauxpoints
        #mettre à jour la matrice coût od
        self.calcul_matrice_cout_od()



class Affichage(tk.Tk):

    """Instanciation de la classe d'affichage"""
    def __init__(self,width, height,graph,nb_lieu):
        
        tk.Tk.__init__(self)
        self.geometry(f"{width}x{height+50}")
        self.configure(bg='#DCDCDC')
        self.nb_lieu=nb_lieu
        self.width=width
        self.height=height
        self.graph=graph
        self.routes=0
        self.create_widget()
        self.bind("<KeyPress-n>", self.on_key_press)
        self.bind('<Escape>', self.close)
        self.text=tk.StringVar()



        self.label=tk.Label(self,textvariable=self.text,bg='#DCDCDC')
        self.label.pack()

    def create_widget(self):
        
        """Création du canvas"""
        self.canvas=tk.Canvas(self,width=self.width,height=self.height)
        
        for i in range(len(self.graph.liste_lieux)) :
            x0=self.graph.liste_lieux[i].x
            y0=self.graph.liste_lieux[i].y
            self.canvas.create_oval(x0-10,y0-10,x0+10,y0+10)
            self.canvas.create_text(x0,y0,text=str(i))
        
        self.canvas.pack()

    def create_route(self):
        """Affichage des differentes routes possibles"""
        
        liste=[]


        for i in range(self.nb_lieu+1):
            liste.append(i)
        print(liste)
        i =0
        for itineraire in (BruteForce().creer_itineraires(liste)):
            itineraire=list(itineraire)
            self.routes=i
            route=Route(itineraire,graph.matricedesdistances)

            if i==0:
                meilleure_route=route
            elif route.distance<meilleure_route.distance:
                meilleure_route=route

            liste_coord=[]
            for index in route.ordre:
                liste_coord.append(self.graph.liste_lieux[index].x)
                liste_coord.append(self.graph.liste_lieux[index].y)
                


            if route==meilleure_route and i==0:
                blue_line=self.canvas.create_line(liste_coord,fill = "blue")
                find=i
                
            elif route==meilleure_route and i!=0:
                self.canvas.delete(blue_line)

                blue_line=self.canvas.create_line(liste_coord,fill = "blue")
                find=i

            else :
                line = self.canvas.create_line(liste_coord,dash = (5, 2))
                self.canvas.after(1,self.canvas.delete,line)

            self.text.set(f"Nous avons obtenue une distance de {meilleure_route.distance} en {find}/{self.routes} itérations.")
            self.update()
            i+=1
        
        nb=0
        for index in meilleure_route.ordre:
            self.canvas.create_text(self.graph.liste_lieux[index].x,self.graph.liste_lieux[index].y-15,text=str(nb))
            nb+=1
        self.update()

    
    def on_key_press(self,event):

        """ Fonction a implementer lorsque l'on aura les valeur itératives"""
        print('coucou')
        self.create_route()
        

    
    def close(self,event):

        """Fonction qui quitte le programme lorsque l'on appuie sur la touche échap"""
        self.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing




class BruteForce():
        
    def creer_itineraires(self, liste_lieux):
        liste_lieux= liste_lieux.copy()
        depart = liste_lieux.pop(0)
        
        for itineraire in permutations(liste_lieux):
            itineraire = list(itineraire)
            itineraire.append(0)
            itineraire.insert(0,0)

            yield itineraire



NB_LIEU=5
SIZE=800
graph=Graph(SIZE,SIZE,NB_LIEU)
app=Affichage(SIZE,SIZE,graph,NB_LIEU)
<<<<<<< HEAD
app.mainloop()
=======
app.mainloop()
>>>>>>> 337ae1b5e01bd955c09647e8781b9914d6210f1a
