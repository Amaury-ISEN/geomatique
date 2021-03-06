from math import sqrt
import tkinter as tk
import sys
import random
import pandas as pd
import numpy as np 
from itertools import permutations
import time
from pyproj import Proj, transform
from sklearn.preprocessing import Normalizer

random.seed(42)

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
        # Si la liste n'a pas la même longueur qu'une liste recrée via son max, alors il manque un indice :
        elif len(ordre[1:-1]) != len([i for i in range(1,max(ordre[1:-1])+1)]):
            raise ValueError ("Il manque une valeur de la liste dans ordre.")
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

    def __init__(self, largeur, hauteur, nombre, **kwargs) :
        self.largeur= largeur
        self.hauteur = hauteur
        self.nombre = nombre
        self.liste_lieux = []

        # Si un chemin vers un csv pour les points est renseigné lors de l'instanciation du graphe :
        if "path_points" in kwargs :
            self.path_points = kwargs["path_points"]
            self.load_points()

            # Si un chemin vers un csv pour ma matrice OD est renseigné lors de l'instanciation du graphe :
            if "path_matrice" in kwargs :
                self.path_matrice = kwargs["path_matrice"]
                self.load_matrice()

            # Si pas de chemin vers matrice, on la calcule :
            else :
                self.matricedesdistances= []
                self.calcul_matrice_cout_od()

        else : # Si pas de points ni de matrice en csv, les générer ici :
            #on appelle la fonction qui génère une liste d elieux, et permet de remplir la liste
            self.liste_lieux_rand()
            self.matricedesdistances= []    
            self.calcul_matrice_cout_od()

    def load_points(self):
        """Charge les points de coordonnées GPS depuis le chemin csv renseigné lors de la construction du graphe."""
        df_points = pd.read_csv(self.path_points, sep=",")


        # enlever min et / par max
        df_points["latitude"] = (df_points["latitude"]-df_points["latitude"].min())/self.hauteur
        df_points["longitude"] = (df_points["longitude"]-df_points["longitude"].min())/self.largeur
        print("scaled points", df_points[["latitude", "longitude"]])
        # print("self.hauteur", self.hauteur)
        # print("self.largeur", self.largeur)

        # df_points["latitude"] *= 10
        # df_points["longitude"] *= 10

        
        # normalizer = Normalizer()
        # df_points[["latitude"]] = normalizer.fit_transform(df_points[["latitude"]])
        # df_points[["longitude"]] = normalizer.fit_transform(df_points[["longitude"]])


        print("scaled points", df_points[["latitude", "longitude"]])
        for i in range(len(df_points)-1):
            x = df_points["latitude"][i]
            y = df_points["longitude"][i]
            lieu = Lieu(x,y)
            self.liste_lieux.append(lieu)

        # print(x,y)

    def load_matrice(self):
        """Charge une matrice OD à l'aide du chemin vers le csv renseigné lors de la construction du graphe."""
        self.matricedesdistances= []
        self.calcul_matrice_cout_od()

        for i in range (len(self.liste_lieux)):
            listedesdistances=[]          
            for e in range (len(self.liste_lieux)):
                d=self.liste_lieux[i].calcul_distance(self.liste_lieux[e])
                listedesdistances.append(d)
            self.matricedesdistances.append(listedesdistances)
        #transformer les listes en tableau panda   
        self.matricedesdistances = pd.DataFrame(self.matricedesdistances)


    #création aléatoire des  liste de lieux
    def liste_lieux_rand(self):

        for i in range(self.nombre+1):
            x = random.randint(0,self.largeur)
            y = random.randint(0,self.hauteur)      
            lieu = Lieu(x,y)
            self.liste_lieux.append(lieu)
            print(x,y)

    # def liste_lieux_reels(self, path) :




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

    def afficher_recuit(self):
        """fonction pour afficher le recuit"""
        tsp=TSP_SA(1400,10000,self.graph.matricedesdistances,self.nb_lieu)
        i=0
        for tour,temperature,route_2,best_route,nb in tsp.recuit():

            liste_coord=[]
            if i==0:
                for index in best_route.ordre:
                    liste_coord.append(self.graph.liste_lieux[index].x)
                    liste_coord.append(self.graph.liste_lieux[index].y)
                blue_line=self.canvas.create_line(liste_coord,fill = "blue")

            meilleure_route=best_route
            
            liste_coord=[]
            for index in route_2.ordre:
                liste_coord.append(self.graph.liste_lieux[index].x)
                liste_coord.append(self.graph.liste_lieux[index].y)
                
         
            if route_2==best_route and i!=0:
                self.canvas.delete(blue_line)
                blue_line=self.canvas.create_line(liste_coord,fill = "blue")
         

            else :
                line = self.canvas.create_line(liste_coord,dash = (5, 2))
                self.canvas.after(1,self.canvas.delete,line)
    

            self.text.set(f" distance: {meilleure_route.distance} en {nb}/{tour} itérations. temp:{int(temperature)}")
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
        #self.create_route()
        self.afficher_recuit()
        

    
    def close(self,event):

        """Fonction qui quitte le programme lorsque l'on appuie sur la touche échap"""
        self.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing



class TSP_SA():

    
    def __init__ (self, temperature, nb_iterations,matrice,nb_lieu):
        self.matrice = matrice
        self.temperature = temperature
        self.nb_iterations = nb_iterations
        self.nb_lieu=nb_lieu
        self.ordre=self.init_ordre()


        
        # Création d'une route aléatoire en attendant mieux avec le PPV :
        self.best_route = Route(self.chemin_plus_proche_voisins(),self.matrice)
        self.route_1 = Route(self.chemin_plus_proche_voisins(),self.matrice)
        self.route_2 = Route(self.chemin_plus_proche_voisins(),self.matrice)
        self.tour = 0
        self.delta = 0
        self.proba_acceptation = None

    def chemin_plus_proche_voisins(self):
        ordre=[0]
        dataframe=self.matrice.copy()
        dataframe.drop(0, axis=1, inplace=True)
        for i in range(len(dataframe.columns)-2):
            liste_drop=['indexmin']
            route =(dataframe["indexmin"][ordre[-1]])
            ordre.append(int(route))
            liste_drop.append(int(ordre[-1]))
            dataframe.drop(liste_drop, axis=1, inplace=True)
            dataframe["indexmin"]=dataframe[dataframe>0].idxmin(axis=1)

        ordre.append(int(dataframe["indexmin"][ordre[-1]]))
        ordre.append(0)
        print(ordre)
        return ordre

    
    def recuit(self):
        initial_temperature=self.temperature
        listetemp=[]
        nb_best_route=0
        for i in range(self.nb_iterations):

            self.permutation()

        
    
            # Calcul du delta de la fonction coût (ici distance totale) entre la route précédente et la nouvelle :
            self.delta = self.route_2.distance-self.route_1.distance
            
            if self.delta < 0:
                # On a un delta négatif, on conserve donc cette nouvelle route meilleure que la précédente.
                self.route_1 = self.route_2
                if self.route_2.distance < self.best_route.distance:
                    # Cette nouvelle route est meilleure que la meilleure jusqu'ici, on écrase cette dernière avec :
                    self.best_route = self.route_2
                    nb_best_route=i

                    
            if self.delta > 0:
                # On a un delta positif, on va conserver ou non cette nouvelle route selon la proba d'acceptation
                self.proba_acceptation = np.exp(-self.delta/self.temperature)
                
                if random.random() < self.proba_acceptation :
                    # Le test de probabilité a été passé, on conserve la nouvelle route malgré tout
                    self.route_1 = self.route_2
                    print("accepted")
                
            self.tour += 1

            self.temperature = self.temperature * 0.999
            listetemp.append(self.temperature)
            yield self.tour,self.temperature,self.route_2,self.best_route,nb_best_route
        
        print(listetemp)


    def permutation(self):

        ordre=self.route_2.ordre
        a=random.randrange(1,len(ordre)-3)
        b=a+3
        ordre[a:b]=list(reversed(ordre[a:b]))
        self.route_2=Route(ordre,self.matrice)

    def init_ordre(self):
        ordre=[]
        for i in range(self.nb_lieu+1):
            ordre.append(i)
        ordre.append(0)
        return ordre
        
class BruteForce():
        
    def creer_itineraires(self, liste_lieux):
        liste_lieux= liste_lieux.copy()
        depart = liste_lieux.pop(0)
        
        for itineraire in permutations(liste_lieux):
            itineraire = list(itineraire)
            itineraire.append(0)
            itineraire.insert(0,0)

            yield itineraire



NB_LIEU=50
SIZE=1000
# graph=Graph(SIZE,SIZE,NB_LIEU)
graph=Graph(SIZE,SIZE,nombre = 16,
            path_points="liste_points_gps.csv",
            path_matrice="matrice_od.csv")

# app=Affichage(SIZE,SIZE,graph,NB_LIEU)
app=Affichage(SIZE,SIZE,graph, graph.nombre)

app.mainloop()
