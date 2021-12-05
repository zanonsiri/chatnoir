# -*- coding:utf-8 -*-
__projet__ = "projet_informatique"
__nom_fichier__ = "main"
__author__ = "Emilyne Beaudet et Iris Zanoncelli "
__date__ = " 26 novembre 2021"


from PyQt5.QtWidgets import *
from interface import GUI_Plateau
from agent import Chat

if __name__ == "__main__":
    # creation d'un application
    app = QApplication([])
    # creation d'une interface
    gui = GUI_Plateau(taille_plateau=11,x=0,y=0,diametre=50,espacement_cercle=10)
    x,y = 480,480

    # Ajouter un contrôle sur les coordonnées au


    chat = Chat(gui,initial_x= x,initial_y = y, max_iteration_fictif= 2)
    print("Position du chat initial : ",chat.position())
    #chat.minimax()

    for _ in range (3):

        chat.mouvement()
        print()
        print("Nouvelle étape ")
        print()
        print("Position du chat : ", chat.position())

    print("Voisins du chat ", chat.recupere_voisins(chat.x, chat.y))

    # affichage de l'interface
    gui.show()
    # lancement de l'application
    r = app.exec_()