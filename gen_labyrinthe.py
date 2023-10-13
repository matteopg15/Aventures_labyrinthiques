#Module permettant de générer le labyrinthe dans lequel le joueur évolue

from random import randint, choice


class Labyrinthe:
    def __init__(self, c, l):
        """
        Initialisation du Labyrinthe
        Entree : c (int, nb colonnes), l (int, nb lignes)
        Sortie : None
        """
        self.colonnes = c
        self.lignes = l 

        self.labyrinthe = [[ j+(self.lignes+1)*i for j in range(self.colonnes)] for i in range(self.lignes)]
        self.matrice_v = [[1 for j in range(self.colonnes+1)] for i in range(self.lignes)]
        self.matrice_h = [[1 for j in range(self.colonnes)] for i in range(self.lignes+1)]
        self.x = 0
        self.y = 0
        self.deja_visite = []
        self.exploration = []


    def __str__(self):
        """
        Renvoie une chaine de caractères représentant le Labyrinthe
        Entree : Aucune
        Sortie : (str)
        """
        tab = [['#'  for j in range(self.colonnes*2+1)]  for i in range(self.lignes*2+1)]
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                #Nb dans la case
                if i%2 == 1 and j%2 == 1:
                    tab[i][j] = self.labyrinthe[i//2][j//2]

                #Mur vertical
                elif i%2 == 1 and j%2 == 0:
                    if self.matrice_v[i//2][j//2] == 1:
                        tab[i][j] = "#"
                    elif self.matrice_v[i//2][j//2] == 0:
                        tab[i][j] = ' '
                    elif self.matrice_v[i//2][j//2] == 3:
                        tab[i][j] = 'E'
                    elif self.matrice_v[i//2][j//2] == 4:
                        tab[i][j] = 'S'
                #Mur horizontal
                elif i%2 == 0 and j%2 ==1:
                    if self.matrice_h[i//2][j//2]:
                        tab[i][j] = "#"
                    else:
                        tab[i][j] = ' '
    
        res = "\n".join(["".join(["{:^3}".format(str(j)) for j in i]) for i in tab])
        return res
    
    def totab(self):
        """
        Renvoie un tableau représentant le Labyrinthe
        Entree : Aucune
        Sortie : (list)
        """
        tab = [[1  for j in range(self.colonnes*2+1)]  for i in range(self.lignes*2+1)]
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                #Nb dans la case
                if i%2 == 1 and j%2 == 1:
                    tab[i][j] = 0#self.labyrinthe[i//2][j//2]

                #Mur vertical
                elif i%2 == 1 and j%2 == 0:
                    if self.matrice_v[i//2][j//2] == 1:
                        tab[i][j] = 1
                    elif self.matrice_v[i//2][j//2] == 0:
                        tab[i][j] = 0
                    elif self.matrice_v[i//2][j//2] == 3:
                        tab[i][j] = 3
                    elif self.matrice_v[i//2][j//2] == 4:
                        tab[i][j] = 4
                #Mur horizontal
                elif i%2 == 0 and j%2 ==1:
                    if self.matrice_h[i//2][j//2]:
                        tab[i][j] = 1
                    else:
                        tab[i][j] = 0
    
        return tab

    def voisins_inconnus(self):
        """
        Renvoie la liste des voisins inconnus de la case (self.x, self.y)
        Entrée : Aucune
        Sortie : (list)
        """
        rep = []
        #HAUT
        if self.y != 0:
            if self.matrice_h[self.y][self.x] == 0 and self.deja_visite[self.y-1][self.x] == 0:
                rep.append((self.x,self.y-1))
        
        #BAS
        if self.y != self.lignes - 1:
            if self.matrice_h[self.y+1][self.x] == 0 and self.deja_visite[self.y+1][self.x] == 0:
                rep.append((self.x,self.y+1))
        
        #GAUCHE
        if self.x != 0:
            if self.matrice_v[self.y][self.x] == 0 and self.deja_visite[self.y][self.x-1] == 0:
                rep.append((self.x-1,self.y))
        
        #DROITE
        if self.x != self.colonnes - 1:
            if self.matrice_v[self.y][self.x+1] == 0 and self.deja_visite[self.y][self.x+1] == 0:
                rep.append((self.x+1,self.y))

        return rep

    def etendre_val(self, depart):
        """
        Etant la valeur de la case depart à toutes les cases qui lui sont accessible
        Entrée : depart (tuple au format (x (int), y (int)) )
        Sortie : None
        """
        parcours = True
        val = self.labyrinthe[depart[1]][depart[0]]
        self.x = depart[0]
        self.y = depart[1]
        self.exploration = [depart]
        self.deja_visite = [[0 for j in range(self.colonnes)] for i in range(self.lignes)]
        defile = 0
        while parcours:
            self.x = depart[0]
            self.y = depart[1]
            self.deja_visite[self.y][self.x] = 1
            voisins = self.voisins_inconnus()
            if len(voisins) == 0 and len(self.exploration) != 0:
                depart = self.exploration.pop()
                defile = 1
            elif len(voisins) != 0:
                if defile and len(voisins) > 1:
                    self.exploration.append((self.x,self.y))
                    defile=0
                self.exploration.append(voisins[0])
                v = voisins[0]
                depart = (v[0], v[1])
            else:
                parcours = 0
            self.labyrinthe[depart[1]][depart[0]] = val
            
        parcours = False

    def fusion_aleatoire(self):
        """
        Algorithme de la fusion aléatoire permettant de générer un Labyrinthe parfait à partir de la situation de départ générée par __init__
        Entrée : Aucune
        Sortie : None
        """
        
        murs_a_ouvrir = self.colonnes*self.lignes-1
        nb_iter = murs_a_ouvrir**2

        #Sélection du mur à ouvrir
        while murs_a_ouvrir and nb_iter:
            choix       = randint(0,len(self.labyrinthe[0])-1), randint(0,len(self.labyrinthe)-1)
            x,y         = choix
            possibilite = []
            #HAUT
            
            if y > 1:
                if self.matrice_h[y][x] == 1 and self.labyrinthe[y][x] != self.labyrinthe[y-1][x]:
                    possibilite.append((x, y))
                else:
                    possibilite.append(None)
            else:
                possibilite.append(None)
            
            
            #BAS
            
            if y != self.lignes - 1:
                if self.matrice_h[y+1][x] == 1 and self.labyrinthe[y][x] != self.labyrinthe[y+1][x]:
                    possibilite.append((x,y+1))
                else:
                    possibilite.append(None)
            else:
                possibilite.append(None)
            
            #GAUCHE
            
            if x > 1:
                if self.matrice_v[y][x] == 1 and self.labyrinthe[y][x] != self.labyrinthe[y][x-1]:
                    possibilite.append((x, y))
                    
                else:
                    possibilite.append(None)
            else:
                possibilite.append(None)

            #DROITE
            if x != self.colonnes - 1:
                if self.matrice_v[y][x+1] == 1 and self.labyrinthe[y][x] != self.labyrinthe[y][x+1]:
                    possibilite.append((x+1,y))
                else:
                    possibilite.append(None)
            else:
                possibilite.append(None)

            if possibilite != [None,None,None,None]:
                choix_index = randint(0,3)

                while possibilite[choix_index] == None:
                    choix_index = randint(0,3)
                choix_mur = possibilite[choix_index]
                murs_a_ouvrir -=1
                if choix_index <= 1:
                    self.matrice_h[choix_mur[1]][choix_mur[0]] = 0
                    
                else:
                    self.matrice_v[choix_mur[1]][choix_mur[0]] = 0
                    

                
                self.etendre_val(choix)
            nb_iter-=1
        if not nb_iter and murs_a_ouvrir:
            raise RuntimeError("Timed out, la génération a pris trop de temps")
        else:
            print("Fin normale")
    def gen_issues(self):
        """
        Génère la sortie du labyrinthe
        Entrée : Aucune
        Sortie : None
        """
        #Sortie
        possible = []
        for i in range(len(self.matrice_v)):
            for j in range(len(self.matrice_v[0])):
                if j == len(self.matrice_v[0])-1 :
                    possible.append((j,i))
        choix = choice(possible)
        self.matrice_v[choix[1]][choix[0]] = 4 #4 -> Sortie



































        
        
