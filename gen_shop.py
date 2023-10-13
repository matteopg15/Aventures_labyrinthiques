"""
Module permettant de générer et utiliser le magasin. Le magasin permet avec des pièces d'acheter des déplacements 
et des intérêts.
"""
from tkinter import *
from tkinter import messagebox


# Initialiser les variables globales de pièces et de déplacements/intérêts

coins,deplacements,interests = 0,0,0

purchases = (0, 0, 0)
# Fonction pour mettre à jour l'affichage des informations
def update_display():
    """
    Mets à jour l'affichage du magasin
    Entrée : coin_label (tkinter.Label, global), deplacement_label (tkinter.Label, global), interest_label (tkinter.Label, global)
    Sortie : None
    """
    global coin_label
    global deplacement_label
    global interest_label
    coin_label.config(text=f"Pièces : {coins}")
    deplacement_label.config(text=f"Déplacements : {deplacements}")
    interest_label.config(text=f"Intérêts : {interests}")

# Fonction pour acheter des déplacements
def buy_deplacements(tout):
    """
    Permet l'achat de déplacement contre des pièces
    Entrée : tout (bool), coins (int, global), deplacements (int, global)
    Sortie : None
    """
    global coins, deplacements
    # Vérifier s'il y a assez d'argent
    if coins < 1:
        error_label.config(text="Vous n'avez pas assez de pièces !", fg="red")
    else:
        # Mettre à jour le nombre de pièces et de déplacements
        if tout:
            #Achète le maximum possible avec l'argent possédé par le joueur
            deplacements += 1*(coins//1) #Modifier le dénominateur si on change le prix
            coins -= coins//1            #Modifier le dénominateur si on change le prix
            
        else:
            coins -= 1
            deplacements += 1
        update_display()

# Fonction pour acheter des intérêts
def buy_interests(tout):
    """
    Permet l'achat d'intérêts contre des pièces
    Entrée : tout (bool), coins (int, global), interests (int, global)
    Sortie : None
    """
    global coins, interests

    # Vérifier s'il y a assez d'argent
    if coins < 1:
        error_label.config(text="Vous n'avez pas assez de pièces !", fg="red")
    else:
        # Mettre à jour le nombre de pièces et d'intérêts
        if tout:
            #Achète le maximum possible avec l'argent possédé par le joueur
            interests += 1*(coins//1) #Modifier le dénominateur si on change le prix
            coins -= coins//1         #Modifier le dénominateur si on change le prix
            
        else:
            coins -= 1
            interests += 1
 
        update_display()

# Fonction pour valider les achats et afficher le nombre de déplacements et d'intérêts achetés
def validate_purchases():
    """
    Affiche le résultat des achats du joueur
    Entrée : coins (int, global), interests (int, global), deplacements (int, global)
    Sortie : None
    """
    global coins,interests,deplacements
    
    error_label.config(text="")
    messagebox.showinfo("Achats validés", f"Vous avez acheté {deplacements} déplacements et {interests} intérêts ! Vous avez {coins} pièces restantes.")
    update_display()


# Fonction pour afficher la fenêtre
def show_window(moula,moves,trucbanque):
    """
    Génère et affiche le magasin
    Entrée : moula (int, nombre de pièces du joueur), trucbanque (int, nombre d'intérêts du joueur), moves (int, nombre de déplacements du joueur)
    coins (int, global) ,deplacements (int, global), interests (int, global), window (tkinter.Tk, global),button_validate (tkinter.Button, global),
    button_interests (tkinter.Button, global),button_deplacements (tkinter.Button, global),error_label (tkinter.Label, global),
    coin_label (tkinter.Label, global),interest_label (tkinter.Label, global),deplacement_label (tkinter.Label, global)
    Sortie : None
    """
    global coins,deplacements,interests
    global window,button_validate,button_interests,button_deplacements,error_label
    global coin_label,interest_label,deplacement_label
    coins,deplacements,interests = moula,moves,trucbanque

  

    # Créer la fenêtre principale
    window = Tk()
    window.title("Acheter des déplacements et des intérêts")

    # Créer un label pour afficher le nombre de pièces
    coin_label = Label(window, text=f"Pièces : {coins}")
    coin_label.pack()

    # Créer un label pour afficher le nombre de déplacements
    deplacement_label = Label(window, text=f"Déplacements : {deplacements}")
    deplacement_label.pack()

    # Créer un label pour afficher le nombre d'intérêts
    interest_label = Label(window, text=f"Intérêts : {interests}")
    interest_label.pack()

    # Créer un label pour afficher les messages d'erreur
    error_label = Label(window, text="", fg="red")
    error_label.pack()

    # Créer un bouton pour acheter un déplacements
    #button_deplacements = Button(window, text="Acheter un déplacement", command=buy_deplacements)
    button_deplacements = Button(window, text="Acheter un déplacement")
    button_deplacements.pack()
    button_deplacements.bind("<Button-1>", lambda x : buy_deplacements(False))
    button_deplacements.bind("<Button-3>", lambda x : buy_deplacements(True))


    # Créer un bouton pour acheter un intérêt
    #button_interests = Button(window, text="Acheter un intérêt", command=buy_interests)
    button_interests = Button(window, text="Acheter un intérêt")
    button_interests.pack()
    button_interests.bind("<Button-1>", lambda x : buy_interests(False))
    button_interests.bind("<Button-3>", lambda x : buy_interests(True))


    # Créer un bouton pour valider les achats
    button_validate = Button(window, text="Valider", command=lambda: (validate_purchases(), update_purchases()))
    button_validate.pack()

    # Afficher la fenêtre
    window.mainloop()


# Fonction de rappel pour mettre à jour la variable purchases lorsque le bouton est cliqué
def update_purchases():
    """
    Enregistre le bilan des achats du joueur et ferme le magasin
    Entrée : purchases (tuple, global), window (tkinter.Tk, global)
    Sortie : None
    """
    global purchases,window
    purchases = (coins, deplacements, interests)
    window.quit()
    window.destroy()