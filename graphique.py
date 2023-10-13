"""
Module graphique du jeu
"""
#MessageBox Enigme (gagné/perdu)
#Affichage gagné et perdu
#Équilibrer le système d'intérêts
from tkinter import *
from tkinter import ttk

try:
    import gen_enigme as ge
    import gen_shop as gs
    import gen_win_loose as gw
except ModuleNotFoundError:
    raise RuntimeError("Veillez à ce que les fichier gen_shop.py, gen_enigme.py et gen_win_loose.py soient dans le même dossier que main.py")

HAUTEUR = 0
LARGEUR = 0
COTE_CASE = 30
LABYRINTHE = 0
fenetre = Tk()
fenetre.title("Labyrinthe")
fond = Canvas(fenetre)
#KEY BINDING
fenetre.bind("<z>", lambda x: mouvement(0))
fenetre.bind("<s>", lambda x: mouvement(1))
fenetre.bind("<q>", lambda x: mouvement(2))
fenetre.bind("<d>", lambda x: mouvement(3))

#IMAGE LOADING
try :
    piece = PhotoImage(file='piece.png')
    chest = PhotoImage(file='chest.png')
    key = PhotoImage(file='key.png')
    trap = PhotoImage(file='spike.png')
    enigme = PhotoImage(file='énigme.png')
    bonhomme = PhotoImage(file='personnage.png')
except :
    raise RuntimeError("Impossible de charger les images, veillez à ce qu'elles soient dans le même dossier que main.py")


temps = 10
nb_piece = 5
interet = 0
nb_key = 0
en_enigme = False
x,y = 1,1
def init(lab):
    global HAUTEUR, LARGEUR,LABYRINTHE,fenetre,fond
    HAUTEUR = len(lab)
    LARGEUR = len(lab[0])
    LABYRINTHE = lab
    LABYRINTHE[y][x] = 2
    fond = Canvas(fenetre, width = (LARGEUR*2+1) * COTE_CASE, height = (HAUTEUR*2+1) * COTE_CASE)
    fond.pack()

def dessine_le_plateau():
    '''
    Affiche le plateau dans lequel le joueur évolue
    Entrée : HAUTEUR (int, global), LARGEUR (int, global), COTE_CASE (int, global),LABYRINTHE (list, global)
    Sortie : None
    '''
    global HAUTEUR, LARGEUR, COTE_CASE,LABYRINTHE
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            if LABYRINTHE[i][j] == 0:
                couleur = "white"
            elif LABYRINTHE[i][j] == 1:
                couleur = "black"
            elif LABYRINTHE[i][j] == 2:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = bonhomme)
            elif i == 1 and j == 1:
                couleur = "red"
            elif LABYRINTHE[i][j] == 4:
                couleur = "green"
            elif LABYRINTHE[i][j] == 5:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = piece)
            elif LABYRINTHE[i][j] == 6:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = chest)
            elif LABYRINTHE[i][j] == 7:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = key)
            elif LABYRINTHE[i][j] == 8:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = trap)
            elif LABYRINTHE[i][j] == 9:
                couleur = False
                fond.create_image(j*COTE_CASE, i*COTE_CASE, anchor=NW, image = enigme)
            if couleur != False:
                fond.create_rectangle(j*COTE_CASE, i*COTE_CASE, (j+1)*COTE_CASE, (i+1)*COTE_CASE, fill = couleur)
    fenetre.mainloop()
def end(resultat):
    global fenetre
    fenetre.quit()
    fenetre.destroy()
    gw.show_window(resultat)



    
def check_bonus():
    """
    Vérifie si le joueur se trouve sur un bonus et applique ses effets s'il se trouve sur l'un d'entre eux
    Entrée : LABYRINTHE (list, global),nb_piece (int, global), nb_key (int, global),temps (int, global),
    en_enigme (bool, global),y (int, global),x (int, global),interet (int, global)
    Sortie : None
    """
    global LABYRINTHE,nb_piece, nb_key,temps,en_enigme,y,x,interet
    if LABYRINTHE[y][x] == 4:
        end("win")
    elif LABYRINTHE[y][x] == 5:
        nb_piece += 2
    elif LABYRINTHE[y][x] == 7:
        nb_key += 1
    elif LABYRINTHE[y][x] == 6 and nb_key >= 1:
        nb_key -= 1
        nb_piece += 30
    elif LABYRINTHE[y][x] == 8:
        temps -= 5
    elif LABYRINTHE[y][x] == 9:
        en_enigme = True #empêche le joueur de se déplacer
        if ge.enigme(): #test si l'enigme est réussi
            nb_piece += 30
        else:
            nb_piece -= 15
        en_enigme = False


def check_temps():
    """
    Vérifie si le joueur a encore des déplacements, si non, il le renvoie au début et ouvre le magasin. 
    S'il n'a plus de déplacements ni de pièces, il a perdu 
    Entrée : temps (int, global),x (int, global),y (int, global),nb_piece (int, global),interet (int, global)
    Sortie : (bool)
    """
    global temps,x,y,nb_piece,interet
    if temps <= 0:
        nb_piece += interet * 4
        if nb_piece <= 0:
            end("loose")
        else:
            fond.create_rectangle(x*COTE_CASE, y*COTE_CASE, (x+1)*COTE_CASE, (y+1)*COTE_CASE, fill = "white")
            x,y = 1,1
            fond.create_image(x*COTE_CASE, y*COTE_CASE, anchor=NW, image = bonhomme)
            
            gs.show_window(nb_piece,temps,interet)
            nb_piece,temps,interet = gs.purchases
            print(nb_piece,temps,interet)
        return False
    return True


def mouvement(direction):
    """
    Permet d'afficher et d'appliquer les mouvements du joueur
    Entrée : LABYRINTHE (list, global),x (int, global),y (int, global),temps (int, global),en_enigme (bool, global)
    Sortie : None 
    """
    global LABYRINTHE,x,y,temps,en_enigme
    if check_temps() and not en_enigme:
        if direction == 0:
            
            #HAUT
            if y > 1 and LABYRINTHE[y-1][x] != 1:
            
                LABYRINTHE[y][x] = 0
                fond.create_rectangle(x*COTE_CASE, y*COTE_CASE, (x+1)*COTE_CASE, (y+1)*COTE_CASE, fill = "white")
                x,y = x,y-1
            
        elif direction == 1:
            #BAS
            if y < (HAUTEUR -1) and LABYRINTHE[y+1][x] != 1:
                LABYRINTHE[y][x] = 0
                fond.create_rectangle(x*COTE_CASE, y*COTE_CASE, (x+1)*COTE_CASE, (y+1)*COTE_CASE, fill = "white")
                x,y = x,y+1
        elif direction == 2:
            #GAUCHE
            if x > 1 and LABYRINTHE[y][x-1] != 1:
                LABYRINTHE[y][x] = 0
                fond.create_rectangle(x*COTE_CASE, y*COTE_CASE, (x+1)*COTE_CASE, (y+1)*COTE_CASE, fill = "white")
                x,y = x-1,y
        elif direction == 3:
            #DROITE
            if x < (LARGEUR -1) and LABYRINTHE[y][x+1] != 1:
                LABYRINTHE[y][x] = 0
                fond.create_rectangle(x*COTE_CASE, y*COTE_CASE, (x+1)*COTE_CASE, (y+1)*COTE_CASE, fill = "white")
                x,y = x+1,y
        check_bonus()
        LABYRINTHE[y][x] =2
        fond.create_image(x*COTE_CASE, y*COTE_CASE, anchor=NW, image = bonhomme) 
        temps -= 1
        check_temps()
    

