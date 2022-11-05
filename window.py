from tkinter import *
#from tkmacosx import * #non funziona su macOS 13
from turtle import color

single = FALSE
multiplayer = FALSE

def choose_algorithm():
        for widget in root.winfo_children():
                widget.destroy()
        #scelgo l'algoritmo con cui giocare
        w3 = Label(root, text ='Which kind of algorithm do you want to test?', fg = "white" ,bg = "black",font = "50").pack(pady=35) 
        mb3 = Menubutton(root, text="Choose here")
        mb3.menu = Menu(mb3)
        mb3["menu"] = mb3.menu
        mb3.menu.add_command(label="Alg1", command= lambda: print("alg1"))#devo settare variabile per scegliere alg
        mb3.menu.add_command(label="Alg2", command= lambda: print("alg2"))#idem
        mb3.pack()
       


def VarSingle():
        #fai qualcosa sul dic
        single = TRUE
        multiplayer = FALSE
        for widget in root.winfo_children():
                widget.destroy()
        #scelgo se giocare da solo o far giocare il bot
        w2 = Label(root, text ='Which kind of player do you want?', fg = "white" ,bg = "black",font = "50").pack(pady=35) 
        mb2 = Menubutton(root, text="Choose here")
        mb2.menu = Menu(mb2)
        mb2["menu"] = mb2.menu
        mb2.menu.add_command(label="Bot player", command= choose_algorithm)
        mb2.menu.add_command(label="Play by yourself", command= lambda: print("ciao gioco da solo"))#faccio qualcosa per giocare da solo
        mb2.pack()


def VarMultiplayer():
        #fai qualcosa sul dic
        multiplayer = TRUE
        single = FALSE
        for widget in root.winfo_children():
                widget.destroy()
        #creo nuovo menù per selezionare num bot
        #non ho implementato la scelta due giocatori umani
        w1 = Label(root, text ='How many Bot?', fg = "white" ,bg = "black",font = "50").pack(pady=35) 
        mb1 = Menubutton(root, text="Choose here")
        mb1.menu = Menu(mb1)
        mb1["menu"] = mb1.menu
        mb1.menu.add_command(label="1", command= lambda: print("gioco contro il bot"))#fare qualcosa per giocare contro bot
        mb1.menu.add_command(label="2", command= lambda: print("giocono solo i bot"))#fare qualcosa per giocare solo bot
        mb1.pack()

root = Tk(className='Snake')
width = 600 # Width 
height = 300 # Height
 
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height)
 
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.configure(bg='black')

w = Label(root, text ='Single player or multiplayer?', fg = "white" ,bg= "black",font = "60") 
w.pack(pady=35)

mb = Menubutton(root, text="Choose here")
mb.menu = Menu(mb)
mb["menu"] = mb.menu
mb.menu.add_command(label="Single player", command = VarSingle)
mb.menu.add_command(label="Multiplayer", command = VarMultiplayer)
mb.pack()

root.mainloop()