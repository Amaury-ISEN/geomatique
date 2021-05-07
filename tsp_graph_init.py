from math import sqrt

class Lieu ():
    # Classe de création de lieux entendus comme des points de coordonnées x et y
    def __init__(self, x, y) :
        """Instanciation d'un point avec ses attributs coordonnées"""
        self.x = x
        self.y = y
    
    def calcul_distance(self, point):
        """Calcul de la distance entre le point self et une autre instance de Lieu appelée point."""
        distance = sqrt((self.x-self.y)**2 +(point.x-point.y)**2)
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