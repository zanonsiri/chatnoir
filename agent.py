import random

class Chat:
    def __init__(self,gui,initial_x,initial_y):
        self.gui = gui
        self.x = initial_x
        self.y = initial_y

    def mouvement(self):
        voisins  = self.recupere_voisins()
        voisins_accessibles = []
        for voisin in voisins : 
            if not self.gui.dico_cercle[voisin] : 
                voisins_accessibles.append(voisin)
        
        nouvelle_coordonnee = random.choice(voisins_accessibles)
        self.gui.dessiner_case(self.x,self.y)
        self.x, self.y = nouvelle_coordonnee
        self.gui.dessiner_chat(self.x,self.y)

    def position(self):
        return self.x,self.y
    
    def recupere_voisins(self):
        voisins = []
        x = self.x
        y = self.y
        espacement = self.gui.diametre_ + self.gui.espacement_cercle_ # 50 + 10
        #Voisin de gauche 
        if x - espacement > espacement : #condition de gauche
            voisins.append((x - espacement,y))
            if y + espacement < self.gui.height - 2 * self.gui.diametre_: #TODO à vérifier condition du bas
                voisins.append((x - espacement//2,y + espacement))
            if y - espacement > 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x - espacement//2,y - espacement))

        #Voisins de droite
        if x + espacement < self.gui.width - (self.gui.diametre_ - self.gui.espacement_cercle_): #condition de droite
            voisins.append((x + espacement,y))
            if y + espacement < self.gui.height - 2 * self.gui.diametre_: #TODO à vérifier condition du bas
                voisins.append((x + espacement//2,y + espacement))
            if y - espacement > 0 : #condition du haut
                #Voisins de dessus gauche
                voisins.append((x + espacement//2,y - espacement))

        
        return voisins
    