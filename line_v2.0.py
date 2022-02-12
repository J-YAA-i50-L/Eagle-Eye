import numpy as np
import cv2
import AvtoNet as an

img_size = [400, 900]  # Размер изображения с которым мы работаем

point_up = 25
point_mid = int(400 / 2)
point_down = 400 - point_up

baz = 60
k_ngl = 1
k_deviation = 1

pred_Up_IndWhitestColumnL = 0
pred_mid_IndWhitestColumnL = 0
pred_down_IndWhitestColumnL = 0

pred_Up_IndWhitestColumnR = 0
pred_mid_IndWhitestColumnR = 0
pred_down_IndWhitestColumnR = 0

mode = 255
speedL = 0
speedR = 0

vid = np.float32([[40, 400],
                  [450, 400],
                  [355, 320],
                  [125, 320]])

vid_p = np.float32([[0, img_size[0]],
                    [450, img_size[0]],
                    [450, 0],
                    [0, 0]])

vid_v = np.array(vid, dtype=np.int32)

cap = cv2.VideoCapture(r"c:/Python/python by/GAZ.py/road_Trim1.mp4")

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

    # cv2.imshow("Video", resized_now)  # Вывод измененного изображения на экран

    gray_img = an.gray_filtr(resized_now)

    # cv2.imshow("Video", gray_img)

    try:
        canny = an.canny(gray_img)  # Алгоритм canny

        # cv2.imshow("Cany1", canny)

        canny_t = an.mask_1(canny)

        cv2.imshow("Canny_2", canny_t)

        lines = cv2.HoughLinesP(canny_t, 2, np.pi / 180, 90, np.array([()]), minLineLength=15, maxLineGap=5)
        lines_a = an.average_slope_intercept(canny_t, lines)
        lines_d = an.display_lines(canny_t, lines_a)
        combo = cv2.addWeighted(lines_d, 0.8, lines_d, 0.5, 2)
        combo = an.mask_2(combo)

        cv2.imshow("Cany", combo)

        dem = an.demonstrat(resized_now)

        cv2.imshow("DEM", dem)

        cv2.polylines(combo, [vid_v], True, 500)  # Выделение трапеции на изображении

        cv2.imshow("Polygon", combo)

        M = cv2.getPerspectiveTransform(vid, vid_p)  # Создание изображения по размерам трапеции
        warped = cv2.warpPerspective(combo, M, (450, img_size[0]), flags=cv2.INTER_LINEAR)

        # cv2.imshow("Warped", warped)

        resized_up = warped[0:50, 0:450]  # Первая зона роспознования
        resized_mid = warped[175:225, 0:450]  # Вторая зона распознования
        resized_down = warped[350:400, 0:450]  # Третья зона распознования

        # cv2.imshow("resized_up", resized_up)
        # cv2.imshow("resized_mid", resized_mid)
        # cv2.imshow("resized_down", resized_down)

        Up_histogram = np.sum(resized_up[resized_up.shape[0] // 2:, :, ], axis=0)
        Up_midpoint = Up_histogram.shape[0] // 2

        mid_histogram = np.sum(resized_mid[resized_mid.shape[0] // 2:, :, ], axis=0)
        mid_midpoint = mid_histogram.shape[0] // 2

        down_histogram = np.sum(resized_down[resized_down.shape[0] // 2:, :, ], axis=0)
        down_midpoint = down_histogram.shape[0] // 2

        # Поиск самых белых сталбцов с лева и справа
        # Нахождения середины между столбцами в трех зонах

        Up_IndWhitestColumnL = np.argmax(Up_histogram[:Up_midpoint])
        if Up_IndWhitestColumnL == 0:
            Up_IndWhitestColumnL = pred_Up_IndWhitestColumnL
        pred_Up_IndWhitestColumnL = Up_IndWhitestColumnL
        Up_IndWhitestColumnR = np.argmax(Up_histogram[Up_midpoint:]) + Up_midpoint
        if Up_IndWhitestColumnR == 0:
            Up_IndWhitestColumnR = pred_Up_IndWhitestColumnR
        pred_Up_IndWhitestColumnR = Up_IndWhitestColumnR
        Up_sred = int((Up_IndWhitestColumnL + Up_IndWhitestColumnR) / 2)

        mid_IndWhitestColumnL = np.argmax(mid_histogram[:mid_midpoint])
        if mid_IndWhitestColumnL == 0:
            mid_IndWhitestColumnL = pred_mid_IndWhitestColumnL
        pred_mid_IndWhitestColumnL = mid_IndWhitestColumnL
        mid_IndWhitestColumnR = np.argmax(mid_histogram[mid_midpoint:]) + mid_midpoint
        if mid_IndWhitestColumnR == 0:
            mid_IndWhitestColumnR = pred_mid_IndWhitestColumnR
        pred_mid_IndWhitestColumnR = mid_IndWhitestColumnR
        mid_sred = int((mid_IndWhitestColumnL + mid_IndWhitestColumnR) / 2)

        down_IndWhitestColumnL = np.argmax(down_histogram[:down_midpoint])
        if down_IndWhitestColumnL == 0:
            down_IndWhitestColumnL = pred_down_IndWhitestColumnL
        pred_down_IndWhitestColumnL = down_IndWhitestColumnL
        down_IndWhitestColumnR = np.argmax(down_histogram[down_midpoint:]) + down_midpoint
        if down_IndWhitestColumnR == 0:
            down_IndWhitestColumnR = pred_down_IndWhitestColumnR
        pred_down_IndWhitestColumnR = Up_IndWhitestColumnR
        down_sred = int((down_IndWhitestColumnL + down_IndWhitestColumnR) / 2)

        combo_visual = np.dstack((warped, warped, warped))  # Создание трех конального изображения
        cv2.circle(combo_visual, (Up_sred, point_up), 10, (255, 0, 255))  # Tочка треугольника А
        cv2.circle(combo_visual, (mid_sred, point_mid), 10, (0, 0, 255))  # Средняя точка F
        cv2.circle(combo_visual, (down_sred, point_down), 10, (255, 0, 255))  # Tочка треугольника B
        cv2.circle(combo_visual, (down_sred, point_up), 5, (255, 160, 0))  # Tочка треугольника B1

        # cv2.imshow("Tochki", warped_visual)

        cv2.line(combo_visual, (Up_sred, point_up), (down_sred, point_down), (0, 128, 255), 1)
        cv2.line(combo_visual, (Up_sred, point_up), (down_sred, point_up), (0, 128, 255), 1)
        cv2.line(combo_visual, (down_sred, point_up), (down_sred, point_down), (0, 128, 255), 1)

        cv2.imshow("Troektoria", combo_visual)  # Создание треугольника для наглядного показа троектории

        abx = down_sred - Up_sred
        aby = 350

        cos = np.divide(((abx * 0) + (aby * 400)), (
                np.sqrt(np.square(abx) + np.square(aby)) * np.sqrt(np.square(0) + np.square(400))))  # Расчет угла

        ngl = np.degrees(np.arccos(cos))
        if ngl <= 3.0:
            ngl = 0

        deviation = mid_sred - 225

        if Up_sred < down_sred:
            ngl = -ngl

        speedL = int(baz + baz * (ngl / 90) * k_ngl + baz * (deviation / 90) * k_deviation)  # Скорость левого мотора
        if speedL < 10:
            speedL = 10

        speedR = int(baz - baz * (ngl / 90) * k_ngl - baz * (deviation / 90) * k_deviation)  # Скорость правого мотора
        if speedR < 10:
            speedR = 10

        print(speedL, '\t|\t', speedR, '\t')

    except:
        pass
