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
    def __init__(self, ordre):
        """Instanciation d'une route, ordre est une liste de points (objets Lieu)"""
        self.ordre = ordre        
    
    def calcul_distance_route(self):
        """Calcul de la distance totale entre les points d'une route"""
        distances = [] # distances entre les points deux à deux
        distance_route = 0 # distance totale
        # On itère sur un zip de la liste ordre et de sa soeur décalée de 1 élément.
        # zip() crée liste de tuples avec les points deux à deux [(point1,point2), ...] 
        for point1, point2 in zip(self.ordre, self.ordre[1:]):
            # ajout des distances entre les points deux à deux
            distances.append(point1.calcul_distance(point2))
        distance_route = sum(distances) # somme de toutes les distances pour avoir le total
        return distance_route


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
        self.width=width
        self.height=height
        self.graph=graph
        self.routes=routes

        self.create_widget()
        self.bind("<KeyPress-n>", self.on_key_press)
        self.bind('<Escape>', self.close)


        self.text=tk.StringVar()
        self.text.set("coucou")


        self.label=tk.Label(self,textvariable=self.text)
        self.label.pack()

    def create_widget(self):
        
        """Création du canvas"""
        self.canvas=tk.Canvas(self,width=self.width,height=self.height,bg='#DCDCDC')
        
        for i in range(len(self.graph.liste_lieux)) :
            x0=self.graph.liste_lieux[i].x
            y0=self.graph.liste_lieux[i].y
            self.canvas.create_oval(x0-10,y0-10,x0+10,y0+10)
            self.canvas.create_text(x0,y0,text=str(i))
        
        self.canvas.pack()

    def create_route(self):
        """Affichage des differentes routes possibles"""
        liste_coord=[]
        for route in self.routes:
            for index in route.ordre:
                liste_coord.append(self.graph.liste_lieux[index].x)
                liste_coord.append(self.graph.liste_lieux[index].y)

            self.canvas.create_line(liste_coord,dash = (5, 2))




    def on_key_press(self,event):

        """ Fonction a implementer lorsque l'on aura les valeur itératives"""
        print('coucou')

        self.text.set("Ca fonctionne")
        self.create_route()

    
    def close(self,event):

        """Fonction qui quitte le programme lorsque l'on appuie sur la touche échap"""
        self.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing




app=Affichage(400,400,Graph(400,400,10),[Route([0,1,2,3,4,5,6,7,8,9,0])])
app.mainloop()