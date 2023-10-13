import tkinter
import itertools


colors = ["red", "green", "blue", "yellow"]

def show_window(result):
    if result == "win":
        text = "Vous avez gagné"
    elif result == "loose":
        text = "Vous avez perdu"
    else:
        raise ValueError("Invalid result value")

    window = tkinter.Tk()
    window.title("Fenêtre aux couleurs changeantes")

    global label
    label = tkinter.Label(window, text=text, font=("Arial", 32))
    label.pack()


    def change_color():
        global label
        global colors

        color = next(colors_cycle)

        label.config(fg=color)

        window.after(100, change_color)

    colors_cycle = itertools.cycle(colors)
    change_color()
    window.mainloop()

