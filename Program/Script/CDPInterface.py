# -*- coding: utf8 -*-
''' Gestion de l'interface de contrôle des expériences de l'eye tracker'''
# Gestion des expériences par création de méthodes virtuelles complétées dans le fichier CDP experience


__authors__ = ("Mathieu Legrand") 
__contact__ = ("mathieu.legrand78@gmail .com")
__version__ = "1.0.1"
__copyright__ = "copyleft" 
__date__ = "28/08/2020"


import tkinter as tk
import os
import configparser
from functools import partial
import tkinter.messagebox
from matplotlib import pyplot
from CDPConfiguration import CDPConfiguration
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import threading
import json

__metaclass__ = type

class CDPApplication():
    def addButtonCal(self, indice, col, row):

        self.boutons[indice] = tk.Button(self.padFrame, text=indice, command=partial(self.cal_point, indice), height = 2, width = 2)
        self.boutons[indice].grid(column=col, row=row, pady = 3, padx = 3)     
         # Ajout des raccourcis clavier 
        self.root.bind("<KP_"+str(indice)+">", self.event_num_func_cal)

    def addButton(self,indice,col,row):
        self.boutons[indice] = tk.Button(self.padFrame, text=indice, command=partial(self.val_point, indice), height = 2, width = 2)
        self.boutons[indice].grid(column=col, row=row, pady = 3, padx = 3)     
         # Ajout des raccourcis clavier 
        self.root.bind("<KP_"+str(indice)+">", self.event_num_func)




    def unbind(self,nombre):
	    ''' Supprime les raccourcis clavier sur le pavé numérique'''

	    for i in range (nombre):
		    self.root.unbind("<KP_"+str(i+1)+">")





    def event_num_func(self, event):
        self.CDPSendValidationPoint( int(event.char ))
        self.currentButton = self.boutons[int(event.char )]
        self.currentButton.configure(bg='green')
        self.ListeOeil += [self.CDPeyeData( int(event.char ))]
        self.effacer()

    def val_point(self,event):
        self.CDPSendValidationPoint(event)
        self.currentButton = self.boutons[event]
        self.currentButton.configure(bg='green')
        self.ListeOeil += [self.CDPeyeData(event)]
        self.effacer()




    def cal_point(self,event):
        x = threading.Thread(target=self.sendPoint, args=(event,))
        x.start()
        self.validatePoint(event)  

    def event_num_func_cal(self, event):
        x = threading.Thread(target=self.sendPoint, args=(int(event.char ) ,))
        x.start()
        self.validatePoint(int(event.char ) )  

    def event_enter_func(self, event):
        self.validatePoint()              




    def __init__(self,  title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry('450x300')

        
        # MENU
        menubar = tk.Menu(self.root )
        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Effacer écran", command=self.effacer)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="Charger une caibration",  command=self.loadCalibration)
        menu2.add_command(label="Lancer une calibration",  command=self.calibrate)
        menu2.add_command(label="Valider la calibration",  command=self.ValidationCalibration)
        menu2.add_separator()

        menu2.add_command(label="Visualiser la calibration",  command=self.CDPVisualisationCalibration)
        menubar.add_cascade(label="Calibration", menu=menu2)

        menu3 = tk.Menu(menubar, tearoff=0)
        menu3.add_command(label="Où est Charlie ?",  command=self.Nictation)
        menu3.add_separator()

        menu3.add_command(label="Apprentissage Position",  command=self.ApprentissagePos)

        menu3.add_command(label="Fixation Point",  command=self.InterfacefixationPoint)
        #menu3.add_command(label="SGVS",  command=self.SGVS)
        #menu3.add_command(label="Fixation Visage",  command=self.FixVisage)
        menu3.add_command(label="Exploration Visages",  command=self.InterfaceExplorationVisage)
        #menu3.add_command(label="Afficher GIF",  command=self.CDPDispGIF)


        menubar.add_cascade(label="Experiences", menu=menu3)
        
        menu4 = tk.Menu(menubar, tearoff=0)
        menu4.add_command(label="Afficher",  command=self.AffichageVis)
        menubar.add_cascade(label="Visualisation", menu=menu4)

        menu5 = tk.Menu(menubar, tearoff=0)
        menu5.add_command(label="Connecter",  command=self.CDPInitialisation)
        menu5.add_separator()

        menu5.add_command(label="Déconnecter",  command=self.CDPDisconnect)
        menubar.add_cascade(label="EyeTracker", menu=menu5)





        self.root.config(menu=menubar)

        # Chargement de la configuration
        # L'objet Config gère tous les accés aux noms de ficheirs et dossiers
        configFilename = os.path.dirname(os.path.abspath(__file__)) + "/" +'CDPInterface.ini'
        self.Config= CDPConfiguration(configFilename)
        
        self.tracker = 0
        
        try:
            with open(self.Config.getScriptDirname('ListeIndividus.json') , "r") as fichier:

                data = json.load(fichier)            
                self.ListeInd = data["ListeInd"] 
                
        except IOError :
            print ("fichier %s introuvable", filename )   
        self.root.mainloop()
        
    ''' Fonctions de calibrations '''


    
    def loadCalibration(self):
        self.CDPLoadCalibration()

    def calibrate(self):

        self.padFrame = tk.Frame(self.root)
        self.boutons = 10*[0]
        self.addButtonCal ( 7,  3,  1)
        self.addButtonCal ( 4,  2,  2)
        self.addButtonCal ( 1,  1,  3)
        self.addButtonCal ( 8, 5,  1)
        self.addButtonCal ( 5,  4,  2)
        self.addButtonCal ( 2,  3,  3)
        self.addButtonCal ( 6,  1,  1)
        self.addButtonCal ( 3,  5,  3)   
 
        #Raccourci "enter"

        self.root.bind("<KP_Enter>", self.event_enter_func) 
	        

        tk.Button(self.padFrame, text="Sauvegarde", command=self.applyCalibration).grid(column=1, row=6, columnspan=6, pady = 3, padx = 3, sticky='nesw')
        tk.Button(self.padFrame, text="Quitter la Calibration", command=self.LeaveCalibration).grid(column=1, row=7, columnspan=6, pady = 3, padx = 3, sticky='nesw')
        self.padFrame.grid_forget()
        self.CDPinitCalibration()
        self.showPad()

    def LeaveCalibration(self):
        self.padFrame.destroy()
        self.unbind(9)

        self.CDPLeaveCalibration()

    def applyCalibration(self):

        self.hidePad()
        self.ListeCal = self.CDPApplyCalibration()
        self.padFrame.destroy()
        self.unbind(9)
        self.grapheCalibration()

        Confirm = tkinter.messagebox.askyesno('Confirmation', 'La calibration convient-elle ?')
        if not Confirm :
            self.tkplot.destroy()
            self.calibrate()
        else : 
            self.tkplot.destroy()
            self.CDPEndCalibration(self.ListeCal)

    def grapheCalibration(self):
        self.tkplot = tk.Toplevel(self.root)
        self.tkplot.title ("Représentation Calibration") # nom de la fenetre tkinter fille
        self.fig = Figure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tkplot)  
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        ax = self.fig.add_subplot(111)
        ax.set_ylim(0,1080)
        ax.invert_yaxis()
        ax.set_xlim(0,1920)
        
        col = ['black','grey','yellow','green','pink','red','blue','purple','orange']
        cpt = 0

        OldXref = self.ListeCal[0][0]
        OldYref = self.ListeCal[0][1]
        ListeXref = [OldXref]
        ListeYref = [OldYref]
        ListeTest = [(OldXref,OldYref)]
        for Pos in self.ListeCal:
            Xref = Pos[0]
            Yref = Pos[1]
            if (Xref,Yref) not in ListeTest:
                ListeXref += [Xref]
                ListeYref += [Yref]
                ListeTest += [(Xref,Yref)]
                cpt +=1

            if Pos[2] != 0 and Pos[3] != 0:
                ax.scatter(Pos[2],Pos[3], c = col[cpt],marker='x',s=8)
            if Pos[4] != 0 and Pos[5] != 0:
                ax.scatter(Pos[4],Pos[5],c=col[cpt],marker='s',s=8)
        for i in range (len (ListeXref)):
            ax.scatter(ListeXref[i],ListeYref[i],c=col[i],s=80)

        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.show()	

    def ValidationCalibration(self):
        
        self.ListeOeil= []
        self.padFrame = tk.Frame(self.root)
        self.boutons = 10*[0]
        self.addButton ( 7,  3,  1)
        self.addButton ( 4,  2,  2)
        self.addButton ( 1,  1,  3)
        self.addButton ( 8,  5,  1)
        self.addButton ( 5,  4,  2)
        self.addButton ( 2,  3,  3)
        self.addButton ( 6,  1,  1)
        self.addButton ( 3,  5,  3)   

        tk.Button(self.padFrame, text="Valider", command=lambda:[self.AfficherGain(),self.destroyPad()]).grid(column=1, row=6, columnspan=6, pady = 3, padx = 3, sticky='nesw')
        tk.Button(self.padFrame, text="Quitter", command=self.destroyPad).grid(column=1, row=7, columnspan=6, pady = 3, padx = 3, sticky='nesw')
        self.showPad()


    def destroyPad(self):

        self.padFrame.destroy()
        self.unbind(9)



    def GetEyeData(self,indice):
        self.currentButton.configure(bg='green')
        self.ListeOeil += [self.CDPeyeData()]
    
    def AfficherGain(self):

        self.CDPSaveGain(self.ListeOeil)
        self.RepresentationGraphe()


    def RepresentationGraphe(self):


        self.tkplot = tk.Toplevel(self.root)
        self.tkplot.title ("Représentation Gain") # nom de la fenetre tkinter fille
        self.fig = Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tkplot)  
        self.canvas.get_tk_widget().pack(fill='both', expand=True)


        ax = self.fig.add_subplot(111)
        ax.set_xlim(0,1920)
        ax.set_ylim(0,1080)
        ax.invert_yaxis()

        col = ['black','grey','yellow','green','pink','red','blue','purple']
        cpt = 0

        for Liste in self.ListeOeil:
            ListeXdroit = []
            ListeYdroit = []
            ListeXgauche = []
            ListeYgauche = []
            for i in range (len(Liste)):

                if Liste[i][1]!=(-1,-1) and Liste[i][2] !=(-1,-1):

                    ListeXdroit += [(Liste[i][1][0])]
                    ListeYdroit+= [(Liste[i][1][1])]
                    ListeXgauche += [(Liste[i][2][0])]
                    ListeYgauche += [(Liste[i][2][1])]

                elif Liste[i][1]!=(-1,-1):
                    ListeXdroit += [(Liste[i][1][0])]
                    ListeYdroit+= [(Liste[i][1][1])]

                elif Liste[i][2]!=(-1,-1):
                    ListeXgauche += [(Liste[i][2][0])]
                    ListeYgauche += [(Liste[i][2][1])] 

            ax.scatter(ListeXdroit,ListeYdroit,c=col[cpt],s=10)
            ax.scatter(ListeXgauche,ListeYgauche,c=col[cpt],s=10)
            ax.scatter(Liste[0][0][0],Liste[0][0][1],c=col[cpt],s=60)
            cpt+=1


        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.show()	


    def GainX(self,x,Gain):
        Gain = (x -960)*(Gain - 1)
        return (Gain)

    def GainY(self,y,Gain):
        Gain = (y-540)*(Gain-1)
        return (Gain)

    def sendPoint(self, num):
        self.currentButton = self.boutons[num]
        self.CDPSendPoint(num)
        
    def validatePoint(self,num):
        self.currentButton.configure(bg='green')
        self.CDPValidatePoint(num)


    def ValidationPos(self):
	    self.CPDValidationPostion()


    def InterfacefixationPoint(self):

        self.cptVisu = 0
        self.ind = tk.Label(self.root, text="Sélectionner un individu :")
        self.ind.grid(row=0,columnspan=3)
        self.scrollbar = tk.Scrollbar(self.root)
        self.listbox = tk.Listbox(self.root,height=3)
        self.listbox.grid(row =1,column=2)
        for i in self.ListeInd:
            self.listbox.insert(tk.END,i)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview) 




        self.afficvistxt = tk.Label(self.root, text="Cocher la case pour la visualisation :")
        self.afficvistxt.grid(row=3,columnspan=3)
        self.affvis  = tk.IntVar ()
        self.case = tkinter.Checkbutton (variable = self.affvis)
        self.case.grid(row=3,column=3)


        self.xtxt = tk.Label(self.root, text="x fixation =")
        self.xtxt.grid(row=6,column=1)
        self.x = tk.Entry(self.root,justify='center')
        self.x.insert(0,0.5)
        self.x.grid(row=6,column=2)

        self.ytxt = tk.Label(self.root, text="y fixation =")
        self.ytxt.grid(row=7,column=1)
        self.y = tk.Entry(self.root,justify='center')
        self.y.insert(0,0.65)
        self.y.grid(row=7,column=2)

        self.toltxt = tk.Label(self.root, text="Tolérance (px) =")
        self.toltxt.grid(row=8,column=1)
        self.tol = tk.Entry(self.root,justify='center')
        self.tol.insert(0,80)
        self.tol.grid(row=8,column=2)

        self.temps = tk.Label(self.root, text="Entrer le temps de fixation en millisecondes :")
        self.temps.grid(row=9,columnspan=3)
        self.tfix = tk.Entry(self.root,justify='center')
        self.tfix.insert(0,250)
        self.tfix.grid(row=10,column=2)
        self.buttonVal = tk.Button(self.root, text="Valider", command = self.fixationPoint)
        self.buttonVal.grid(row=11,column=2)

        self.annuler = tk.Button(self.root, text="Stop", command=self.annuleFixationPoint)
        self.annuler.grid(row=12,column=2)

        


    def fixationPoint(self):
        if self.affvis.get() == 1 and self.cptVisu ==0:     
            self.AffichageVis()
            self.cptVisu = 1
        if self.affvis.get() == 0 and self.cptVisu ==1:
            self.CDPDeleteVisualisation()
            self.cptVisu = 0

        tol = int(self.tol.get())
        xfix = float(self.x.get())
        yfix = float(self.y.get())

        self.tfixation = int(self.tfix.get())
        Name = self.listbox.get(tk.ACTIVE)
        self.CDPFixationPoint(self.tfixation,Name,tol,xfix,yfix)

    def annuleFixationPoint(self):

        self.case.destroy()
        self.afficvistxt.destroy()
        self.temps.destroy()
        self.tfix.destroy()
        self.buttonVal.destroy()
        self.annuler.destroy()
        self.scrollbar.destroy()
        self.listbox.destroy()
        self.afficvistxt.destroy()
        self.case.destroy()
        self.xtxt.destroy()
        self.x.destroy()
        self.ytxt.destroy()
        self.y.destroy()
        self.toltxt.destroy()
        self.tol.destroy()
        self.ind.destroy()

    def ApprentissagePos(self):

        self.nom = tk.Label(self.root, text="Nom de l'individu")
        self.nom.grid(row=0)
        self.rec = tk.Label(self.root, text="Récompense")
        self.rec.grid(row=1)
        self.cond = tk.Label(self.root, text="Condition")
        self.cond.grid(row=2)
        self.rq = tk.Label(self.root, text="Remarque")
        self.rq.grid(row=3)

        self.AffichageVis()
        self.scrollbar = tk.Scrollbar(self.root)
        self.listbox = tk.Listbox(self.root,height=3)
        self.listbox.grid(row =0,column=1)
        for i in self.ListeInd:
            self.listbox.insert(tk.END,i)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.recompense = tk.Entry(self.root)
        self.recompense.insert(0,"Sirop de fruit dilué x fois ")
        self.recompense.grid(row=1, column=1)

        self.condition = tk.Entry(self.root)
        self.condition.insert(0,"Court")
        self.condition.grid(row=2, column=1)
        
        self.remarque = tk.Entry(self.root)
        self.remarque.insert(0,"RAS")
        self.remarque.grid(row=3, column=1)


        self.buttonVal = tk.Button(self.root, text="Start", command = self.ApprentissagePosition)
        self.buttonVal.grid(row=5, column=1)

        self.abandonner = tk.Button(self.root, text="Fin", command=self.dstroyentry)    
        self.abandonner.grid(row=5, column=2)

    def dstroyentry(self):
        
        self.cond.destroy()
        self.condition.destroy()
        self.recompense.destroy()
        self.rec.destroy()
        self.abandonner.destroy()
        self.buttonVal.destroy()
        self.remarque.destroy()
        self.rq.destroy()
        self.nom.destroy()
        self.scrollbar.destroy()
        self.listbox.destroy()

        self.CDPDeleteVisualisation()


    def ApprentissagePosition(self):


        Name = self.listbox.get(tk.ACTIVE)
        Condition = self.condition.get()
        Recompense = self.recompense.get()
        self.CDPApprentissagePos(Name,Condition,Recompense)



    ''' Exemples d experience ''' 


    def fonc_essai(self):
        self.fonction_essai()

    def Les4points(self):
        self.CDPLes4points() 


    def hidePad(self):
        self.padFrame.grid_forget()
      
    def showPad(self):
        self.padFrame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        for indice in range(len(self.boutons)): 
            if ( self.boutons[indice] !=0 ):
                self.boutons[indice] .configure(bg='#F0F0F0')



    def FixVisage(self):
	    self.CDPFixVisage()


    def InterfaceExplorationVisage(self):
        self.nom = tk.Label(self.root, text="Nom de l'individu")
        self.nom.grid(row=0,column=1)



        self.scrollbar = tk.Scrollbar(self.root)
        self.listbox = tk.Listbox(self.root,height=3)
        self.listbox.grid(row =0,column=2)
        for i in self.ListeInd:
            self.listbox.insert(tk.END,i)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)


        self.coordonneext = tk.Label(self.root, text="x Fixation")
        self.coordonneext.grid(row=1,column=1)
        self.cordonneeX = tk.Entry(self.root,justify='center')
        self.cordonneeX.insert(0,0.2)
        self.cordonneeX.grid(row=1,column=2)

        self.coordonneeyt = tk.Label(self.root, text="y Fixation")
        self.coordonneeyt.grid(row=2,column=1)
        self.cordonneeY = tk.Entry(self.root,justify='center')
        self.cordonneeY.insert(0,0.65)
        self.cordonneeY.grid(row=2,column=2)




        self.buttonVal = tk.Button(self.root, text="Start", command = lambda: self.ExploVisage())
        self.buttonVal.grid(row=3, column=2)

        self.abandonner = tk.Button(self.root, text="Fin", command=self.destroyIntefaceExplVisage)    
        self.abandonner.grid(row=4, column=2)


    def ExploVisage(self):
        xfix = self.cordonneeX.get()
        yfix = self.cordonneeY.get()
        self.CDPExplorationVisage(self.listbox.get(tk.ACTIVE),xfix,yfix)

    def destroyIntefaceExplVisage(self):
        self.coordonneext.destroy()
        self.cordonneeX.destroy()
        self.coordonneeyt.destroy()
        self.cordonneeY.destroy()
        self.nom.destroy()
        self.abandonner.destroy()
        self.buttonVal.destroy()
        self.scrollbar.destroy()
        self.listbox.destroy()




    ''' Gestions des interfaces graphiques ''' 



    def effacer(self):
	    self.CDPeffacer()	

    def AffichageVis(self):
        self.CDPaffichageVis()
    


    def Nictation(self):
        self.CDPcontroleNictation()


    ''' Quitter l'interface ''' 

 
    def quit(self):
        if tkinter.messagebox.askyesno('Confirmation', 'Etes-vous certain de vouloir quitter ?'):
            self.root.destroy()


    def SGVS(self):
        self.CDPSGVS() 


        
    # Methodes a surcharger dans les classes filles

    def CDPExit(self):
        pass   

    def CDPValidatePoint(self,num):
        pass   

    def CDPInitialisation(self):
        pass   
    def CDPDisconnect(self):
        pass

    def CDPSendPoint(self, num):
        pass  

    def CDPApplyCalibration(self):
        pass

    def CDPLoadCalibration(self):
	    pass
    def CDPVisualisationCalibration(self):
        pass
    def CDPLeaveCalibration(self):
        pass

    def CPDValidationPostion(self):
        pass 

    def CDPinitCalibration(self):
        pass
    def CDPEndCalibration(self):
        pass
    def CDPeyeData(self):
        pass
    def CDPSaveGain(self,Liste):
        pass
    def CDPFixationPoint(self,t,name,tol,x,y):
        pass

    def CDPApprentissagePos(self,Name,Cond,Rec):
        pass

    def fonction_essai(self):
        pass

    def CDPExplorationVisage(self,name,xfix,yfix):
        pass

    def CDPSGVS(self):
	    pass
    def CDPFixVisage(self):
	    pass
    def CDPcontroleNictation(self):
        pass

    def CDPeffacer(self):
	    pass 

    def CDPaffichageVis(self):
        pass



    def CDPDispGIF(self):
        pass
        