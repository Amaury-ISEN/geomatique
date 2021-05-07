import random
from lieu import Lieu
import pandas as pd


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







#Graph(10, 100, 5).listelieux()
#Graph(10, 100, 5).calcul_matrice_cout_od()
test = Graph(10, 100, 5)
print(test.matricedesdistances)