from tkinter import *
import random
import time


WIDTH = 1600
HEIGHT = 1000

tk = Tk()
tk.attributes('-fullscreen', 1)
Button(tk, text="Quit", command=root.destroy).pack()
canvas = Canvas(tk)


tk.title ("Drawing")
canvas.pack()

ball = canvas.create_oval(10, 10, 60, 60, fill="yellow")

xspeed = 1
yspeed = 1

while True :
	canvas.move(ball, xspeed, yspeed)
	pos = canvas.coords(ball)
	if pos[3] >= HEIGHT or pos[1] <= 0:
		yspeed = -yspeed
	if pos[2] >= WIDTH or pos[0] <= 0:
		xspeed = - xspeed
	tk.update()
	time.sleep(0.01)

tk.mainloop()



 

