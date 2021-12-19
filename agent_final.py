# -*- coding:utf-8 -*-

__projet__ = "Chat noir"
__nom_fichier__ = "agent_final"
__author__ = "Emilyne BEAUDET & Iris ZANONCELLI"
__date__ = "décembre 2021"

import random


class Chat:

    def __init__(self, gui, initial_x, initial_y, max_iteration_fictif):
        """
        max_iteration_fictif correspond au maximun d'étape que les joueurs peuvent prévoir. Ils peuvent donc prevoir 2 coups chacun à l'avance
        """
        self.gui_ = gui
        self.x_ = initial_x
        self.y_ = initial_y
        self.espacement_ = self.gui_.diametre_ + self.gui_.espacement_cercle_  # L'espacement correspond à l'écart entre deux cercles\
        # en partant du centre du premier cercle pour arriver au centre du deuxième cercle.
        self.max_iteration_fictif_ = max_iteration_fictif
        self.gui_.dessiner_point_chat(self.x_, self.y_)

    def position(self):
        """
        Donne la position du chat réelle
        """
        return self.x_, self.y_

    def mouvement(self):
        """
        Correspond au déplacement réel du chat
        voisins_accessibles = liste des cases voisines au chat sur laquelles il peut se rendre.
        nouvelle_coordonée = c'est la nouvelle position que le chat aura choisi de se rendre, parmi ses voisins accessibles
        :return: fait appel à la fonction d'affichage gagne si le chat a reussi a sortir du plateau
        """
        nouvelle_coordonnee = self.minimax() # fait appel à la stratégie de déplacement
        self.gui_.dessiner_case(self.x_, self.y_)
        self.gui_.dico_coordonnee_cercles[(self.x_, self.y_)] = 0  # on remet la position accessible à l'occupation du chat
        self.x_, self.y_ = nouvelle_coordonnee

        self.gui_.dessiner_point_chat(self.x_, self.y_)
        # changement d'état du cercle, 2 correspondant à la présence du chat, le joueur ne pourra pas cliquer dessus
        self.gui_.dico_coordonnee_cercles[(self.x_, self.y_)] = 2

        # test fin de la partie :test si le chat gagne
        if self.est_cote(self.x_, self.y_):
            return self.gui_.gagne()

    def recupere_voisins(self, x, y):
        """
        :param x: abscisse du centre du cercle ou se situe le chat
        :param y: ordonnée du centre du cercle ou se situe le chat

        Correspond à la fonction qui permet d'avoir les coordonnées des cercles voisins au cercle chat
        :return: la liste des coordonnées de chaque cercle positionnés autour du chat qui consitue les voisins du chat

        """
        voisins = []

        # recherche les voisin de gauche
        if x - self.espacement_ >= 0:
            voisins.append((x - self.espacement_, y))

            # Voisin du bas à gauche
            if y + self.espacement_ <= self.espacement_ * (self.gui_.taille_plateau_ - 1):
                # s'il n'a pas dépassé la ligne du bas, on ajoute à la liste des voisins le centre du cercle situé en dessous à gauche du chat \
                #d'ou l'ajout de l'espacement à y et l'ajout dela moitié de l'espacement à x
                voisins.append((x - self.espacement_ // 2, y + self.espacement_))

            # Voisins du haut à gauche
            if y - self.espacement_ >= 0:
                voisins.append((x - self.espacement_ // 2, y - self.espacement_))

        # Voisins de droite
        if x + self.espacement_ <= self.espacement_ * (self.gui_.taille_plateau_ - 1):
            voisins.append((x + self.espacement_, y))

            # Voisin du bas à droite
            if y + self.espacement_ <= self.espacement_ * (self.gui_.taille_plateau_ - 1):
                voisins.append((x + self.espacement_ // 2, y + self.espacement_))

            # Voisin du haut à droite
            if y - self.espacement_ >= 0:
                voisins.append((x + self.espacement_ // 2, y - self.espacement_))

        return voisins

    def recupere_voisins_accessibles(self, grille, x, y):
        """

        :param grille: dico_coordonnee_cercles : correspond à toutes les coordonnées des centres des cercles du plateau
        :param x et param y : sont les coordonées du chat
        voisins : liste des voisins qui sont accessibles au chat
        :return: la liste des voisins accessibles : les cercles vert clair ou peut se deplacer le chat
        """
        liste_voisins = self.recupere_voisins(x, y)
        voisins_accessibles = []
        for voisin in liste_voisins:
            if grille[voisin] == 0:
                voisins_accessibles.append(voisin)
        return voisins_accessibles

    def minimax(self):
        """
        on commence à faire l'optimisation du jeu
        on cherche sur quel voisin le chat pourrait aller théoriquement pour maximiser son gain et minimiser le gain de l'utilisateur
        num_etape = au nombre d'étape que l'on prévoit à l'avance, on le définit nous même = on regarde dans le futur et etudie les prochains coups possibles
        L'optimisation d'un jeu s'illustre à l'aide d'un arbre en particulier de ses feuilles, de ses branches et ses racines.
        on cherche donc à évaluer les positions de chacun, on va donc devoir travailler en l'alternance soit du coté de l'ange soit du cote du démon.

        Les racines de l'arbre = position initale du chat et du démon

        on crée une copie de la grille réel qui correspondra à la grille de prédictions pour les prochains mouvements du chat et du démon. grille_copie ici c'est la grille des mouvements anticipés
        :return: la prochaine position fictive que le chat devrait prendre pour avancer de manière optimale
        """
        num_etape = 0
        branches = self.recupere_voisins_accessibles(grille=self.gui_.dico_coordonnee_cercles, x=self.x_, y=self.y_)  # calcule des 1ere branches
        if len(branches) == 0:
            return self.gui_.perdu() # appelle la fonction d'affichage s'il n'y a plus de voisin
        mini_seuil = -1e30
        etape_min = 10
        prochaine_position = branches[0]
        for branche in branches:  # 1er étape d'anticipation qui itère sur les voisins possibles

            # on anticipe la prochaine action du chat soit sa prochaine position possible.
            grille_anticipee = self.gui_.dico_coordonnee_cercles.copy()  #copie du plateau et change les positions pour obtenir les positions fictives possible

            # nouvelle position fictive, on teste les positions a savoir si c'est les meilleurs valeurs ou pas
            # on passe au choix posssible du démon
            mini_value, etape = self.min_value(grille_anticipee, branche[0], branche[1],num_etape + 1)  # 2eme étape d'anticipation
            # doit récuperer la position du démon
            if mini_value > mini_seuil:
                mini_seuil = mini_value
                prochaine_position = branche

            elif mini_value == mini_seuil and etape < etape_min:
                etape_min = etape
                prochaine_position = branche

        return prochaine_position

    def min_value(self, grille, position_fictive_x, position_fictive_y, nombre_etape):
        """
        du coté du chat : minimalise le gain de l'utilisateur
        """
        if self.est_cote(position_fictive_x, position_fictive_y) or self.est_bloque(grille, position_fictive_x,position_fictive_y):
            return self.evaluation(grille, position_fictive_x, position_fictive_y), nombre_etape

        if nombre_etape == self.max_iteration_fictif_:
            return self.fonction_evaluation(position_fictive_x, position_fictive_y, nombre_etape)

        valeur = 1e30
        for coordonee in grille:
            if not (coordonee == (position_fictive_x, position_fictive_y) or grille[coordonee] == 1):
                grille_copie = grille.copy()
                grille_copie[coordonee] = 1
                valeur = min(valeur, self.max_value(grille_copie, position_fictive_x, position_fictive_y, nombre_etape))
        return valeur, nombre_etape

    def max_value(self, grille, position_fictive_x, position_fictive_y,nombre_etape):
        """
        de coté du chat : maximalise le gain du chat
        """
        valeur = -1e30
        for coordonee in self.recupere_voisins_accessibles(grille, position_fictive_x, position_fictive_y):
            grille_copie = grille.copy()
            valeur = max(valeur, self.min_value(grille_copie, coordonee[0], coordonee[1], nombre_etape + 1)[0])
        return valeur

    def fonction_evaluation(self, x, y, nombre_etape):
        """
        evalue la plus petite distance entre les 4 distances pour savoir quel est le chemin optimisé
        """
        # x correspond a la distance horizontale entre le bord gauche du plateau et le point
        # gui.width - x correspond a la distance horizontale entre le bord droit du plateau et le point
        # y correspond a la distance verticale entre le haut du plateau et le point
        # gui.width - y correspond a la distance verticale entre le bas du plateau et le point
        return -min([x, y, self.gui_.width - x, self.gui_.height - y]), nombre_etape

    def evaluation(self, grille_anticipee, x_anticipe,y_anticipe):
        """
        valeur du gain en fonction de l'amplacement anticipé du chat
        """
        if self.est_cote(x_anticipe, y_anticipe):
            return 10  # valeur du gain en position sur un bord

        if self.est_bloque(grille_anticipee, x_anticipe, y_anticipe):
            return -1 # valeur du gain en position bloquante

    def est_bloque(self, grille_anticipee, x_anticipe, y_anticipe):
        """
        Repond à la question : Le chat est-il bloqué ?

        """
        if len(self.recupere_voisins_accessibles(grille_anticipee, x_anticipe,y_anticipe)) == 0:  # regarde le nombre de voisin accessible que le chat possède
            return True
        return False

    def est_cote(self, x_anticipe,y_anticipe):
        """
        Repond à la question : Est ce que l'on est sur un coté ?
        la fonction vérifie si chat est sur l'un des cotés du plateau
        """
        if x_anticipe <= self.espacement_ // 2:
            return True
        if x_anticipe >= self.espacement_ * (self.gui_.taille_plateau_ - 1) - self.espacement_ // 2:
            return True
        if y_anticipe <= self.espacement_ // 2:
            return True
        if y_anticipe >= self.espacement_ * (self.gui_.taille_plateau_ - 1) - self.espacement_ // 2:
            return True
        return False
