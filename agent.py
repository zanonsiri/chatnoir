import random

class Chat:

    def __init__(self,gui,initial_x,initial_y):
        self.gui = gui
        self.x = initial_x
        self.y = initial_y
        self.espacement = self.gui.diametre_ + self.gui.espacement_cercle_  # 50 + 10

    def mouvement(self):
        voisins_accessibles = self.recupere_voisins_accessibles(grille= self.gui.dico_coordonnee_cercles, x= self.x, y= self.y)
        nouvelle_coordonnee = random.choice(voisins_accessibles)
        self.gui.dessiner_case(self.x,self.y)
        self.x, self.y = nouvelle_coordonnee
        self.gui.dessiner_chat(self.x,self.y)
        #import time
        #time.sleep(2)

    def recupere_voisins_accessibles(self, grille, x, y): # grille c'est les coordonnées, la position des cercles

        voisins = self.recupere_voisins(x, y)
        voisins_accessibles = []
        for voisin in voisins:
            if not grille[voisin]:
                voisins_accessibles.append(voisin)

        return voisins_accessibles

    def position(self):
        return self.x,self.y
    
    def recupere_voisins(self, x, y):
        voisins = []

        #Voisin de gauche 
        if x - self.espacement >= 0 : #condition de gauche
            voisins.append((x - self.espacement,y))
            if y + self.espacement <= self.espacement * (self.gui.taille_plateau_-1): #TODO à vérifier condition du bas
                voisins.append((x - self.espacement//2, y + self.espacement))
            if y - self.espacement >= 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x - self.espacement//2, y - self.espacement))

        #Voisins de droite
        if x + self.espacement <= self.espacement * (self.gui.taille_plateau_ - 1) : #condition de droite
            voisins.append((x + self.espacement,y))
            if y + self.espacement <=self.espacement * (self.gui.taille_plateau_ - 1): #TODO à vérifier condition du bas a tester si c'est superieur et égal
                voisins.append((x + self.espacement//2, y + self.espacement))
            if y - self.espacement >= 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x + self.espacement//2,y - self.espacement))

        
        return voisins

    def minimax(self):
        """
        création de l'optimisation du jeu
        :return:
        """
        racine = self.position() # position initiale
        branches = self.recupere_voisins()
        feuilles = 1
    def min_value(self): # les valeurs de quand on est dans un min donc dans la position de l'adversaire
        return 1

    def max_value(self): # maximise (si on se place coté démon, on maximise et on minimise celle de l'ange)
        return 1

    def evaluation(self,grille_anticipe, x_anticipe, y_anticipe):# la fonction qui indique si on est bloqué ou pas donc si on est arrivé à la sortie ou si le démon nous a bloqué

        if self.est_cote ( x_anticipe, y_anticipe):
            return 10 # return une valeur, on a réussi

        if self.est_bloque (grille_anticipe, x_anticipe, y_anticipe):
            return 0

    def est_bloque(self, grille_anticipe, x_anticipe, y_anticipe):
        return 1



    def est_cote(self, x_anticipe, y_anticipe): # quand on est arrivé au bout mais la on enticipe donc self.x vaut tjrs la racine, donc on crée un autre plateau dans notre tête.
        """
        est ce que l'on est sur un cote ?
        :param grille_anticipee:
        :param x_anticipe:
        :param y_anticipe:
        :return:
        """
        if x_anticipe <= self.espacement//2 : # on le fait pour le cote ange
            return True
        if x_anticipe >= self.espacement * (self.gui.taille_plateau_-1) - self.espacement//2:
            return True # y gere le bas et le haut et x le gauche droite
        if y_anticipe <= self.espacement // 2:  # on le fait pour le cote ange
            return True
        if y_anticipe >= self.espacement * (self.gui.taille_plateau_ - 1) - self.espacement // 2:
            return True  # y gere le bas et le haut et x le gauche droite
        return False
