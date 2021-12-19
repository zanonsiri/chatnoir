# -*- coding:utf-8 -*-

__projet__ = "Chat noir"
__nom_fichier__ = "interface_finale"
__author__ = "Emilyne BEAUDET & Iris ZANONCELLI"
__date__ = "novembre 2021"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from agent_final import Chat
import sys


# definition d'une GUI
class GUI_Plateau(QWidget):
    def __init__(self, taille_plateau, x, y, diametre, espacement_cercle):

        self.taille_plateau_ = taille_plateau
        self.x_ = x
        self.y_ = y
        self.centre_ = (self.x_, self.y_)
        self.diametre_ = diametre
        self.espacement_cercle_ = espacement_cercle

        # Creation fenêtre graphique
        QWidget.__init__(self)
        self.setWindowTitle("Plateau")
        self.monLayout = QGridLayout()
        self.width, self.height = 700, 700
        self.scene_ = QGraphicsScene(0, 0, self.width, self.height, self)
        self.view_ = QGraphicsView(self.scene_, self)
        self.view_.setMinimumSize(self.width + 100, self.height + 100)  # pour avoir une petite marge pour le dessin
        self.monLayout.addWidget(self.view_, 5, 0, 1, 2)

        # permet de mettre la fenetre graphique en haut à gauche de l'écran
        self.setGeometry(0, 0, 400, 300)

        # Entete
        self.label_filename_ = QLabel("Jeu du chat noir", self)
        self.label_filename_.setFont(QFont("calibri", 16))
        self.label_filename_.setAlignment(Qt.AlignCenter)
            # num ligne, num colonne, nbr de ligne, nbr de colonnes
        self.monLayout.addWidget(self.label_filename_, 1, 0, 1, 2)
        self.setLayout(self.monLayout)

        # Creation et connexion du bouton quitter
        self.b_quitter_ = self.create_button("Quitter", qApp.quit)
        self.b_quitter_.setFont(QFont("calibri", 13))
        self.b_quitter_.clicked.connect(qApp.quit)
        self.monLayout.addWidget(self.b_quitter_, 6, 1, 1, 1)

        # Creation et connexion du bouton recommencer
        self.b_effacer_ = self.create_button("Recommencer", self.reset)
        self.b_effacer_.setFont(QFont("calibri", 13))
        self.b_effacer_.clicked.connect(self.reset)
        self.monLayout.addWidget(self.b_effacer_, 6, 0, 1, 1)

        # Création de cercles et de la liste des cercles + du dico des cercles
        self.tracer_cercles()

        # Création du dico des points composantant les carrées associés aux cercles
        self.cercle_inscrit_aire()

        # Cases impossible en couleur
        self.case_impossibles()

        # Dessin du point du chat
        self.dessiner_point_chat(330, 300)

    def reset(self):
        """
        Permet d'effacer l'interface de jeu et relance une nouvelle partie
        @return:
        """
        self.scene_.clear()

        self.x_ = 0
        self.y_ = 0

        chat = Chat(self, initial_x=330, initial_y=300, max_iteration_fictif=2)
        self.chat.x_ = 330
        self.chat.y_ = 300

        # Création de cercles et du dico des cercles
        self.tracer_cercles()

        # Création du dico des points composantant les carrées associés aux cercles
        self.cercle_inscrit_aire()

        # Cases impossible en couleur
        self.case_impossibles()

        # Dessin du point du chat
        self.dessiner_point_chat(330, 300)


    def create_button(self, libelle, method):
        """ creation d'un bouton et association avec l'action à lancer au clic """
        button = QPushButton(libelle, self)
        button.clicked.connect(method)
        return button


    def tracer_cercles(self):
        """
        Cette fonction permet de tracer les cercles composant le plateau de jeu
        et aussi de créer une liste contenant tous les cercles avec leur état
        (0 : accessible, 1 : inacessible au chat)
        @return:
        """
        self.liste_cercle = []
        xinit = self.x_

        # création du dico des cercles, pour associer un cercle à un état : 0 si pas cliqué et 1 si cliqué
        etat = 0

        for l in range(self.taille_plateau_):

            for c in range(self.taille_plateau_):
                self.scene_.addEllipse(self.x_, self.y_, self.diametre_, self.diametre_, QColor(55, 210, 122),QBrush(Qt.green))
                self.liste_cercle.append([self.x_, self.y_, etat])
                # entre les 2 centres on a la valeur d'un diametre + une valeur d'espacement
                self.x_ += self.diametre_ + self.espacement_cercle_

            self.y_ += self.diametre_ + self.espacement_cercle_
            self.x_ = xinit
            xinit = self.x_

            # décalage des cercles de la ligne suivante (quinconce)
            if l % 2 == 0:
                # il faut décaler le cerle de la ligne suivante de (diametre + espacement)/2 si numéro de ligne paire,
                # sinon on remet en position x initiale
                self.x_ += (self.diametre_ + self.espacement_cercle_) / 2


    def cercle_inscrit_aire(self):
        """
        Avec cette fonction, on associe à chaque cercle, le carré dans lequel il est inscrit
        Nous allons ensuite déterminés toutes les coordonnées des points qui composent ce carrés et les mettre
        dans une liste qui nous permettra de déterminer a quel cercle appartient le point sur lequel on a cliqué
        via la fonction MoussePressEvent
        @return:
        """

        self.liste_aire = []

        # on fait la liste de tous les points des carrées pour chaque cercle (121)
        for num_cercle in range(len(self.liste_cercle)):
            self.liste_aire.append([])

            xinit, yinit, etat = self.liste_cercle[num_cercle]
            x_coin_carre = xinit - self.diametre_ / 2
            y_coin_carre = yinit - self.diametre_ / 2
            x = x_coin_carre
            y = y_coin_carre

            for i in range(self.diametre_):
                x = x_coin_carre
                self.liste_aire[num_cercle].append((x, y))

                for j in range(self.diametre_ - 1):  # on retire 1 car on ajoute deja le premier point de la ligne avant
                    # on parcours le carré avec un pas de 1 pour les x et les y
                    x += 1
                    self.liste_aire[num_cercle].append((x, y))
                y += 1

    def case_impossibles(self):
        """
        Cette fonction permet de choisir aléatiorement le nombre de cercles inaccessible par le chat dès le début du jeu
        les cercles sont ensuite choisi aléatoirement sur le plateau et leur état passe de :
            0 = le chat peut aller dessus
        à   1 = le chat ne peut pas y aller
        @return:
        """
        # choix aléatoire du nombre de cases inaccessible par le chat dès le début
        nb_case_impossible = random.randint(3, 15)

        # création de la liste des numéros de cercles impossibles
        for i in range(nb_case_impossible):
            # on a un nombre de cases qui ne sont pas accessible sur le plateau
            # on va donc définir de quel cercle il s'agit de façon aléatoire
            num_cercle = random.randint(0, len(self.liste_cercle)-1)
            x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]

            # il ne faut pas que l'un des points innacessible au départ soit la place initiale du chat
            while x_cercle == 330 and y_cercle == 300:
                num_cercle = random.randint(0, self.taille_plateau_**2 - 1)
                x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]

            # changement l'état du cercle, il passe en 1, il ne sera donc plus accessible au chat
            self.liste_cercle[num_cercle][2] = 1

            # changement la couleur du cercle en vert foncé
            self.redessiner_cercle(x_cercle, y_cercle)

        # création d'un dictionnaire pour simplifier le codage pour les deplacements du chat
        self.dico_coordonnee_cercles = {}
        for i in range(len(self.liste_cercle)):
            self.dico_coordonnee_cercles[tuple(self.liste_cercle[i][:2])] = self.liste_cercle[i][2]

    def mousePressEvent(self, event):
        """
        Cette fonction permet de créer une réaction au clique sur l'interface de jeu
        Une fois un cercle cliqué, il change de couleur et devient vert foncé
        @param event: l'evenement correspond au clique
        @return:
        """
        reussite = False
        # on soustrait des valeurs à x et y car l'origine de la fenetre de dessin n'est pas la meme que celle des cercles
        x = event.x() - 88
        y = event.y() - 126
        print(x,y)

        for num_cercle in range(len(self.liste_cercle)):
            x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]
            cercle = (x_cercle, y_cercle)

            for i in range(len(self.liste_aire[num_cercle])):
                if self.dico_coordonnee_cercles[cercle] == 0 and (x, y) == self.liste_aire[num_cercle][i]:
                    # on change l'état du cercle, il passe en 1, il ne sera donc plus accessible au chat
                    self.liste_cercle[num_cercle][2] = 1
                    self.dico_coordonnee_cercles[cercle] = 1
                    self.redessiner_cercle(x_cercle, y_cercle)
                    self.chat.mouvement()
                    reussite = True

        if reussite == False:
            reclick = QMessageBox()
            reclick.setIcon(QMessageBox.Information)
            reclick.setText("Cliquez sur un cercle vert clair s'il vous plait")
            reclick.setStandardButtons(QMessageBox.Ok)
            reclick.exec_()

    def dessiner_cercle(self, x, y, premiere_couleur, deuxieme_couleur):
        """
        Fonction qui dessine les cercles vert clair de l'interface
        @param x: abscisse du centre du cercle
        @param y: ordonnée du centre du cercle
        @param premiere_couleur: couleur initiale du cercle
        @param deuxieme_couleur: couleur que le cercle va prendre suite à une action
        @return:
        """
        self.scene_.addEllipse(x, y, self.diametre_, self.diametre_, QColor(premiere_couleur),QBrush(deuxieme_couleur))

    def redessiner_cercle(self, x, y):
        """
        Permet de changer la couleur d'un cercle cliqué
        @param x: abscisse du centre du cercle
        @param y: ordonnée du centre du cercle
        @return:
        """
        self.dessiner_cercle(x, y, QColor(55, 110, 122), QBrush(Qt.darkGreen))

    def def_chat(self, chat):
        """
        Définition de l'attribu chat
        @param chat: l'objet chat issu de la classe Chat
        @return:
        """
        self.chat = chat

    def dessiner_point_chat(self, x, y):
        """
        Dessine le chat (cercle rouge)
        @param x: abscisse du centre du cercle "chat"
        @param y: ordonnée du centre du cercle "chat"
        @return:
        """
        self.dessiner_cercle(x, y, Qt.red, Qt.red)

    def dessiner_case(self, x, y):
        """
        Permet de dessiner un cercle vert
        @param x: abscisse du centre du cercle
        @param y: ordonnée du centre du cercle
        @return:
        """
        self.dessiner_cercle(x, y, QColor(55, 210, 122), Qt.green)

    def gagne(self):
        """
        Permet de faire afficher la fenetre pour dire au joueur que le chat a gagné
        @return:
        """
        fin_partie = QMessageBox()
        fin_partie.setIcon(QMessageBox.Information)
        fin_partie.setText("DOMMAGE, Vous avez perdu... ")
        fin_partie.setStandardButtons(QMessageBox.Ok)
        fin_partie.exec_()

    def perdu(self):
        """
        Permet de faire afficher la fenetre pour dire au joueur que le chat a perdu
        @return:
        """
        fin_partie = QMessageBox()
        fin_partie.setIcon(QMessageBox.Information)
        fin_partie.setText("BRAVO, vous avez gagné ! ")
        fin_partie.setStandardButtons(QMessageBox.Ok)
        fin_partie.exec_()




