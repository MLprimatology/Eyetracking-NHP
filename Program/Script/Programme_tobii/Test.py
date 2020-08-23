import time
import tobii_research as tr
 
global_user_position_guide = None

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]

 
def user_position_guide_callback(user_position_guide):
	global global_user_position_guide
	global_user_position_guide = user_position_guide

 
def user_position_guide(eyetracker):
	global global_user_position_guide
 
	print("Subscribing to user position guide for eye tracker with serial number {0}.".format(eyetracker.serial_number))
	eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE, user_position_guide_callback, as_dictionary=True)
 
	# Wait while some user position guide is collected.
	time.sleep(2)

	eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_position_guide_callback)
	print("Unsubscribed from user position guide.")
 
	print("Last received user position guide package:")
	print(global_user_position_guide


user_position_guide(eyetracker)



import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
