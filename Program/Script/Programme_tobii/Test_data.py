def execute(eyetracker):
	return(gaze_data(eyetracker))
 
 

import time
import tobii_research as tr
  
global_gaze_data = None

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]
 
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
	print(global_gaze_data.get("right_gaze_point_on_display_area"))
	print(global_gaze_data.get("left_gaze_point_on_display_area"))
	OeilD = global_gaze_data.get("right_gaze_point_on_display_area") #coordonnee oeil gauche display area
	OeilG = global_gaze_data.get("left_gaze_point_on_display_area") ## coordonnee oeil droit display area

	eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
	print("Unsubscribed from gaze data.")
 
	print("Last received gaze package:")
	return (OeilD, OeilG)


a , b = execute(eyetracker)
print(a, b)

