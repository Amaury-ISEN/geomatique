from math import sqrt
import tkinter as tk
import sys


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


class Affichage(tk.Tk):



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
        
        
        self.canvas=tk.Canvas(self,width=self.width,height=self.height,bg='#DCDCDC')
        
        for i in range(len(graph.liste_lieux)) :
            x0=lieu[i].x
            y0=lieu[i].y
            self.canvas.create_oval(x0,y0,x0+10,y0+10)
            self.canvas.create_text(x0,y0,text=str(i))
        
        self.canvas.pack()

    def create_route(self):
        liste_coord=[]
        for route in self.routes:
            for lieu in route:
                liste_coord.append(lieu.x)
                liste_coord.append(lieu.y)

            self.canvas.create_line(liste_coord,dash = (5, 2))




    def on_key_press(self,event):
        print('coucou')

        self.text.set("Ca fonctionne")
        self.create_route()

    
    def close(self,event):
        self.withdraw() # if you want to bring it back
        sys.exit() # if you want to exit the entire thing
