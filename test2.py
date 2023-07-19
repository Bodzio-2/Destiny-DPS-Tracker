import cv2
import numpy as np
import time
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

normal_crit = "C:/Users/dunge/Desktop/crit.png"
insane_overlap = "C:/Users/dunge/Desktop/insane_overlap.png"

img = cv2.imread(insane_overlap)


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("hsv", hsv)
cv2.waitKey(0)

# Get binary-mask

# Yellow numbers
# msk = cv2.inRange(hsv, np.array([20, 150, 175]), np.array([30, 255, 255]))

# White numbers
msk = cv2.inRange(hsv, np.array([0, 0, 230]), np.array([30, 50, 255]))

krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
dlt = cv2.dilate(msk, krn, iterations=1)
thr = 255 - cv2.bitwise_and(dlt, msk)


# OCR
d = pytesseract.image_to_string(thr, config="--psm 6 -c tessedit_char_whitelist=,0123456789 ")
print(d)

cv2.imshow("thresh", thr)
cv2.waitKey(0)