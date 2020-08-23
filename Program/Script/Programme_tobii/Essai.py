import tkinter as tk
import random
import time


root = tk.Tk()
root.attributes('-fullscreen',True )   ### fond gris$
can = tk.Canvas( root,bg='grey',highlightthickness=0  ) #### enlever barre outil de canvas 
tk.Button(can, text="Quit", command=root.destroy).pack() ## ajouter un bouton quit pour quitter l interface
can.pack( fill='both',expand=1 )
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

x1 = WIDTH / 2 -15 ## cercle de rayon 15 et centre de coorodonnes(W/2,H/2)
y1 = HEIGHT /2 -15
x2 = WIDTH / 2 +15
y2 = HEIGHT /2 +15

can.pack()

ball = can.create_oval(x1, y1, x2, y2, fill="yellow") ### creation d un cercle jaune 

xspeed = 1
yspeed = 1


while True :
	can.move(ball, xspeed, yspeed)
	pos = can.coords(ball)
	if pos[3] >= HEIGHT or pos[1] <= 0:
		yspeed = -yspeed
	if pos[2] >= WIDTH or pos[0] <= 0:
		xspeed = - xspeed
	root.update()
	time.sleep(0.01)

root.mainloop()

