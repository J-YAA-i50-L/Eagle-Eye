import cv2
import numpy as np

ing_size = [900, 400]

cap = cv2.VideoCapture(r"c:/Python/python by/GAZ.py/svet_e.mp4")
# cap = cv2.VideoCapture(r"c:/Python/python by/GAZ.py/bin_test.mp4")

while (cv2.waitKey(1) != 27):
    ret, img = cap.read()
    if ret == False:              #если конец видио
        print('конец видио')
        break

    img = cv2.resize(img, (ing_size[1], ing_size[0]))
    cv2.imshow('img', img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11), (5, 5))

    # Деление светофора на три зоны
    hsv_r = hsv[0:300, 0:400]
    hsv_e = hsv[300:600, 0:400]
    hsv_g = hsv[600:900, 0:400]

    # Красный цвет бинаризация

    lower_range_r = np.array([173, 125, 204], np.uint8)
    upper_range_r = np.array([255, 255, 255], np.uint8)

    maks_r = cv2.inRange(hsv_r, lower_range_r, upper_range_r)
    maks_r = cv2.morphologyEx(maks_r, cv2.MORPH_CLOSE, st1)
    maks_r = cv2.morphologyEx(maks_r, cv2.MORPH_OPEN, st2)

    maks_r = cv2.GaussianBlur(maks_r, (5, 5), 1)

    cv2.imshow('mask_r', maks_r)

    # Жёлтый цвет бинаризация

    lower_range_e = np.array([13, 104, 222], np.uint8)
    upper_range_e = np.array([47, 232, 255], np.uint8)

    maks_e = cv2.inRange(hsv_e, lower_range_e, upper_range_e)
    maks_e = cv2.morphologyEx(maks_e, cv2.MORPH_CLOSE, st1)
    maks_e = cv2.morphologyEx(maks_e, cv2.MORPH_OPEN, st2)

    maks_e = cv2.GaussianBlur(maks_e, (5, 5), 1)

    cv2.imshow('mask_e', maks_e)

    # Зелёный цвет бинаризация
    lower_range_g = np.array([36, 106, 158], np.uint8)
    upper_range_g = np.array([154, 255, 255], np.uint8)

    maks_g = cv2.inRange(hsv_g, lower_range_e, upper_range_e)
    maks_g = cv2.morphologyEx(maks_g, cv2.MORPH_CLOSE, st1)
    maks_g = cv2.morphologyEx(maks_g, cv2.MORPH_OPEN, st2)

    maks_g = cv2.GaussianBlur(maks_g, (5, 5), 1)

    cv2.imshow('mask_g', maks_g)

    if np.any(maks_r[150, 200] != 0):
        print("Красный цвет")
    if np.any(maks_e[150, 200] != 0):
        print("Жёлтый цвет")
    if np.any(maks_g[150, 200] != 0):
        print("Зелёный цвет")

