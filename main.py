# -*- coding:utf-8 -*-
__projet__ = "projet_informatique"
__nom_fichier__ = "main"
__author__ = "Iris Zanoncelli"
__date__ = " 26 novembre 2021"


from PyQt5.QtWidgets import *
from interface import GUI_Plateau
from agent import Chat

if __name__ == "__main__":
    print("hello")
    # creation d'un application
    app = QApplication([])
    # creation d'une interface
    gui = GUI_Plateau(taille_plateau=11,x=0,y=0,diametre=50,espacement_cercle=10,image_chat="images/chat_log.jpg")
    x,y = 330,300
    chat = Chat(gui,initial_x= x,initial_y = y)
    print(chat.position())
    chat.mouvement()
    print(chat.position())
    print("Voisins du chat ", chat.recupere_voisins())
    # affichage de l'interface
    gui.show()
    # lancement de l'application
    r = app.exec_()