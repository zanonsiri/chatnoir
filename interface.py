# -*- coding:utf-8 -*-
__projet__ = "Info"
__nom_fichier__ = "plateau_chat_noir"
__author__ = "Emilyne BEAUDET, Iris Zanoncelli"
__date__ = "novembre 2021"


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random


# definition d'une GUI
class GUI_Plateau(QWidget):
    def __init__(self, taille_plateau, x, y, diametre, espacement_cercle,image_chat):
        self.taille_plateau_ = taille_plateau
        self.x_ = x
        self.y_ = y
        self.centre_ = (self.x_, self.y_)
        self.diametre_ = diametre
        self.espacement_cercle_ = espacement_cercle
        self.image_chat  = image_chat
        # Creation fenêtre graphique
        QWidget.__init__(self)
        self.setWindowTitle("Plateau")
        monLayout = QGridLayout()
        wid, hgt = 700, 700
        self.scene_ = QGraphicsScene(0, 0, wid, hgt, self)
        self.view_ = QGraphicsView(self.scene_, self)
        self.view_.setMinimumSize(wid + 100, hgt + 100)  # pour avoir une petite marge pour le dessin
        monLayout.addWidget(self.view_, 5, 0, 1, 2)
        # Creation et connexion du bouton quitter
        self.b_quitter_ = self.create_button("Quitter", qApp.quit)
        self.b_quitter_.clicked.connect(qApp.quit)
        monLayout.addWidget(self.b_quitter_, 6, 1, 1, 1)
        # Creation et connexion du bouton quitter
        self.b_effacer_ = self.create_button("Recommencer", self.reset)
        monLayout.addWidget(self.b_effacer_, 6, 0, 1, 1)
        # Création de cercles et du dico des cercles
        dico_cercle = self.tracer_cercles()
        # Création du dico des points composantant les carrées associés aux cercles
        dico_aire = self.cercle_inscrit_aire(dico_cercle)
        # Cases impossible en couleur
        dico_cercle = self.case_impossibles(dico_cercle)
        # Réaction au clic
        # x, y = self.mousePressEvent("clicked")
        # self.change_couleur(dico_cercle, dico_aire)
        # Choix du nombre de partie, pas obligé de le garder
        self.label_filename_ = QLabel("Nombre de parties", self)
        self.label_filename_.setAlignment(Qt.AlignCenter)
        self.edit_filename_ = QLineEdit(self)
        # num ligne, num colonne, nbr de ligne, nbr de colonnes
        monLayout.addWidget(self.label_filename_, 1, 0)
        monLayout.addWidget(self.edit_filename_, 1, 1, 1, 1)  # comment regler la taille ? (50/50)
        self.setLayout(monLayout)

    def reset(self):
        """ efface la zone de dessin"""
        self.scene_.clear()

    def create_button(self, libelle, method):
        """ creation d'un bouton et association avec l'action à lancer au clic """
        button = QPushButton(libelle, self)
        button.clicked.connect(method)
        return button

    def tracer_cercles(self):
        """
        Cette fonction permet de tracer les cercles composant le plateu de jeu
        et aussi de créer un dictionnaire contenant tous les cercles avec leur état
        @return: le dictionnaire des cercles
        """
        dico_cercle = {}
        xinit = self.x_
        # centre = (self.x_, self.y_)
        for l in range(self.taille_plateau_):
            for c in range(self.taille_plateau_):
                # addEllipse(position en x, position en y, taille du rayon en x, taille du rayon en y, ...)
                self.scene_.addEllipse(self.x_, self.y_, self.diametre_, self.diametre_, QColor(55, 210, 122),
                                       QBrush(Qt.green))
                # entre les 2 centres on a la valeur d'un diametre + une valeur d'espacement
                self.x_ += self.diametre_ + self.espacement_cercle_
                # création du dico des cercles, pour associer un cercle à un état : 0 si pas cliqué et 1 si cliqué
                dico_cercle[self.x_, self.y_] = 0
            self.y_ += self.diametre_ + self.espacement_cercle_
            self.x_ = xinit
            xinit = self.x_
            if l % 2 == 0:
                # on met les cercles en quinconce
                # il faut décaler le cerle de la ligne suivante de (diametre + espacement)/2
                self.x_ += (self.diametre_ + self.espacement_cercle_) / 2
        print(dico_cercle)
        return dico_cercle

    def cercle_inscrit_aire(self, dico_cercle):
        """
        Avec cette fonction, on associe à chaque cercle, le carré dans lequel il est inscrit
        Nous allons ensuite déterminés toutes les coordonnées des points qui composent ce carrés et les mettrent
        dans un dictionnaire qui nous permettra d'identifier le cercle sur lequel on clique a partir de la
        fonction MoussePressEvent
        @param dico_cercle: le dictionnaire de tout les cercles qui on été crées
        @return: un dictionnaire des coordonnées des points composants le carrée dans lequel le cercle est inscrit
        """
        dico_aire = {}
        for cercle in dico_cercle:
            # on initialise le premier point du carré (angle en haut à gauche)
            self.x_ = self.x_ - self.diametre_ / 2
            # print("x initial = ", self.x_)
            self.y_ = self.y_ - self.diametre_ / 2
            # print("yinitial = ", self.y_)
            dico_aire[cercle] = [(self.x_, self.y_)]
            for l in range(self.diametre_):
                # on parcours le carré avec un pas de 1 pour les x et les y
                for c in range(50):
                    self.x_ += 1
                    dico_aire[cercle].append((self.x_, self.y_))
                self.y_ += 1
                # print("xfinal = ", self.x_)
                # print("yfinal = ", self.y_)
                # print("dico_aire =", dico_aire[cercle])
        return dico_aire

    def case_impossibles(self, dico_cercle):
        """
        Fonction qui positionne aléatoirement le nombre de case inacessible par le chat au début de la partie
        :return:
        """
        # choix aléatoire du nombre de cases inaccessible par le chat dès le début
        nb_case_impossible = random.randint(1, 13)
        print("nb cases imposs", nb_case_impossible)
        # création de la liste des numéros de cercles impossibles
        liste_cercle_impos = []
        for i in range(nb_case_impossible):
            # on a un nombre de cases qui ne sont pas accessible sur le plateau
            # on va donc définir de quel cercle il s'agit de façon aléatoire
            # (dans le dictionnaire, le 1e cercle et le numéro 0 dans le dictionnaire)
            x_num_cercle = random.randint(0, 10)
            y_num_cercle = random.randint(0, 10)
            self.scene_.addEllipse(x_num_cercle, y_num_cercle, self.diametre_, self.diametre_, QColor(55, 110, 122),
                                   QBrush(Qt.darkGreen))
            # for cercle in dico_cercle :
            #     if (x_num_cercle, y_num_cercle) == cercle :
            # liste_cercle_impos.append(num_cercle)
            # print("liste_cercle_impos", liste_cercle_impos)
            # # print(dico_cercle[num_cercle])
            # #x, y, etat = dico_cercle[num_cercle]
            #
            # # c'est pas bon, ca ajoute à la fin 102 : 1
            # dico_cercle[num_cercle] = [1]
            #
            # self.scene_.addEllipse(self.x_, self.y_, self.diametre_, self.diametre_, QColor(55, 110, 122),
            #                        QBrush(Qt.darkGreen))
        print(dico_cercle)
        #return dico_cercle

    def mousePressEvent(self, event):
        """
        @param event: le clic souris
        @return: les coordonnées des points sur lequel on a cliqué
        """
        print("clic souris")
        print(event.x(), event.y())
        return event.x(), event.y()

    def change_couleur(self, dico_cercle, dico_aire):
        """
        Fonction qui assure le changement de couleur du cercle une fois qu'il est cliqué
        :param event:
        :return:
        """
        x, y = self.mousePressEvent(event)
        for cercle in dico_cercle:
            for ele in dico_aire:
                if (x, y) in dico_aire[ele]:
                    self.scene_.addEllipse(self.x_, self.y_, self.diametre_, self.diametre_, QColor(55, 210, 122),
                                           QBrush(Qt.darkGreen))
                else:
                    print("Cliquez sur un cercle s'il nous plait")
                    self.mousePressEvent(event)
    
    def dessine_chat(self, x, y):
        return 