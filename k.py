from numpy.lib.function_base import copy
import AvtoNet as an
import cv2
import numpy as np

img_size = [400, 900]  # Размер изображения с которым мы работаем

tochka_up = 25
tochka_mid = int(400 / 2)
tochka_dowen = 400 - tochka_up
baz = 120
k_ngl = 1
k_otkl = 1
pred_Up_IndWhitestColumnL = 0
pred_mid_IndWhitestColumnL = 0
pred_dofen_IndWhitestColumnL = 0
pred_Up_IndWhitestColumnR = 0
pred_mid_IndWhitestColumnR = 0
pred_dofen_IndWhitestColumnR = 0
mode = 255
speedL = 0
speedR = 0

vid = np.float32([[40, 400], 
    [450, 400], 
    [355, 320], 
    [105, 320]])

vid_p = np.float32([[0, img_size[0]],
        [450, img_size[0]],
        [450, 0],
        [0, 0]])

vid_v = np.array(vid, dtype=np.int32)

cap = cv2.VideoCapture(r"road_Trim1.mp4")
# cap = cv2.VideoCapture(r"c:/Python/python by/GAZ.py/Primer.mp4")

if not cap.isOpened():
    print('не найдени файл')
    exit()

while cv2.waitKey(1) != 27:
    ret_val, img = cap.read()  # чтение кадров из файла
    if not ret_val:  # если конец видио
        print('конец видио')
        break
    resized_now = cv2.resize(img, (img_size[1], img_size[0]))  # Уменьшение размеров файла
    resized_now = resized_now[0:400, 0:450]
    cv2.imshow("Frame", resized_now)  # Вывод измененного изображения на экран
    try:  # Детектировование разметки и её выделение
        canny = an.canny(resized_now)  # Алгоритм canny
        cv2.imshow("Cany1", canny)
        cani_t = an.mask_1(canny)
        cv2.imshow("Cany2", cani_t)
        
        lines = cv2.HoughLinesP(cani_t, 2, np.pi / 180, 100, np.array([()]), minLineLength=20, maxLineGap=5)
        lines_a = an.average_slope_intercept(cani_t, lines)
        lines_d = an.display_lines(cani_t, lines_a)
        combo = cv2.addWeighted(lines_d, 0.8, lines_d, 0.5, 2)
        cv2.imshow("Cany", combo)

        cv2.polylines(combo, [vid_v], True, 500)  # Выделение трапеции на изображении
        cv2.imshow("Polygon", combo) 
        M = cv2.getPerspectiveTransform(vid, vid_p)  # Создание изображения по размерам трапеции
        warped = cv2.warpPerspective(combo, M, (450, img_size[0]), flags=cv2.INTER_LINEAR)
        cv2.imshow("Warped", warped)

        resized_up = warped[0:50, 0:450]  # Первая зона роспознования
        resized_mid = warped[175:225, 0:450]  # Вторая зона распознования
        resized_dofen = warped[350:400, 0:450]  # Третья зона распознования
        # cv2.imshow("resized_up", resized_up)
        # cv2.imshow("resized_mid", resized_mid)
        # cv2.imshow("resized_dofen", resized_dofen)
        Up_histogram = np.sum(resized_up[resized_up.shape[0] // 2:, :, ], axis=0)
        Up_midpoint = Up_histogram.shape[0] // 2
        mid_histogram = np.sum(resized_mid[resized_mid.shape[0] // 2:, :, ], axis=0)
        mid_midpoint = mid_histogram.shape[0] // 2
        dofen_histogram = np.sum(resized_dofen[resized_dofen.shape[0] // 2:, :, ], axis=0)
        dofen_midpoint = dofen_histogram.shape[0] // 2
        # Поиск самых белых сталбцов с лева и справа
        # Нахождения середины между столбцами в трех зонах
        Up_IndWhitestColumnR = np.argmax(Up_histogram[Up_midpoint:]) + Up_midpoint
        if Up_IndWhitestColumnR == 0:
            Up_IndWhitestColumnR = pred_Up_IndWhitestColumnR
        pred_Up_IndWhitestColumnR = Up_IndWhitestColumnR
        Up_sred = int(Up_IndWhitestColumnR - 200)

        mid_IndWhitestColumnR = np.argmax(mid_histogram[mid_midpoint:]) + mid_midpoint
        if mid_IndWhitestColumnR == 0:
            mid_IndWhitestColumnR = pred_mid_IndWhitestColumnR
        pred_mid_IndWhitestColumnR = mid_IndWhitestColumnR
        mid_sred = int(mid_IndWhitestColumnR - 200)

        dofen_IndWhitestColumnR = np.argmax(dofen_histogram[dofen_midpoint:]) + dofen_midpoint
        if dofen_IndWhitestColumnR == 0:
            dofen_IndWhitestColumnR = pred_dofen_IndWhitestColumnR
        pred_dofen_IndWhitestColumnR = Up_IndWhitestColumnR
        dofen_sred = int(dofen_IndWhitestColumnR - 200) 

        combo_visual = np.dstack((warped, warped, warped))  # Создание трех конального изображения
        cv2.circle(combo_visual, (Up_sred, tochka_up), 10, (255, 0, 255))  # Tочка треугольника А
        cv2.circle(combo_visual, (mid_sred, tochka_mid), 10, (0, 0, 255))  # Средняя точка F
        cv2.circle(combo_visual, (dofen_sred, tochka_dowen), 10, (255, 0, 255))  # Tочка треугольника B
        # cv2.imshow("Tochki", warped_visual)
        cv2.line(combo_visual, (Up_sred, tochka_up), (dofen_sred, tochka_dowen), (0, 128, 255), 1)
        cv2.line(combo_visual, (Up_sred, tochka_up), (dofen_sred, tochka_up), (0, 128, 255), 1)
        cv2.line(combo_visual, (dofen_sred, tochka_up), (dofen_sred, tochka_dowen), (0, 128, 255), 1)
        cv2.circle(combo_visual, (dofen_sred, tochka_up), 5, (255, 160, 0))  # Tочка треугольника B1 
        cv2.imshow("Troektoria", combo_visual)  # Создание треугольника для наглядного показа троектории
        abx = dofen_sred - Up_sred
        aby = 350
        cos = np.divide(((abx * 0) + (aby * 400)), (np.sqrt(np.square(abx) + np.square(aby))
                                                    * np.sqrt(np.square(0) + np.square(400))))  # Расчет угла
        ngl = np.degrees(np.arccos(cos))
        otkl = mid_sred - 225
        if Up_sred < dofen_sred:
            ngl = -ngl
        speedL = baz + baz * (ngl / 90) * k_ngl + baz * (otkl / 90) * k_otkl  # Скорость левого мотора
        speedR = baz - baz * (ngl / 90) * k_ngl - baz * (otkl / 90) * k_otkl  # Скорость правого мотора
    except:
        pass
    
    