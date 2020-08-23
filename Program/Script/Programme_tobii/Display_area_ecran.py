

def execute(eyetracker):
# <BeginExample>
	from tobii_research import DisplayArea
	import tkinter as tk

	root = tk.Tk()

	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
 
	display_area = eyetracker.get_display_area()

	print("Got display area from tracker with serial number {0}:".format(eyetracker.serial_number))
	print("Bottom Left: {0}".format(display_area.bottom_left))
	print(display_area.bottom_left[0])
	print("Bottom Right: {0}".format(display_area.bottom_right))
	print("Height: {0}".format(display_area.height))
	print("Top Left: {0}".format(display_area.top_left))
	print("Top Right: {0}".format(display_area.top_right))
	print("Width: {0}".format(display_area.width))

def Conversion_user_pixel():
	

import tobii_research as tr
found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]
