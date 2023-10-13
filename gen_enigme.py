"""
Module permettant de génèrer et d'afficher une énigme (nombre décimal à convertir en binaire)
"""
from tkinter import *
from tkinter import ttk
from random import randint


str_bin = ""
reussi = False
label_txt = ""

def binaire():
    """
    Génère un nombre binanire alétaoire entre 20 et 500
    Entrée : Aucune
    Sortie : (tuple, un nombre (int) et son équivalent en binaire (str))
    """

    nb = randint(20,500)
    return nb,bin(nb)[2:]

    
def add(nb,win,text,frame):
    """
    Mets à jour l'interface de l'utilisateur
    Entrée : nb (str),win (tkinter.Tk),text (str),frame (tkinter.Frame), str_bin (str, global), label_txt (tkinter.Label, global)
    Sortie : None
    """
    global str_bin,label_txt
    str_bin += nb
    text = str_bin
    if label_txt is not None:
        label_txt.destroy()
    label_txt = ttk.Label(frame,text=text).grid(column=0,row=1)
    win.update()

def valider(rep,win):
    """
    Valide la réponse du joueur et détruit l'interface de l'énigme
    Entrée : rep (str), win (tkinter.Tk), str_bin (str, global), reussi (bool, global)
    Sortie : None
    """
    global str_bin,reussi
    if str(rep) == str(str_bin):
        reussi = True
    str_bin = ""
    win.quit()
    win.destroy()
    
    
def enigme():
    """
    Génère et affiche l'interface de l'énigme
    Entrée : str_bin (str, global), reussi (bool, global), label_txt (tkinter.Label, global)
    Sortie : (bool)
    """
    global str_bin,reussi,label_txt
    quest,rep = binaire()

    window = Tk()
    window.title("Enigme")
    frm = ttk.Frame(window,padding=10)
    frm.grid()
    window.geometry("220x100")
    #text
    #text = StringVar()
    #text.set(str_bin)
    text = str_bin
    #box
    ttk.Label(frm,text=str(quest) + " en bainaire ?").grid(column=0,row=0)
    #label_txt = ttk.Label(frm,textvariable=text)
    #label_txt.grid(column=0,row=1)
    label_txt = ttk.Label(frm,text=text)
    label_txt.grid(column=0,row=1)
    ttk.Button(frm, text="1", command=lambda:add("1",window,text,frm)).grid(column=1, row=0)
    ttk.Button(frm, text="0", command=lambda:add("0",window,text,frm)).grid(column=1, row=1)
    ttk.Button(frm, text="Valider", command=lambda:valider(rep,window)).grid(column=0, row=2)
    #attente du destroy()
    window.mainloop()
    if reussi:
        return True
    return False

