# -*- coding: utf8 -*-



import tkinter, Tkconstants, tkFileDialog, tkMessageBox
import tkinter as tk
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

from PIL import Image
class CDPBaseVisualisation:

	def __init__(self,refInterface):
		pass
	def clear(self):
		pass

	def Show_gauche(self,x,y,col,r):
		pass

	def Show_droit(self,x,y,col,r):
		pass

	def affiche_image(self, fichier, pos):
		pass 

	def validation_calibration(self,PosDroit,PosGauche):
		pass

	def effacer_mouvement(self):
		pass

	def effacer_image(self):
		pass
	def Show_gaze(self,x,y):
		pass
	def effacer_gaze(self):
		pass
	def blackscreen(self):
		pass
	def Show_point(self,x,y,r,col):
		pass
	def write_time(self,Tp,Tr,Tv,Txp,Nbrec,TinterTrial,tvtot,trtot,dist,tmaxcons):		
		pass
	def effacer_text(self):
		pass
	def effacer_point(self):
		pass

	def draw_AOI_fix(self):
		pass
	
class CDPVisualisation(CDPBaseVisualisation):
	def __init__(self,refInterface,disp):
		self.listImg = []
		self.refInterface = refInterface	
		self.disp = disp
		self.fig = 0
		self.factor = 2 # facteur de division de la taille de la fentre par rapport a l ecran experience
		self.tk = tk.Toplevel() ## fenetre tktiner fille
		self.tk.protocol("WM_DELETE_WINDOW", self.delete)
		self.tk.title ("Fenetre de suivi") # nom de la fenetre tkinter fille
		self.fig = Figure(figsize=[9.6,5.4],dpi=100,facecolor='black') # ajout du un objet figure sur la fenetre tkinter

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.tk)  # A tk.DrawingArea.
		self.canvas.get_tk_widget().pack(fill='both', expand=1)

		self.Oeilgauche = self.canvas.get_tk_widget().create_oval(-10, -10, -10, -10, fill='white')
		self.Oeildroit = self.canvas.get_tk_widget().create_oval(-10, -10, -10, -10, fill='white')
		self.photoImg = self.canvas.get_tk_widget().create_oval(-10, -10, -10, -10, fill='white')
		self.Pos = self.canvas.get_tk_widget().create_oval(-10, -10, -10, -10, fill='white')
		self.Point = self.canvas.get_tk_widget().create_oval(-10, -10, -10, -10, fill='white')
		self.canvas.show()

	def Show_gauche(self,x,y,col,r):
		'Affiche un point sur la fenetre de visualisation aux coroonnes donnees de la couleur voulu et du rayon voulu'
		x1 = (int(x) / self.factor) - r
		y1 = (int(y) / self.factor) - r
		x2 = (int(x) / self.factor) + r
		y2 = (int(y) / self.factor) + r
		self.Oeilgauche = self.canvas.get_tk_widget().create_oval(x1, y1, x2, y2, fill=col)

	def Show_droit(self,x,y,col,r):
		x1 = (int(x) / self.factor) - r
		y1 = (int(y) / self.factor) - r
		x2 = (int(x) / self.factor) + r
		y2 = (int(y) / self.factor) + r
		self.Oeildroit = self.canvas.get_tk_widget().create_oval(x1, y1, x2, y2, fill=col)

	def effacer_mouvement(self):
		self.canvas.get_tk_widget().delete(self.Oeildroit)
		self.canvas.get_tk_widget().delete(self.Oeilgauche)

	def effacer_image(self):
		self.canvas.get_tk_widget().delete(self.photo)

	def VisuShow(self):
		self.canvas.show()

	def Show_gaze(self,x,y):
		x1 = (int(x) / self.factor) - 3
		y1 = (int(y) / self.factor) - 3
		x2 = (int(x) / self.factor) + 3
		y2 = (int(y) / self.factor) + 3
		self.Pos = self.canvas.get_tk_widget().create_oval(x1, y1, x2, y2, fill='yellow')
		self.canvas.show()

	def effacer_gaze(self):

		self.canvas.get_tk_widget().delete(self.Pos)
	
	
	def write_time(self,Tp,Tr,Tv,Txp,Nbrec,TinterTrial,tvtot,trtot,dist,tmaxcons):

		self.tp =self.canvas.get_tk_widget().create_text(0,0,text="Tp = " + str(Tp) + ' ms',fill='white',anchor=tk.NW,font=("Arial", 15))
		self.tr = self.canvas.get_tk_widget().create_text(0,30,text="Tr = " + str(Tr) + ' ms',fill='red',anchor=tk.NW,font=("Arial", 15))
		self.tv = self.canvas.get_tk_widget().create_text(0,60,text="Tv = " + str (Tv) + ' ms',fill='green',anchor=tk.NW,font=("Arial", 15))
		self.tptv = self.canvas.get_tk_widget().create_text(0,90,text="Tv + Tr = " + str(Tr+Tv) + ' ms',fill='white',anchor=tk.NW,font=("Arial", 15))

		self.txp = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/self.factor,0,text="Txp = " + str(Txp) + ' s',fill='white',anchor=tk.NE,font=("Arial", 15))
		self.rec = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/self.factor,30,text="Recompense = " + str(Nbrec) ,fill='white',anchor=tk.NE,font=("Arial", 15))
		self.tvtot = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/self.factor,60,text="tvtot = " + str(tvtot) +' ms',fill='green',anchor=tk.NE,font=("Arial", 15))
		self.trtot = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/self.factor,90,text="trtot = " + str(trtot) +' ms',fill='red',anchor=tk.NE,font=("Arial", 15))
		self.tmaxcons = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/self.factor,120,text="tmax consécutif = " + str(tmaxcons) +' ms',fill='white',anchor=tk.NE,font=("Arial", 15))

		self.dist = self.canvas.get_tk_widget().create_text(self.disp.dispsize[0]/(self.factor*2),self.disp.dispsize[1]/self.factor,text="Distance à l'écran" + ' ' + str(dist) +' cm',fill='white',anchor=tk.S,font=("Arial", 15))
		self.tit = self.canvas.get_tk_widget().create_text(self.disp .dispsize[0]/self.factor,self.disp.dispsize[1]/self.factor,text="Temps InterTrial total = " + str(TinterTrial) +' ms',fill='white',anchor=tk.SE,font=("Arial", 15))

	def draw_AOI_fix(self):

		self.aoi = self.canvas.get_tk_widget().create_rectangle(480-40,351-40,480+40,351+40,outline='red')
		self.fixation = self.canvas.get_tk_widget().create_oval(480-15,351-15,480+15,351+15,fill='white')
		self.canvas.show()

	def effacer_text(self):

		self.canvas.get_tk_widget().delete(self.tp)
		self.canvas.get_tk_widget().delete(self.tr)
		self.canvas.get_tk_widget().delete(self.tv)
		self.canvas.get_tk_widget().delete(self.tptv)
		self.canvas.get_tk_widget().delete(self.txp)
		self.canvas.get_tk_widget().delete(self.rec)
		self.canvas.get_tk_widget().delete(self.tvtot)
		self.canvas.get_tk_widget().delete(self.trtot)
		self.canvas.get_tk_widget().delete(self.dist)
		self.canvas.get_tk_widget().delete(self.tmaxcons)
		self.canvas.get_tk_widget().delete(self.tit)



	def affiche_image(self, fichier, pos):


		' Ajout d une image dans sur l objet figure'

		img = Image.open(fichier)
		Newimg = img.resize((int(img.width / self.factor),int(img.height/self.factor)), Image.ANTIALIAS)
		self.photoImg  = ImageTk.PhotoImage(Newimg)
		self.photo = self.canvas.get_tk_widget().create_image(int(pos[0]/self.factor),int(pos[1]/self.factor), image=self.photoImg)
		self.canvas.show()

	def Show_point(self,x,y,r,col):

		x1 = (int(x) / self.factor) - r
		y1 = (int(y) / self.factor) - r
		x2 = (int(x) / self.factor) + r
		y2 = (int(y) / self.factor) + r
		self.Point = self.canvas.get_tk_widget().create_oval(x1, y1, x2, y2, fill=col)
		self.canvas.show()

	def effacer_point(self):

		self.canvas.get_tk_widget().delete(self.Point)
		self.canvas.show()

	def blackscreen(self):

		self.canvas.get_tk_widget().delete('all')
		self.canvas.get_tk_widget().create_rectangle(0, 0, 960, 540, fill='black')
		self.canvas.show()


	def delete(self):

		'permet la destruction de la fenetre de visualisation'
		self.tk.destroy()
		self.refInterface.CDPDeleteVisualisation()


	def clear(self):
		'permet d effacer ce qu il y a sur la fenetre de visualisation'
		self.tk.destroy()
		self.tk = tk.Toplevel(width = self.disp.dispsize[0]/self.factor, height=self.disp.dispsize[1]/self.factor,bg='black')
		self.tk.protocol("WM_DELETE_WINDOW", self.delete)
		self.tk.title ("Fenetre de suivi")
		self.fig = Figure(figsize=[9.6,5.4],dpi=100,facecolor='black')
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.tk)  # A tk.DrawingArea.
		self.canvas.get_tk_widget().pack(fill = 'both')
		

	










