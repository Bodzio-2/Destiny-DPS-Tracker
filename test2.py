import cv2
import numpy as np
import time
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread("C:/Users/dunge/Desktop/crit.png")


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("hsv", hsv)
cv2.waitKey(0)

# Get binary-mask
msk = cv2.inRange(hsv, np.array([0, 150, 175]), np.array([179, 255, 255]))
krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
dlt = cv2.dilate(msk, krn, iterations=1)
thr = 255 - cv2.bitwise_and(dlt, msk)


# OCR
d = pytesseract.image_to_string(thr, config="--psm 6 -c tessedit_char_whitelist=,0123456789 ")
print(d)

cv2.imshow("thresh", thr)
cv2.waitKey(0)