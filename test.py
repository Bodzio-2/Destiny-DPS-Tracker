import cv2
import numpy as np
import time
import pyautogui
import pytesseract
import os

print("----------------------------")


def writeAnnouncement(message):
    print(message)
    print("----------------------------" + "\n")


def removeFiles(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


writeAnnouncement("Cleaning folders")

removeFiles('images/contours/')
removeFiles('images/dilation/')
removeFiles('images/gray/')
removeFiles('images/processed/')

writeAnnouncement("Folders cleaned, Starting program")

i = 0
found = False
start_x = pyautogui.size()[0]/6
start_y = pyautogui.size()[1]/8

size_x = (pyautogui.size()[0]/4) * 3
size_y = (pyautogui.size()[1]/5) * 4

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

file = open("parsedText.txt", "w+")

while (i != 200):

    image = pyautogui.screenshot(region=(start_x, start_y, size_x, size_y))

    image = cv2.cvtColor(np.array(image),
                         cv2.COLOR_RGB2BGR)
    
    # blurred = cv2.GaussianBlur(image, (5, 5), 1)

    mask = cv2.inRange(image, (0, 140, 160), (50, 240, 255))
  
    res = 255 - mask

    ret, thresh1 = cv2.threshold(
        res, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = res.copy()
    j = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y+h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x: x+w]

        text = pytesseract.image_to_string(cropped)
        text=text.split()
        text=text[0]
        print(text)
        cv2.imwrite("images/processed/" + str(i) +
                    "_" + str(j) + ".png", cropped)

        if(text!=''):
            file.write(text + "\n")
        j += 1
        found = True

    if (found):
        cv2.imwrite("images/gray/" + str(i) + ".png", res)
        cv2.imwrite("images/dilation/" + str(i) + ".png", dilation)
        found = False

    cv2.imwrite("images/contours/" + str(i) + ".png", image)

    i += 1

    time.sleep(0.2)
file.close()
