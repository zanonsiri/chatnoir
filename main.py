# -*- coding:utf-8 -*-
__projet__ = "projet_informatique"
__nom_fichier__ = "main"
__author__ = "Emilyne Beaudet et Iris Zanoncelli "
__date__ = " 26 novembre 2021"


from PyQt5.QtWidgets import *
from interface4_probleme import GUI_Plateau
from agent_probleme import Chat

if __name__ == "__main__":
    # creation d'un application
    app = QApplication([])
    # creation d'une interface
    gui = GUI_Plateau(taille_plateau=11,x=0,y=0,diametre=50,espacement_cercle=10)
    x,y = 330, 300

    # Ajouter un contrôle sur les coordonnées au


    chat = Chat(gui,initial_x= 330,initial_y = 300, max_iteration_fictif= 2)  #TODO Utilisable jusqu'à 2 coups en avance du chat, nécessité optimisation si passage à 3
    gui.def_chat(chat)

    # affichage de l'interface
    gui.show()
    # lancement de l'application
    r = app.exec_()