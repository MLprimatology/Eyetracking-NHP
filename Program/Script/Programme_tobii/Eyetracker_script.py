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
## obtenir gaze data ####
def test(eyetracker):
	return(gaze_data(eyetracker))
 
 
def gaze_data_callback(gaze_data):
	global global_gaze_data
	global_gaze_data = gaze_data
 
 
def gaze_data(eyetracker):
	global global_gaze_data
 
	print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
	eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
 	
   # Wait while some gaze data is collected.
	time.sleep(1)
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




 
# Enter calibration mode.
calibration = tr.ScreenBasedCalibration(eyetracker)
calibration.enter_calibration_mode()
print "Entered calibration mode for eye tracker with serial number {0}.".format(eyetracker.serial_number)



# Define the points on screen we should calibrate at.
# The coordinates are normalized, i.e. (0.0, 0.0) is the upper left corner and (1.0, 1.0) is the lower right corner.
points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]
 
for point in points_to_calibrate:
	print "Show a point on screen at {0}.".format(point)

	x1 = Conversionx(point[0]) - 15
	y1 = Conversiony(point[1]) - 15 
	x2 = Conversionx(point[0]) + 15
	y2 = Conversiony(point[1]) + 15
	ball = can.create_oval(x1, y1, x2, y2, fill="yellow") ### creation d un cercle jaune 
	root.update()

	## appuyer sur une toucher  pour continuer 

	sys.stdin.readline()

	print "Collecting data at {0}.".format(point)
	if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
	# Try again if it didn't go well the first time.
	# Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
		
		calibration.collect_data(point[0], point[1])
	can.delete(ball)
print "Computing and applying calibration."
calibration_result = calibration.compute_and_apply()

print "Compute and apply returned {0} and collected at {1} points.".\
	format(calibration_result.status, len(calibration_result.calibration_points))

# The calibration is done. Leave calibration mode.
calibration.leave_calibration_mode()

print('Press enter to finish calibration')



sys.stdin.readline()

List_Pos = []

for point in points_to_calibrate:
	print "Show a point on screen at {0}.".format(point)

	x1 = Conversionx(point[0]) - 15
	y1 = Conversiony(point[1]) - 15 
	x2 = Conversionx(point[0]) + 15
	y2 = Conversiony(point[1]) + 15
	ball = can.create_oval(x1, y1, x2, y2, fill="yellow") ### creation d un cercle jaune 
	root.update()


		## appuyer sur une toucher  pour continuer 

	sys.stdin.readline()

	List_Pos +=[test(eyetracker)]
	can.delete(ball)






print(List_Pos)

for i in range (len(List_Pos)):   #creation oeil droit sur ecran 
	x1 = Conversionx(List_Pos[i][0][0]) - 7
	y1 = Conversionx(List_Pos[i][0][1]) - 7
	x2 = Conversionx(List_Pos[i][0][0]) + 7
	y2 = Conversionx(List_Pos[i][0][1]) + 7
	ball = can.create_oval(x1, y1, x2, y2, fill="green") ### creation d un cercle vert 
	root.update()

for i in range (len(List_Pos)):   #creation oeil gauche sur ecran 
	x1 = Conversionx(List_Pos[i][1][0]) - 7
	y1 = Conversionx(List_Pos[i][1][1]) - 7
	x2 = Conversionx(List_Pos[i][1][0]) + 7
	y2 = Conversionx(List_Pos[i][1][1]) + 7
	ball = can.create_oval(x1, y1, x2, y2, fill="red") ### creation d un cercle rouge 
	root.update()

root.mainloop()









 

 

 
# See that you're happy with the result.






