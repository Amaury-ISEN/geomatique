from math import sqrt
import tkinter as tk
import sys
import random
import pandas as pd




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
        for i in range(self.nombre):
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
        self.matricedesdistances = pd.DataFrame(self.matricedesdistances)





    #Le graph disposera également d'une fonction nommée plus_proche_voisin permettant de renvoyer le plus proche voisin d'un lieu en utilisant la matrice de distance
    #def plus_proche_voisin(self):



class Affichage(tk.Tk):

    """Instanciation de la classe d'affichage"""
    def __init__(self,width, height,graph,routes):
        
        tk.Tk.__init__(self)
        self.geometry("1024x720")
        self.configure(bg='#DCDCDC')
        self.width=width
        self.height=height
        self.graph=graph
        self.routes=routes

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
        
        i=0
        for route in self.routes:
            liste_coord=[]
            for index in route.ordre:
                liste_coord.append(self.graph.liste_lieux[index].x)
                liste_coord.append(self.graph.liste_lieux[index].y)
            if i==0:
                self.canvas.create_line(liste_coord,fill = "red")
            else :
                self.canvas.create_line(liste_coord,dash = (5, 2))
            i=i+1

        




    def on_key_press(self,event):

        """ Fonction a implementer lorsque l'on aura les valeur itératives"""
        print('coucou')

        self.text.set(f"Nous avons obtenue une distance de {self.routes[0].distance} en {len(self.routes)} itérations.")
        self.create_route()

    
    def close(self,event):

        """Fonction qui quitte le programme lorsque l'on appuie sur la touche échap"""
        self.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing





graph=Graph(600,600,10)

app=Affichage(600,600,graph,[Route([0,1,2,3,4,5,6,7,8,9,0],graph.matricedesdistances),Route([0,1,3,2,4,5,7,6,8,9,0],graph.matricedesdistances)])
app.mainloop()