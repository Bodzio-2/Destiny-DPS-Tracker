import cv2
import numpy as np
import time
import pyautogui
import pytesseract

i = 0
start_x = pyautogui.size()[0]/4
start_y = pyautogui.size()[1]/5

size_x = (pyautogui.size()[0]/4) * 2
size_y = (pyautogui.size()[1]/5) * 3


while (True):

    image = pyautogui.screenshot(region=(start_x, start_y, size_x, size_y))

    image = cv2.cvtColor(np.array(image),
                         cv2.COLOR_RGB2BGR)

    blurred = cv2.GaussianBlur(image, (5, 5), 1)
    mask = cv2.inRange(blurred, (0, 180, 200), (20, 240, 255))
    res = 255 - mask

    # edged = cv2.Canny(blurred, 50, 200, 255)
    # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(
        res, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = res.copy()

    file = open("parsedText.txt", "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y+h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x: x+w]

        file = open("parsedText.txt", "a")

        # Here replace with Tesseract-OCR path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        text = pytesseract.image_to_string(cropped)
        print(text)
        cv2.imwrite("./processed/im" + str(i) + ".png", cropped)

        file.write(text)
        file.write("\n")
        file.close()

    # cv2.imwrite("./gray/image" + str(i) + ".png", res)
    # cv2.imwrite("./dilation/im" + str(i) + ".png", dilation)
    # cv2.imwrite("./contours/im" + str(i) + ".png", blurred)
    i += 1
    time.sleep(1)
