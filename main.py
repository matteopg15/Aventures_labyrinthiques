"""
Module principal du jeu : génère le labyrinthe et les bonus
"""
try:
    from tkinter import ttk
    from random import *
except ModuleNotFoundError:
    raise RuntimeError("Les modules TKinter et Random sont nécessaires pour jouer")

try:
    from gen_labyrinthe import Labyrinthe
    import graphique
except ModuleNotFoundError:
    raise RuntimeError("Veillez à ce que les fichier gen_labyrinthe.py et graphique.py soient dans le même dossier que main.py")



#tab_piece = []
def gen_bonus(lab):
    """
    Génère les bonus sur le labyrinthe
    Entrée : lab (list)
    Sortie : None
    """
    #global tab_piece
    clef = 0
    for i in range(len(lab)):
        for j in range(len(lab[i])):
            if lab[i][j] == 0:
                if choice((True,False)):
                        lab[i][j] = 5 #5 --> Piece
                        #tab_piece.append([i,j])
                elif randint(1,100) == 1:
                        lab[i][j] = 6 #6 --> Chest
                        clef += 1
                elif randint(1,10) == 1 and clef > 0:
                        lab[i][j] = 7 #7 --> Key
                        clef -= 1
                elif randint(1,30) == 1: 
                        lab[i][j] = 8 #9 --> Spike
                elif randint(1,30) == 1:
                        lab[i][j] = 9 #9 --> Enigme

lab = Labyrinthe(25,14)
lab.fusion_aleatoire()
lab.gen_issues()
lab = lab.totab()
gen_bonus(lab)


graphique.init(lab)
graphique.dessine_le_plateau()