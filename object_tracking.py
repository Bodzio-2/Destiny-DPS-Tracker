import cv2
import numpy as np
import time
import pyautogui
import pytesseract

image = cv2.imread("C:/Users/dunge/Desktop/crit.png")

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# cv2.imshow("imago", image)
# cv2.waitKey(0)

tracker = cv2.TrackerMIL.create()

initBB = cv2.selectROI("Frame", image, fromCenter=False, showCrosshair=True)


tracker.init(image, initBB)

# cv2.imshow("tracked", tracker)
# cv2.waitKey(0)


if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(image)
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(image, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
		
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", "MIL"),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(60)),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(image, text, (10, 1440 - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			
    
cv2.imshow("result", image)
cv2.waitKey(0)