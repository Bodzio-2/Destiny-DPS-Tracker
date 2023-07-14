import cv2
import numpy as np
import time
import pyautogui
import pytesseract

# def kmeans(input_img, k, i_val):
#     hist = cv2.calcHist([input_img],[0],None,[256],[0,256])
#     img = input_img.ravel()
#     img = np.reshape(img, (-1, 1))
#     img = img.astype(np.float32)

#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#     flags = cv2.KMEANS_RANDOM_CENTERS
#     compactness,labels,centers = cv2.kmeans(img,k,None,criteria,10,flags)
#     centers = np.sort(centers, axis=0)

#     return centers[i_val].astype(int), centers, hist


i = 0
start_x = pyautogui.size()[0]/4
start_y = pyautogui.size()[1]/5

size_x = (pyautogui.size()[0]/4) * 2
size_y = (pyautogui.size()[1]/5) * 3

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

file = open("parsedText.txt", "w+")

while (i != 200):

    image = pyautogui.screenshot(region=(start_x, start_y, size_x, size_y))
    image = cv2.cvtColor(np.array(image),
                         cv2.COLOR_RGB2BGR)

    # _, thresh = cv2.threshold(image, kmeans(input_img=image, k=8, i_val=2)[0], 255, cv2.THRESH_BINARY)
    
    pixel_values = np.float32(image.reshape((-1, 3)))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    compactness, labels, centers = cv2.kmeans(pixel_values, 4, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    segmented_image = np.uint8(centers[labels.flatten()])

    masked_image = np.copy(image).reshape((-1, 3))
    masked_image[labels.flatten() == 1] = [0, 0, 0]
    #masked_image[labels.flatten() == 2] = [0, 0, 0]
    masked_image[labels.flatten() == 3] = [0, 0, 0]
    masked_image[labels.flatten() == 0] = [0, 0, 0]

    masked_image = masked_image.reshape(image.shape)

    cv2.imshow("test", masked_image)
    cv2.waitKey(0)

    blurred = cv2.GaussianBlur(masked_image, (5, 5), 1)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    
    # gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    
    # #dilate = cv2.dilate(gray, rect_kernel, iterations=1)

    # cv2.imshow("test", gray)
    # cv2.waitKey(0)

    # im_eroded = cv2.erode(gray, rect_kernel, iterations=1)
    # blurred_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV_FULL)

    # cv2.imshow("hsv", blurred_hsv)
    # cv2.waitKey(0)


    mask = cv2.inRange(blurred, (0, 190, 180), (30, 255, 255))
    #res = 255 - im_eroded
    
    cv2.imshow("masked", mask)
    cv2.waitKey(0)

    #edged = cv2.Canny(blurred, 50, 200, 255)
    # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(
        mask, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    cv2.imshow("dilation", thresh1)
    cv2.waitKey(0)

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = edged.copy()
    j = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y+h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x: x+w]

        cv2.imshow("cropped", cropped)
        cv2.waitKey(0)

        text = pytesseract.image_to_string(cropped)
        print(text)
        cv2.imwrite("images/processed/" + str(i) +
                    "_" + str(j) + ".png", cropped)

        file.write(text)
        file.write("\n")
        j += 1

    cv2.imwrite("images/gray/" + str(i) + ".png", res)
    cv2.imwrite("images/dilation/" + str(i) + ".png", dilation)
    cv2.imwrite("images/contours/" + str(i) + ".png", blurred)

    i += 1

    time.sleep(1)
file.close()
