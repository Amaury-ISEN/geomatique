from math import sqrt

class Lieu ():
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    
    def calcul_distance(self, point):
        """Calcul de la distance entre le point instancié self et une autre instance de Lieu appelée point."""
        distance = sqrt((self.x-self.y)**2 +(point.x-point.y)**2)
        return distance