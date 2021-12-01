import random

class Chat:

    def __init__(self,gui,initial_x,initial_y):
        self.gui = gui
        self.x = initial_x
        self.y = initial_y
        self.espacement = self.gui.diametre_ + self.gui.espacement_cercle_  # 50 + 10

    def mouvement(self): # deplacement réel
        
        voisins_accessibles = self.recupere_voisins_accessibles(grille= self.gui.dico_coordonnee_cercles, x= self.x, y= self.y)
        nouvelle_coordonnee = random.choice(voisins_accessibles)
        self.gui.dessiner_case(self.x,self.y)
        self.gui.dico_coordonnee_cercles[(self.x, self.y)] = 0 # on remet accessible à l'occupation du démon
        self.x, self.y = nouvelle_coordonnee
        self.gui.dessiner_chat(self.x,self.y)
        self.gui.dico_coordonnee_cercles[(self.x, self.y)] = 2 # on rend la case innaccessible à l'occupation du démon car c'est la position de l'ange
        
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
            if y + self.espacement <= self.espacement * (self.gui.taille_plateau_-1): # à vérifier condition du bas
                voisins.append((x - self.espacement//2, y + self.espacement))
            if y - self.espacement >= 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x - self.espacement//2, y - self.espacement))

        #Voisins de droite
        if x + self.espacement <= self.espacement * (self.gui.taille_plateau_ - 1) : #condition de droite
            voisins.append((x + self.espacement,y))
            if y + self.espacement <=self.espacement * (self.gui.taille_plateau_ - 1): # à vérifier condition du bas a tester si c'est superieur et égal
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
        racine = self.position() # position initiale de l'ange
        branches = self.recupere_voisins_accessibles(grille = self.gui.dico_coordonnee_cercles, x= self.x, y= self.y) # calcule des 1ere branches
        mini_seuil = -10
        for branche in branches: # 1er étape d'anticipation
            # on anticipe au choix possible de l'ange pour sa prochaine action, anticipe la prochaine action de l'ange, prochaine position possible,
            grille_anticipee = self.gui.dico_coordonnee_cercles.copy() # va faire une copie et va changer les positions, fait une copy qui impacte pas la grille initiale

            #grille_anticipee[racine[0], racine[1]] = 0
            #grille_anticipee[branche[0], branche[1]] = 2 # nouvelle position fictive, on teste les positions a savoir si c'est les meilleurs valeurs ou pas
            # on passe au choix posssible du démon
            mini_value = self.min_value(grille_anticipee, branche[0], branche[1]) # 2eme étape d'anticipation
            # doit récuperer la position du démon
            if mini_value >  mini_seuil: # a revoir et essayer de comprendre
                mini_seuil = mini_value
                prochaine_position = branche # a revoir, on a vu que la position de la branche testé juste avant est bonne donc on la prend comme la bonne position
            # passe a la 3eme anticipation et devrait mettre en place la boucle sur quelques itérations( comme aux échec)
        return prochaine_position

    def min_value(self): # les valeurs de quand on est dans un min donc dans la position de l'adversaire
        return 1

    def max_value(self): # maximise (si on se place coté démon, on maximise et on minimise celle de l'ange)
        return 1

    def evaluation(self,grille_anticipee, x_anticipe, y_anticipe):# la fonction qui indique si on est bloqué ou pas donc si on est arrivé à la sortie ou si le démon nous a bloqué
        """
        evaluation des feuilles
        :param grille_anticipeee:
        :param x_anticipe:
        :param y_anticipe:
        :return:
        """
        if self.est_cote ( x_anticipe, y_anticipe):
            return 10 # return une valeur, on a réussi

        if self.est_bloque (grille_anticipee, x_anticipe, y_anticipe):
            return 0

    def est_bloque(self, grille_anticipee, x_anticipe, y_anticipe):

        if len(self.recupere_voisins_accessibles(grille_anticipee, x_anticipe, y_anticipe)) == 0 : # est ce qu'il est bloqué ?
            return True
        return False

    def est_cote(self, x_anticipe, y_anticipe): # quand on est arrivé au bout mais la on enticipe donc self.x vaut tjrs la racine, donc on crée un autre plateau dans notre tête.
        """
        est ce que l'on est sur un cote ?
        :param grille_anticipeee:
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


"""
il reste a completer max_value et min_value meme niveau que le for mais dans maxvalue t'appelle min_value et inversement
ajouter l'anticipation Max ( 4 comme aux echecs) profondeur max sur laquelle aller
il faut pouvoir estimer la valeur, la note de la position sur laquelle on est arrivé. 
veut juste savoir si on arrive ou pas, en gros si le demon peut ne pas nous bloquer
mais c'est pas la longueur de ton chemin qu'est vraiment important

min/max
mise en place les profondeurs max 
attribution d'une note
"""