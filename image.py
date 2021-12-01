# -*- coding:utf-8 -*-
__projet__ = "projet_informatique"
__nom_fichier__ = "image"
__author__ = "Iris Zanoncelli"
__date__ = " 30 novembre 2021"
import interface.GUI_Plateau(Qwidget)

class Image_BMP ():

    def __init__(self, path, offset, width, height, depth, ahead, liste_pixels):
        self.path_ = path
        self.offset_ = offset
        self.width_ =  width
        self.height_ = height
        self.depth_ = depth
        self.ahead_ = ahead
        self.liste_pixels = pixels
        #GUI_Plateau.__init__(self)



