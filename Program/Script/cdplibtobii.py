# -*- coding: utf8 -*-


# Modification du code Pygaze + ajout de fonction

__authors__ = ("Mathieu Legrand")
__contact__ = ("mathieu.legrand78@gmail.com")
__version__ = "1.0.0"
__copyright__ = "copyleft"
__date__ = "23/08/2020"



from __future__ import division #CDP
import time
import os
import math
import copy
import tobii_research as tr
import json
import xlwt
from Visualisation import *
import datetime
from pygaze import libscreen



import keyboard #Using module keyboard
from pygaze import libtime
from pygaze import settings
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.eyetracker import EyeTracker
from pygaze.libtime import clock
from pygaze._eyetracker.libtobii import TobiiProTracker
from pygaze import libsound

from openpyxl import Workbook


class CDPProTracker(TobiiProTracker):
    """A class for Tobii Pro EyeTracker objects"""
    def __init__(self, display, logfile=settings.LOGFILE,
                eventdetection=settings.EVENTDETECTION,
                saccade_velocity_threshold=35,
                saccade_acceleration_threshold=9500,
                blink_threshold=settings.BLINKTHRESH, **args):
                
                TobiiProTracker.__init__(self,display, logfile=settings.LOGFILE,eventdetection=settings.EVENTDETECTION, saccade_velocity_threshold=35, saccade_acceleration_threshold=9500,blink_threshold=settings.BLINKTHRESH, **args)

                self.PositionOeil=[]
                lb = 0.1  # left bound
                xc = 0.5  # horizontal center
                rb = 0.9  # right bound
                ub = 0.1  # upper bound
                yc = 0.5  # vertical center
                bb = 0.9  # bottom bound

                self.points_to_calibrate = [self._norm_2_px(p) for p in [(0.1, 0.9), (0.5,0.9),(0.9, 0.9),(0.3,0.65),(0.7,0.65),(0.1,0.4),(0.5,0.4),(0.9,0.4)]]




    def ReduceBall (self,point,facteur,colour):
        
        
        for i in range (0,200,3):
            self.screen.clear()
            self.screen.draw_circle(colour=colour, pos=point, r=int(self.disp.dispsize[0] / (facteur+i)), pw=5, fill=True)
            self.disp.fill(self.screen)
            self.disp.show()
			
    def showPoint( self,indice):
        point = self.points_to_calibrate[indice-1]
        self.screen.clear()
        # CDP : Changement couleur
        self.screen.draw_circle(colour='red', pos=point, r=int(self.disp.dispsize[0] / 100), pw=5, fill=True)
        #self.screen.draw_circle(colour=(255, 0, 0), pos=point, r=int(self.disp.dispsize[0] / 400.0), pw=5, fill=True)
        self.disp.fill(self.screen)
        self.disp.show()

    def ApprentissagePos(self,Visu):

        self.RecSound = libsound.Sound(soundfile='/home/eyetracker/Downloads/2.wav')

        tablepos = Workbook()
        gazePosSheet = tablepos.active
        gazePosSheet.title = 'gazePos'
        gazePosSheet.append(["Time", "LeftValidity", "RightValidity"])   

        tvtot = 0
        trtot = 0
        Tp = 0
        Tr = 0
        Tv = 0
        texp = 0
        oldtmaxcons = 0
        Nbrec = 0
        TinterTrial = 0
        dist = None 
        cptPerte = 0



        Visu.write_time(Tp,Tr,Tv,texp,Nbrec,TinterTrial,tvtot,trtot,dist,oldtmaxcons)
        Visu.VisuShow()


        origin = (int(self.disp.dispsize[0] / 4), int(self.disp.dispsize[1] / 4))
        size = (int(2 * self.disp.dispsize[0] / 4), int(2 * self.disp.dispsize[1] / 4))

        texp = libtime.get_time()
        OldTime = libtime.get_time()
        

        while  not self.kb.get_key(keylist=['space'], flush=False)[0]:
            OeilD = 0
            OeilG = 0
            gaze_sample = copy.copy(self.gaze[-1])


            self.screen.clear()
            validity_colour = (255, 0, 0)
            col ='red'
            left_validity = False
            right_validity = False
            if gaze_sample['right_gaze_origin_validity'] and gaze_sample['left_gaze_origin_validity']:
                left_validity = 0.15 < gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                right_validity = 0.15 < gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                
                if right_validity and left_validity:
                    validity_colour = (0, 255, 0)
                    col ='green'


            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0] + size[0], origin[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0], origin[1] + size[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=(origin[0], origin[1] + size[1]), epos=(origin[0] + size[0], origin[1] + size[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=(origin[0] + size[0], origin[1] + size[1]), epos=(origin[0] + size[0], origin[1]), pw=1)


            Visu.effacer_mouvement()


            right_eye, left_eye, distance = None, None, []


            if gaze_sample['right_gaze_origin_validity']:
                distance.append(round(gaze_sample['right_gaze_origin_in_user_coordinate_system'][2] / 10, 1))
                OeilD = 1 
                if right_validity:
                    OeilD = 2
                right_eye = ((1 - gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][0]) * size[0] + origin[0],
                                gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour, pos=right_eye, r=int(self.disp.dispsize[0] / 100), pw=5, fill=True)
                Visu.Show_droit(right_eye[0],right_eye[1],col, int(self.disp.dispsize[0] / 200))

            if gaze_sample['left_gaze_origin_validity']:
                distance.append(round(gaze_sample['left_gaze_origin_in_user_coordinate_system'][2] / 10, 1))

                OeilG=1
                if left_validity:
                    OeilG=2
                left_eye = ((1 - gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][0]) * size[0] + origin[0],
                                gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour, pos=left_eye, r=int(self.disp.dispsize[0] / 100), pw=5, fill=True)
                Visu.Show_gauche(left_eye[0],left_eye[1],col, int(self.disp.dispsize[0] / 200))

            gazePosSheet.append([int((libtime.get_time()-texp)),OeilG,OeilD])



            Visu.VisuShow()
            if self._mean(distance) != None:
                dist = self._mean(distance)

            NewTime = libtime.get_time()
            deltaT = NewTime - OldTime
            OldTime = NewTime
            txp = libtime.get_time()-texp



            if cptPerte > 650:
                Tv = 0
                Tr  = 0

            if OeilD ==2 and OeilG ==2:
                Tv += deltaT
                cptPerte =0
                tvtot +=deltaT

            elif OeilD == 1 or OeilG ==1:
                Tr +=deltaT
                cptPerte = 0
                trtot += deltaT

            else : 
                Tp += deltaT
                cptPerte += deltaT


            newtmaxcons = Tr + Tv
            if newtmaxcons > oldtmaxcons:
                oldtmaxcons = newtmaxcons

            if self.kb.get_key(keylist= ['q'], flush=False)[0]:
                tdeb = libtime.get_time()
                self.RecSound.play()
                self.screen.clear()
                self.disp.fill(self.screen)
                self.disp.show()


                Nbrec +=1 
                Tr = 0
                Tv = 0
                self.kb.get_key(keylist=['q'], flush=True, timeout=None) 
                TinterTrial += libtime.get_time() - tdeb
                OldTime = libtime.get_time()
                txp = libtime.get_time()-texp



            if self.kb.get_key(keylist= ['tab'], flush=False)[0]:
                tdeb = libtime.get_time()
                self.screen.clear()
                self.disp.fill(self.screen)
                self.disp.show()
                Tr = 0
                Tv = 0
                self.kb.get_key(keylist=['tab'], flush=True, timeout=None) 
                TinterTrial += libtime.get_time() - tdeb
                OldTime = libtime.get_time()
                txp = libtime.get_time()-texp


                
            Visu.effacer_text()
            Visu.write_time(int(Tp),int(Tr),int(Tv),int(txp/100)/10,Nbrec,int(TinterTrial),int(tvtot),int(trtot),dist,int(oldtmaxcons))
            Visu.VisuShow()

            self.disp.fill(self.screen)
            self.disp.show()


        Visu.effacer_text()
        Visu.VisuShow()

        self.screen.clear()
        self.disp.fill(self.screen)
        self.disp.show()
    
        
        return(['ind','date','jour',int(tvtot),int(trtot),int(Tp),int(txp),int(oldtmaxcons),'Condidtion',Nbrec,int(TinterTrial),Nbrec,'Remarque'],tablepos)


    def initCalibration(self,Visu):

        self.RecSound = libsound.Sound(soundfile='/home/eyetracker/Downloads/2.wav')

        self.calibrated_point = []
        self._write_enabled = False
        self.start_recording()
        self.screen.set_background_colour(colour=(0, 0, 0))
        origin = (int(self.disp.dispsize[0] / 4), int(self.disp.dispsize[1] / 4))
        size = (int(2 * self.disp.dispsize[0] / 4), int(2 * self.disp.dispsize[1] / 4))

        while not self.kb.get_key(keylist=['space'], flush=False)[0]:
            gaze_sample = copy.copy(self.gaze[-1])

            self.screen.clear()

            validity_colour = (255, 0, 0)
            col = 'red'
            Visu.effacer_mouvement()

            if gaze_sample['right_gaze_origin_validity'] and gaze_sample['left_gaze_origin_validity']:
                left_validity = 0.15 < gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                right_validity = 0.15 < gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                if left_validity and right_validity:
                    validity_colour = (0, 255, 0)
                    col = 'green'
            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0] + size[0], origin[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0], origin[1] + size[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=(origin[0], origin[1] + size[1]), epos=(origin[0] + size[0], origin[1] + size[1]), pw=1)

            self.screen.draw_line(colour=validity_colour, spos=(origin[0] + size[0], origin[1] + size[1]), epos=(origin[0] + size[0], origin[1]), pw=1)

            right_eye, left_eye, distance = None, None, []
            if gaze_sample['right_gaze_origin_validity']:
                right_eye = ((1 - gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][0]) * size[0] + origin[0],
                                gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour, pos=right_eye, r=int(self.disp.dispsize[0] / 100), pw=5, fill=True)
                Visu.Show_droit(right_eye[0],right_eye[1],col, int(self.disp.dispsize[0] / 200))

            if gaze_sample['left_gaze_origin_validity']:
                left_eye = ((1 - gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][0]) * size[0] + origin[0],
                                gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour, pos=left_eye, r=int(self.disp.dispsize[0] / 100), pw=5, fill=True)
                Visu.Show_gauche(left_eye[0],left_eye[1],col, int(self.disp.dispsize[0] / 200))

            Visu.VisuShow()
            self.disp.fill(self.screen)
            self.disp.show()

            if self.kb.get_key(keylist= ['tab'], flush=False)[0]:
                self.screen.clear()
                self.disp.fill(self.screen)
                self.disp.show()
                Visu.effacer_mouvement()
                Visu.VisuShow()
                return()
        Visu.effacer_mouvement()
        Visu.VisuShow()

        # # # # # #
        # # calibration
        self.screen.clear()
        
        if not self.eyetracker:

            print("WARNING! libtobii.TobiiProTracker.calibrate: no eye trackers found for the calibration!")
            self.stop_recording()

            return False

        self.calibration = tr.ScreenBasedCalibration(self.eyetracker)
        self.disp.show()
        self.calibration.enter_calibration_mode()
        self.RecSound.play()


    def addCalibrationPoint(self, indice): 
        

        dispAffich = libscreen.Display(screennr=1)
        point = self.points_to_calibrate[indice]
        Newscreen = libscreen.Screen()
        
        for i in range (0,200,3):
            Newscreen.clear()
            Newscreen.draw_circle(colour='red', pos=point, r=int(1920 / (50+i)), pw=5, fill=True)
            dispAffich.fill(Newscreen)
            dispAffich.show()

        dispAffich.close()

    def validateCalibrationPoint(self,num):
        liste_normalizedPoint = [(0.1, 0.9), (0.5,0.9),(0.9, 0.9),(0.3,0.65),(0.7,0.65),(0.1,0.4),(0.5,0.4),(0.9,0.4)]
        self.normalized_point = liste_normalizedPoint[num]

        if self.normalized_point != (0,0):
            status = self.calibration.collect_data(self.normalized_point[0], self.normalized_point[1])
            if status != tr.CALIBRATION_STATUS_SUCCESS:
                status = self.calibration.collect_data(self.normalized_point[0], self.normalized_point[1])
            print( status, "-", self.normalized_point[0], "-", self.normalized_point[1])

	    if (self.normalized_point not in self.calibrated_point) == True :
		    self.calibrated_point += [self.normalized_point]
	    self.calibrated_pointpx =[self._norm_2_px(p) for p in self.calibrated_point]

        self.normalized_point = (0,0)


        
    def applyCalibration(self,filename):
        
        #self.screen.clear()
        #self.disp.fill(self.screen)
        #self.disp.show()

        calibration_result = self.calibration.compute_and_apply()

        self.calibration.leave_calibration_mode()
	
	
                
        print "Compute and apply returned {0} and collected at {1} points.".\
            format(calibration_result.status, len(calibration_result.calibration_points))

        if calibration_result.status != tr.CALIBRATION_STATUS_SUCCESS:
            self.stop_recording()
            print("WARNING! libtobii.TobiiProTracker.calibrate: Calibration was unsuccessful!")
            return False

        self.screen.clear()
        OeilGauche = []
        OeilDroit = []



        Liste = []


        for point in calibration_result.calibration_points:
            for sample in point.calibration_samples:

                if sample.left_eye.validity == tr.VALIDITY_VALID_AND_USED:
                    OeilGauche += [[(self._norm_2_px(point.position_on_display_area)), (self._norm_2_px(sample.left_eye.position_on_display_area))]]

                if sample.right_eye.validity == tr.VALIDITY_VALID_AND_USED:
                    OeilDroit += [[(self._norm_2_px(point.position_on_display_area)), (self._norm_2_px(sample.right_eye.position_on_display_area))]]

                xD = self._norm_2_px(sample.right_eye.position_on_display_area)[0]
                yD = self._norm_2_px(sample.right_eye.position_on_display_area)[1]
                xG = self._norm_2_px(sample.left_eye.position_on_display_area)[0]
                yG = self._norm_2_px(sample.left_eye.position_on_display_area)[1]

                if xD == 0:
                    xD = -1
                if yD == 0:
                    yD = -1
                if xG == 0:
                    xG = -1
                if yG == 0:
                    yG = -1                    
                Liste += [[self._norm_2_px(point.position_on_display_area)[0],self._norm_2_px(point.position_on_display_area)[1],xD,yD,xG,yG]]
        self.PositionOeil = [OeilDroit, OeilGauche]
        
        

        
        self.stop_recording()
        return(Liste)

        #date =  datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        #table.save(filename + '_' + date + ".xls")





    def FinCalibration(self):

        self.screen.clear()
        self.disp.fill(self.screen)
        self.disp.show()
    	self.start_recording()

        ListePos =[]
    	self.kb.get_key(keylist=['space'], flush=True, timeout=None)
        self.calibrated_pointpx = [self._norm_2_px(p) for p in [(0.1,0.1),(0.9,0.1),(0.5,0.5),(0.1,0.9),(0.9,0.9)]]
        for pos in self.calibrated_pointpx:
            ListeProv = []
            self.screen.clear()
    	    self.ReduceBall(pos,40,'yellow')
            self.disp.fill(self.screen)
            self.disp.show()
                # wait for pressing 'space' to collect data
    	    self.kb.get_key(keylist=['space'], flush=True, timeout=None) 
            tdeb = libtime.get_time()
            # Lancement de l'échantillonage / capture de la position des yeux
            oldTimeStamp = 0
            txp,gase = self.binocular_sample()
            while libtime.get_time()-tdeb < 300 :
                time.sleep(0.01)
                NewTimeStamp, Newgazepos = self.binocular_sample()
                if NewTimeStamp != oldTimeStamp :
                    oldTimeStamp = NewTimeStamp
                    ListeProv += [[pos,Newgazepos[0],Newgazepos[1],Newgazepos[2]]]
            # calculate mean accuracy
            ListePos += [ListeProv]

        self.screen.clear()
        self.disp.fill(screen=self.screen)
        self.disp.show()

    	self.stop_recording()
        return(ListePos)
        
    def RecupDonneesOeil(self,indice):



        self.point = self.points_to_calibrate[indice-1]
        ListeProv = []
        self.start_recording()

        tdeb = libtime.get_time()
        # Lancement de l'échantillonage / capture de la position des yeux
        oldTimeStamp = 0
        txp,gase = self.binocular_sample()
        while libtime.get_time()-tdeb < 300 :
            time.sleep(0.01)
            NewTimeStamp, Newgazepos = self.binocular_sample()
            if NewTimeStamp != oldTimeStamp :
                oldTimeStamp = NewTimeStamp
                ListeProv += [[self.point,Newgazepos[0],Newgazepos[1],Newgazepos[2]]]
        self.stop_recording()

        return(ListeProv)
    def binocular_sample(self):

        
        """Returns newest available gaze position

        The gaze position is relative to the self.eye_used currently selected.
        If both eyes are selected, the gaze position is averaged from the data of both eyes.

        arguments
        None

        returns
        sample	-- an [(x1,y1),(x2,y2)] tuple  (-1,-1) on an error and pos we use
        """

        gaze_sample = copy.copy(self.gaze[-1])
        
        if gaze_sample["left_gaze_point_validity"] and gaze_sample["right_gaze_point_validity"]:
            left_sample = self._norm_2_px(gaze_sample["left_gaze_point_on_display_area"])
            right_sample = self._norm_2_px(gaze_sample["right_gaze_point_on_display_area"])
            return (gaze_sample["system_time_stamp"],[(left_sample[0],left_sample[1]), ( right_sample[0],right_sample[1]),(self._mean([left_sample[0], right_sample[0]]), self._mean([left_sample[1], right_sample[1]]))])

        if gaze_sample["left_gaze_point_validity"]:
            return (gaze_sample["system_time_stamp"],[self._norm_2_px(gaze_sample["left_gaze_point_on_display_area"]),(-1,-1),(self._norm_2_px(gaze_sample["left_gaze_point_on_display_area"]))])

        if gaze_sample["right_gaze_point_validity"]:
            return (gaze_sample["system_time_stamp"],[(-1,-1), self._norm_2_px(gaze_sample["right_gaze_point_on_display_area"]),(self._norm_2_px(gaze_sample["right_gaze_point_on_display_area"]))])

        return (gaze_sample["system_time_stamp"],  [(-1, -1),(-1, -1),(-1,-1)])








    
