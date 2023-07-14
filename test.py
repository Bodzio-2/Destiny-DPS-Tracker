import cv2
import numpy as np
import time
import pyautogui
import pytesseract
import os


def writeAnnouncement(message):
    print(message)
    print("----------------------------\n")


def removeFiles(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def imageTreatment(start_x, start_y, size_x, size_y):
    image = pyautogui.screenshot(region=(start_x, start_y, size_x, size_y))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(image, (0, 140, 160), (50, 240, 255))
    res = 255 - mask
    ret, thresh1 = cv2.threshold(
        res, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return res.copy(), contours, dilation, image


def main():

    i = 0
    found = False
    start_x = pyautogui.size()[0] / 6
    start_y = pyautogui.size()[1] / 8
    size_x = (pyautogui.size()[0] / 4) * 3
    size_y = (pyautogui.size()[1] / 5) * 4
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    custom_tesseract_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'
    path_baseImg = 'images/baseimage/'
    path_maskImg = 'images/mask/'
    path_recColImg = 'images/recognized_color/'
    path_procImg = 'images/processed/'

    print("----------------------------")
    writeAnnouncement("Cleaning folders")
    removeFiles(path_baseImg)
    removeFiles(path_maskImg)
    removeFiles(path_recColImg)
    removeFiles(path_procImg)
    writeAnnouncement("Folders cleaned, Starting program")

    file = open("parsedText.txt", "w+")
    sum = 0

    while i != 200:
        im2, contours, dilation, originalImage = imageTreatment(
            start_x, start_y, size_x, size_y)

        j = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cropped = im2[y:y + h, x:x + w]

            text = pytesseract.image_to_string(
                cropped, config=custom_tesseract_config)
            try:
                text = text.split()[0]
            except:
                pass
            if text != '':
                file.write(text + "\n")
                print("DMG = " + text)
                try:
                    sum += int(text)
                except:
                    pass
                print("Sum = " + str(sum))
            cv2.imwrite(path_procImg + str(i) +
                        "_" + str(j) + ".png", cropped)
            j += 1
            found = True

        if found:
            cv2.imwrite(path_recColImg + str(i) + ".png", im2)
            cv2.imwrite(path_maskImg + str(i) + ".png", dilation)
            cv2.imwrite(path_baseImg + str(i) + ".png", originalImage)
            found = False

        i += 1

        time.sleep(0.8)

    file.close()


if __name__ == "__main__":
    main()
