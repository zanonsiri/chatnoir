# -*- coding:utf-8 -*-

__projet__ = "Chat noir"
__nom_fichier__ = "interface4"
__author__ = "Emilyne BEAUDET & Iris ZANONCELLI"
__date__ = "novembre 2021"

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from agent_probleme import Chat
import sys


# definition d'une GUI
class GUI_Plateau(QWidget):
    def __init__(self, taille_plateau, x, y, diametre, espacement_cercle):
        self.taille_plateau_ = taille_plateau
        self.x_ = int(x)
        self.y_ = y
        self.centre_ = (self.x_, self.y_)
        self.diametre_ = diametre
        self.espacement_cercle_ = espacement_cercle
        # self.image_chat = image_chat

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

        # Creation et connexion du bouton quitter
        self.b_effacer_ = self.create_button("Recommencer", self.reset)
        self.b_effacer_.setFont(QFont("calibri", 13))
        self.b_effacer_.clicked.connect(self.reset)
        self.monLayout.addWidget(self.b_effacer_, 6, 0, 1, 1)

        # Création de cercles et du dico des cercles
        self.tracer_cercles()

        # Création du dico des points composantant les carrées associés aux cercles
        self.cercle_inscrit_aire()

        # Cases impossible en couleur
        self.case_impossibles()

        # Dessin du point du chat
        self.dessiner_point_chat(330, 300)

        # fin de la partie

        #x_chat, y_chat = Chat.position(self)
        #self.resultat_final(x_chat, y_chat)

        # # Image chat
        # x_chat, y_chat = 300, 300
        # self.dessiner_chat(x_chat, y_chat)


    def reset(self):
        """ efface la zone de dessin"""
        self.scene_.clear()

        self.x_ = 0
        self.y_ = 0

        chat = Chat(self, initial_x=330, initial_y=300, max_iteration_fictif=2)
        self.chat.x = 330
        self.chat.y = 300

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
        @return: le dictionnaire des cercles
        """
        self.liste_cercle = []
        xinit = self.x_

        # création du dico des cercles, pour associer un cercle à un état : 0 si pas cliqué et 1 si cliqué
        etat = 0

        for l in range(self.taille_plateau_):
            for c in range(self.taille_plateau_):
                # addEllipse(position en x, position en y, taille du rayon en x, taille du rayon en y, ...)
                self.scene_.addEllipse(self.x_, self.y_, self.diametre_, self.diametre_, QColor(55, 210, 122),
                                       QBrush(Qt.green))
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
        Nous allons ensuite déterminés toutes les coordonnées des points qui composent ce carrés et les mettrent
        dans une liste qui nous permettra d'identifier le cercle sur lequel on clique a partir de la
        fonction MoussePressEvent

        @return: liste_aire
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
                # print("y au rang ", i, " = ",y)
                x = x_coin_carre
                self.liste_aire[num_cercle].append((x, y))

                for j in range(self.diametre_ - 1):  # on retire 1 car on ajoute deja le premier point de la ligne avant
                    # on parcours le carré avec un pas de 1 pour les x et les y
                    x += 1
                    self.liste_aire[num_cercle].append((x, y))
                y += 1

    def case_impossibles(self):
        """
        Cette fonction permet de choisir aléatiorement le nombre de cercles innacessibles par le chat dès le début du jeu
        les cercles sont ensuite choisi aléatoirement sur le plateau et leur état passe de :
            0 = le chat peut aller dessus
        à   1 = le chat ne peut pas y aller

        @return:
        """
        # choix aléatoire du nombre de cases inaccessible par le chat dès le début
        nb_case_impossible = random.randint(3, 15)
        print("nb cases imposs = ", nb_case_impossible)
        # création de la liste des numéros de cercles impossibles
        for i in range(nb_case_impossible):
            # on a un nombre de cases qui ne sont pas accessible sur le plateau
            # on va donc définir de quel cercle il s'agit de façon aléatoire
            # (dans la liste, le 1e cercle et le numéro 0 dans le dictionnaire) PLUS MAINTENANT CHANGER
            num_cercle = random.randint(0, len(self.liste_cercle)-1)
            x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]

            # il ne faut pas que l'un des points innacessible au départ soit la place initiale du chat
            while x_cercle == 330 and y_cercle == 300:
                num_cercle = random.randint(0, self.taille_plateau_**2 - 1)
                x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]

            # on change l'état du cercle, il passe en 1, il ne sera donc pas accessible par le chat
            self.liste_cercle[num_cercle][2] = 1

            # on change la couleur du cercle en vert foncé
            self.redessiner_cercle(x_cercle, y_cercle)

        # création d'un dictionnaire pour simplifier le codage pour les deplacements du chat ?
        self.dico_coordonnee_cercles = {}
        for i in range(len(self.liste_cercle)):
            # on recre un dico contenant les coordonées et les cercles car on ne peut pas faire avec une liste vu que la liste associe les coordonées à un numéro [0,1..] et on ne peut pas utiliser directement les coordonées
            self.dico_coordonnee_cercles[tuple(self.liste_cercle[i][:2])] = self.liste_cercle[i][
                2]  # self.liste_cercle[1]=[60,0,0]
        print("dico", self.dico_coordonnee_cercles)


    def mousePressEvent(self, event):
        """
        La fonction permet de changer
        @param event: le clic souris
        @return:
        """

        # Test fin de partie
        x_chat, y_chat = Chat.position(self)
        print("x et y chat", x_chat, y_chat)
        self.resultat_final(x_chat, y_chat)

        reussite = False
        # on soustrait des valeurs à x et y car l'origine de la fenetre de dessin n'est pas la meme que celle des cercles
        x = event.x() - 87
        y = event.y() - 126

        for num_cercle in range(len(self.liste_cercle)):
            x_cercle, y_cercle, etat = self.liste_cercle[num_cercle]
            cercle = (x_cercle, y_cercle)

            for i in range(len(self.liste_aire[num_cercle])):
                if self.dico_coordonnee_cercles[cercle] == 0 and (x, y) == self.liste_aire[num_cercle][i]:
                    # on change l'état du cercle, il passe en 1, il ne sera donc pas accessible par le chat
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

        @param x: abscisse du centre du cercle
        @param y: ordonnée du centre du cercle
        @param premiere_couleur: couleur initiale du cercle
        @param deuxieme_couleur: couleur que le cercle va prendre suite à l'action
        @return:
        """
        self.scene_.addEllipse(x, y, self.diametre_, self.diametre_, QColor(premiere_couleur),
                               QBrush(deuxieme_couleur))


    def redessiner_cercle(self, x, y):
        """
        Permet de changer la couleur d'un cercle
        @param x: abscisse du centre du cercle
        @param y: ordonnée du centre du cercle
        @return:
        """
        self.dessiner_cercle(x, y, QColor(55, 110, 122), QBrush(Qt.darkGreen))

    def def_chat(self, chat):
        self.chat = chat

    def dessiner_point_chat(self, x, y):
        # self.image_chat
        self.dessiner_cercle(x, y, Qt.red, Qt.red)

    def dessiner_chat(self, x_chat, y_chat):
        image = QPixmap("image_chat_rectangle.png")
        logo = QLabel()
        logo.setPixmap(image)
        self.monLayout.addWidget(logo, x_chat, y_chat)

        window = QWidget()
        window.setLayout(self.monLayout)
        window.show()

    def dessiner_case(self, x, y):
        self.dessiner_cercle(x, y, QColor(55, 210, 122), Qt.green)


    def resultat_final (self, x_chat, y_chat):
        """
        Ce que je veux ici c'est que si on
        @param x_chat:
        @param y_chat:
        @return:
        """
        chat = Chat(self, initial_x=330, initial_y=300, max_iteration_fictif=2)
        print('CHAT')

        # test pour savoir si le joueur a perdu, le chat a gagné
        if chat.est_cote(x_chat, y_chat) == True: # la fonction marche si on fait chat.est_cote(0, 0)
            print("if1")
            fin_partie = QMessageBox()
            fin_partie.setIcon(QMessageBox.Information)
            fin_partie.setText("DOMMAGE, Vous avez perdu... ")
            fin_partie.setStandardButtons(QMessageBox.Ok)
            fin_partie.exec_()

        # test pour savoir si le joueur a gagné, le chat a perdu
        elif chat.est_bloque(self.dico_coordonnee_cercles, x_chat, y_chat) == True :
            print("if2")
            fin_partie = QMessageBox()
            fin_partie.setIcon(QMessageBox.Information)
            fin_partie.setText("BRAVO, vous avez gagné ! ")
            fin_partie.setStandardButtons(QMessageBox.Ok)
            fin_partie.exec_()

        else:
            print("!!!")



