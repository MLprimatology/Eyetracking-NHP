import time
import tobii_research as tr
import tkinter as tk
import random
import os
import sys

# Connection eyetracker

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]



calibration = tr.ScreenBasedCalibration(eyetracker)
# Enter calibration mode.
calibration.enter_calibration_mode()
print "Entered calibration mode for eye tracker with serial number {0}.".format(eyetracker.serial_number)



# Define the points on screen we should calibrate at.
# The coordinates are normalized, i.e. (0.0, 0.0) is the upper left corner and (1.0, 1.0) is the lower right corner.
points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]
 
for point in points_to_calibrate:
	time.sleep(1)
	print "Show a point on screen at {0}.".format(point)
	print "Collecting data at {0}.".format(point)
	if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
	# Try again if it didn't go well the first time.
	# Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
		tr.UserPositionGuide

		calibration.collect_data(point[0], point[1])

print "Computing and applying calibration."
calibration_result = calibration.compute_and_apply()
print "Compute and apply returned {0} and collected at {1} points.".\
	format(calibration_result.status, len(calibration_result.calibration_points))



 

 

 
# See that you're happy with the result.

# The calibration is done. Leave calibration mode.
calibration.leave_calibration_mode()
