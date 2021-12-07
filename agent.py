import random

class Chat:

    def __init__(self,gui,initial_x,initial_y, max_iteration_fictif):
        """
        :param gui:
        :param initial_x: ce sont les positions initiale du chat
        :param initial_y: positions initiales du chat
        :param correspond au maximun d'iteration auquel le chat va penser a faire, comme dans les échecs c'est le nombre de coup qu'on prévoit
        pour l'instant on dit que la position initiale du chat est toujours la même.
        """
        self.gui = gui
        self.x = initial_x
        self.y = initial_y
        self.espacement = self.gui.diametre_ + self.gui.espacement_cercle_  # 50 + 10
        self.max_iteration_fictif = max_iteration_fictif
        self.gui.dessiner_chat(self.x,self.y)

    def mouvement(self): # deplacement réel
        """
        Correspond au déplacement réel du chat. C'est le déplacement optimisé qu'il fera car il aura réfléchit avant a comment gagné
        voisins_accessibles correspond à la liste des cases ou peut avancer le chat par rapport à sa position
        nouvelle_coordonée = nouvelle position que le chat va choisir de se rendre parmi les voisins accessibles autour de lui
        on fait appel a la fonction dessiner_case
        on remet disponible la case de l'ancienne position du chat
        on enregistre les nouvelles coordonnées du chat
        on fait appel à la fonction dessiner_chat pour marquer d'un point rouge la nouvelle position du chat
        puis on rend la position du chat innacessible au joueur soit au click
        :return:
        """
        
        nouvelle_coordonnee = self.minimax()
        self.gui.dessiner_case(self.x,self.y)
        self.gui.dico_coordonnee_cercles[(self.x, self.y)] = 0 # on remet accessible à l'occupation du démon
        self.x, self.y = nouvelle_coordonnee
        self.gui.dessiner_chat(self.x,self.y)
        self.gui.dico_coordonnee_cercles[(self.x, self.y)] = 2 # on rend la case innaccessible à l'occupation du démon car c'est la position de l'ange
        
    def recupere_voisins_accessibles(self, grille, x, y):
        """

        :param grille: correspond à la position des cercles soit aux coordonées
        :param x: position du chat
        :param y: position du chat
        voisins : correspond à toutes les coordonnées des voisins situés autour du chat
        création de la liste des voisins qui seront accessibles

        :return: ca retourne la liste des voisins accessibles (soit des points vert clair ou le chat peut aller dessus)selon la position du chat


        """
        voisins = self.recupere_voisins(x, y)
        voisins_accessibles = []
        for voisin in voisins:
            if not grille[voisin]:
                voisins_accessibles.append(voisin)
        return voisins_accessibles

    def position(self):
        """
        :return: la position du chat réelle, quand il y a un self c'est que c'est réelle
        """
        return self.x,self.y
    
    def recupere_voisins(self, x, y):
        """
        :param x:
        :param y:
        Creation de la liste vide des futurs voisins du chat
        on commence par regarder les voisins situés à gauche de la position du chat
        si la position du chat - l'espacement est supérieur à 0, ca signifie qu'il y a encore un cercle et qu'il et tjrs dans la grille (en gros qu'il n'est pas sur le dernier cercle)
        alors on ajoute les coordonées de ce cercle dans la liste car c'est un voisin
        si le cercle situé en dessous de celui du chat est dans le plateau alors on l'ajoute comme voisins potentiel
        condition du haut : si le cercle situé au dessus est encore dans le plateau, on l'ajoute à la liste

        on réalise la meme chose mais du coté droit.
        quand on divise par //2 on prend en compte le décalage qu'il y a entre les cercles le fait qu'il soit pas aligné de la même manière


        :return: retourne la liste des cercles qui sont autour de l'emplacement du chat.
        donc ca retourne les coordonnées de chaque cercle positionnés autour du chat.

        """
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
        if x + self.espacement//2 <= self.espacement * (self.gui.taille_plateau_ - 1) : #condition de droite
            voisins.append((x + self.espacement,y))
            if y + self.espacement <=self.espacement * (self.gui.taille_plateau_ - 1): # à vérifier condition du bas a tester si c'est superieur et égal
                voisins.append((x + self.espacement//2, y + self.espacement))
            if y - self.espacement >= 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x + self.espacement//2,y - self.espacement))
        return voisins

    def minimax(self):
        """
        on commence à faire l'optimisation du jeu
        on cherche sur quel voisin le chat pourrait aller théoriquement.
        num_etape = au nombre d'étape que l'on prévoit à l'avance, on le définit nous même = on regarde dans le futur et etudie les prochains coups possibles
        L'optimisation d'un jeu s'illustre à l'aide d'un arbre en particulier de ses feuilles, de ses branches et ses racines.
        on cherche donc à évaluer les positions de chacun, on va donc devoir travailler en l'alternance soit du coté de l'ange soit du cote du démon.

        Les racines de l'arbre = position initale du chat et du démon

        on crée une copie de la grille réel qui correspondra à la grille de prédictions pour les prochains mouvements du chat et du démon. grille_copie ici c'est la grille des mouvements anticipés
        :return: la prochaine position fictive que le chat devrait prendre pour avancer de manière optimale
        """
        num_etape = 0
        branches = self.recupere_voisins_accessibles(grille = self.gui.dico_coordonnee_cercles, x= self.x, y= self.y) # calcule des 1ere branches
        if len(branches) == 0 : 
            return self.gui.perdu()
        mini_seuil = -1e30
        etape_min = 10
        prochaine_position = branches[0]
        for branche in branches: # 1er étape d'anticipation itere sur les voisins possibles/ correspond presque a un max value
        
            # on anticipe au choix possible de l'ange pour sa prochaine action, anticipe la prochaine action de l'ange, prochaine position possible,
            grille_anticipee = self.gui.dico_coordonnee_cercles.copy() # va faire une copie et va changer les positions, fait une copy qui impacte pas la grille initiale
    
            # nouvelle position fictive, on teste les positions a savoir si c'est les meilleurs valeurs ou pas
            # on passe au choix posssible du démon
            mini_value, etape = self.min_value(grille_anticipee, branche[0], branche[1], num_etape+1) # 2eme étape d'anticipation
            # doit récuperer la position du démon
            if mini_value > mini_seuil: # a revoir et essayer de comprendre
                mini_seuil = mini_value
                prochaine_position = branche # a revoir, on a vu que la position de la branche testé juste avant est bonne donc on la prend comme la bonne position
            elif mini_value == mini_seuil and etape < etape_min : #TODO optimiser en fonction du nombre d'étape
                etape_min = etape 
                prochaine_position = branche 
            print(branche, mini_value, mini_seuil,etape)
            print()
            #passe a la 3eme anticipation et devrait mettre en place la boucle sur quelques itérations( comme aux échec)
        return prochaine_position

    def min_value(self, grille, position_fictive_x, position_fictive_y, nombre_etape): # les valeurs de quand on est dans un min donc dans la position de l'adversaire
        if self.est_cote(position_fictive_x, position_fictive_y) or self.est_bloque(grille, position_fictive_x, position_fictive_y):
            return self.evaluation(grille, position_fictive_x, position_fictive_y), nombre_etape

        if nombre_etape == self.max_iteration_fictif:
            return self.fonction_evaluation(grille,position_fictive_x, position_fictive_y, nombre_etape)
        
        valeur = 1e30
        for coordonee in grille:
            if not (coordonee == (position_fictive_x, position_fictive_y) or grille[coordonee] == 1) : # utilisateur peut atteindre
                grille_copie = grille.copy()
                grille_copie[coordonee] = 1
                valeur = min(valeur, self.max_value(grille_copie, position_fictive_x, position_fictive_y, nombre_etape))
        return valeur, nombre_etape

    def max_value(self, grille, position_fictive_x, position_fictive_y, nombre_etape): # maximise (si on se place coté démon, on maximise et on minimise celle de l'ange)
        
        valeur = -1e30
        for coordonee in self.recupere_voisins_accessibles(grille,position_fictive_x,position_fictive_y):
            grille_copie = grille.copy()
            valeur = max(valeur, self.min_value(grille_copie, coordonee[0],coordonee[1], nombre_etape+1)[0])
        return valeur

    def fonction_evaluation(self,grille, x, y,nombre_etape):
        """

        :param grille:
        :param x:
        :param y:
        :param nombre_etape:
        :return:
        #TODO essayer d'autres fonctions d'évaluation (ex prendre en compte le nombre de cases voisines inatteignables)
        """

        return -min([x,y,self.gui.width - x,self.gui.height - y]), nombre_etape
        

    def evaluation(self,grille_anticipee, x_anticipe, y_anticipe):#changer de nom la fonction qui indique si on est bloqué ou pas donc si on est arrivé à la sortie ou si le démon nous a bloqué
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
            return -1

    def est_bloque(self, grille_anticipee, x_anticipe, y_anticipe):
        """

        :param grille_anticipee:
        :param x_anticipe:
        :param y_anticipe:
        :return:
        """

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
        #x gere le gauche droite
        if x_anticipe <= self.espacement//2 : # on le fait pour le cote ange
            return True
        if x_anticipe >= self.espacement * (self.gui.taille_plateau_-1) - self.espacement//2:
            return True
        # y gere le bas et le haut
        if y_anticipe <= self.espacement // 2:
            return True
        if y_anticipe >= self.espacement * (self.gui.taille_plateau_ - 1) - self.espacement // 2:
            return True
        return False