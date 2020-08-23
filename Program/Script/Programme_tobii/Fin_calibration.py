import time
import tobii_research as tr
import tkinter as tk
import random
import os
import sys


### Fonctions ####


def Conversionx (Xcs):  ## permet de convertir ADCS x en pixel
	Xpix = Xcs * 1920
	return (Xpix)
def Conversiony (Ycs):## permet de convertir ADCS y en pixel
	Ypix = Ycs * 1080 
	return (Ypix)

def execute(eyetracker):
	return(gaze_data(eyetracker))
 
 
def gaze_data_callback(gaze_data):
	global global_gaze_data
	global_gaze_data = gaze_data
 
 
def gaze_data(eyetracker):
	global global_gaze_data
 
	print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
	eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
 	
   # Wait while some gaze data is collected.
	time.sleep(2)
 	print(global_gaze_data)
	OeilD = global_gaze_data.get("right_gaze_point_on_display_area") #coordonnee oeil gauche display area
	OeilG = global_gaze_data.get("left_gaze_point_on_display_area") ## coordonnee oeil droit display area

	eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
	print("Unsubscribed from gaze data.")
 
	print("Last received gaze package:")
	return (OeilD, OeilG)


### run ###
# affichage ecran canva

root = tk.Tk()
root.attributes('-fullscreen',True )   ### fond gris$
can = tk.Canvas( root,bg='grey',highlightthickness=0  ) #### enlever barre outil de canvas 
can.pack( fill='both',expand=1 )



# Connection eyetracker

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]

points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]


List_Pos = []
for point in points_to_calibrate:
	print "Show a point on screen at {0}.".format(point)

	x1 = Conversionx(point[0]) - 15
	y1 = Conversiony(point[1]) - 15 
	x2 = Conversionx(point[0]) + 15
	y2 = Conversiony(point[1]) + 15
	ball = can.create_oval(x1, y1, x2, y2, fill="yellow") ### creation d un cercle jaune 
	root.update()
	List_Pos +=[execute(eyetracker)]


print(len(List_Pos))

for i in range (len(List_Pos)):   #creation oeil droit sur ecran 
	print(i)
	x1 = Conversionx(List_Pos[i][0][0]) - 7
	y1 = Conversionx(List_Pos[i][0][1]) - 7
	x2 = Conversionx(List_Pos[i][0][0]) + 7
	y2 = Conversionx(List_Pos[i][0][1]) + 7
	print((x1,y1,x2,y2))
	ball = can.create_oval(x1, y1, x2, y2, fill="green") ### creation d un cercle green 
	root.update()

for i in range (len(List_Pos)):   #creation oeil gauche sur ecran 
	x1 = Conversionx(List_Pos[i][1][0]) - 7
	y1 = Conversionx(List_Pos[i][1][1]) - 7
	x2 = Conversionx(List_Pos[i][1][0]) + 7
	y2 = Conversionx(List_Pos[i][1][1]) + 7
	ball = can.create_oval(x1, y1, x2, y2, fill="red") ### creation d un cercle green 
	root.update()


root.mainloop()




