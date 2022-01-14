import AvtoNet as an
import cv2
import numpy as np
from numpy.lib.type_check import imag
from ctypes.wintypes import CHAR
import serial

mode = 255
speedL = 0
speedR = 0

ser = serial.Serial('COM3', 9600)
D1= str(mode) + "," + str(speedL) + "," + str(speedR)

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

img_size = [400, 900] # Размер изображения с которым мы работаем

vid = np.float32([[0, 260], 
    [450, 260], 
    [420, 120], 
    [20, 120]])

vid_p = np.float32([[0, img_size[0]],
        [450, img_size[0]],
        [450, 0],
        [0, 0]])

vid_v = np.array(vid,dtype = np.int32)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()
            cv2.imshow("CSI Camera", img)
            keyCode = cv2.waitKey(30) & 0xFF  # Stop the program on the ESC key
            if keyCode == 27:
                break            
            if ret_val == False:  # Если кадры кончились программа завершает свою работу
                print('Конец видио')
                break
            resized_now = cv2.resize(img, (img_size[1], img_size[0]))  # Уменьшение размеров файла
            cv2.imshow("Frame", resized_now)  # Вывод измененного изображения на экран
            cv2.polylines(resized_now, [vid_v], True, 500)  # Выделение трапеции на изображении
            cv2.imshow("Polygon", resized_now) 
            M = cv2.getPerspectiveTransform(vid, vid_p)  # Создание изображения по размерам трапеции
            warped = cv2.warpPerspective(resized_now, M, (450, img_size[0]), flags = cv2.INTER_LINEAR)
            cv2.imshow("Warped", warped)
            try:  # Детектировование разметки и её выделение
                canny = an.canny(warped)  # Алгоритм canny
                lines = cv2.HoughLinesP(canny, 2, np.pi/180, 100, np.array([()]), minLineLength=20, maxLineGap=5)
                lines_a = an.average_slope_intercept(canny, lines)
                lines_d = an.display_lines(canny, lines_a)
                combo = cv2.addWeighted(lines_d, 0.8, lines_d, 0.5, 1)
                cv2.imshow("Cany", combo)
            except:
                pass
            resized_up = combo[0:50,0:450]  # Первая зона роспознования
            resized_mid = combo[175:225,0:450]  # Вторая зона распознования
            resized_dofen = combo[350:400,0:450]  # Третья зона распознования                  
            #cv2.imshow("resized_up", resized_up)
            #cv2.imshow("resized_mid", resized_mid)
            #cv2.imshow("resized_dofen", resized_dofen)
            Up_histogram = np.sum(resized_up[resized_up.shape[0] // 2:,:,], axis=0)
            Up_midpoint = Up_histogram.shape[0] // 2
            mid_histogram = np.sum(resized_mid[resized_mid.shape[0] // 2:,:,], axis=0)
            mid_midpoint = mid_histogram.shape[0] // 2
            dofen_histogram = np.sum(resized_dofen[resized_dofen.shape[0] // 2:,:,], axis=0)
            dofen_midpoint = dofen_histogram.shape[0] // 2
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

            dofen_IndWhitestColumnL = np.argmax(dofen_histogram[:dofen_midpoint])
            if dofen_IndWhitestColumnL == 0:
                dofen_IndWhitestColumnL = pred_dofen_IndWhitestColumnL
            pred_dofen_IndWhitestColumnL = dofen_IndWhitestColumnL
            dofen_IndWhitestColumnR = np.argmax(dofen_histogram[dofen_midpoint:]) + dofen_midpoint
            if dofen_IndWhitestColumnR == 0:
                dofen_IndWhitestColumnR = pred_dofen_IndWhitestColumnR
            pred_dofen_IndWhitestColumnR = Up_IndWhitestColumnR
            
            dofen_sred = int((dofen_IndWhitestColumnL + dofen_IndWhitestColumnR) / 2)                        
            combo_visual = np.dstack((combo, combo, combo))  # Создание трех конального изображения
            cv2.circle(combo_visual, (Up_sred, tochka_up),10, (255, 0, 255))  # Tочка треугольника А
            cv2.circle(combo_visual, (mid_sred, tochka_mid),10, (0, 0, 255))  # Средняя точка F
            cv2.circle(combo_visual, (dofen_sred, tochka_dowen),10, (255, 0, 255)) # Tочка треугольника B
            #cv2.imshow("Tochki", warped_visual)
            cv2.line(combo_visual, (Up_sred, tochka_up), (dofen_sred, tochka_dowen),(0, 128, 255), 1)
            cv2.line(combo_visual, (Up_sred, tochka_up), (dofen_sred, tochka_up),(0, 128, 255), 1)
            cv2.line(combo_visual, (dofen_sred, tochka_up), (dofen_sred, tochka_dowen),(0, 128, 255), 1)
            cv2.circle(combo_visual, (dofen_sred, tochka_up), 5, (255, 160, 0))  # Tочка треугольника B1 
            cv2.imshow("Troektoria", combo_visual)  # Создание треугольника для наглядного показа троектории
            abx = dofen_sred - Up_sred
            aby = 350
            cos = np.divide(((abx * 0) + (aby * 400)), (np.sqrt(np.square(abx) + np.square(aby)) * np.sqrt(np.square(0) + np.square(400))))  # Расчет угла  
            ngl = np.degrees(np.arccos(cos))
            otkl = mid_sred - 225
            if Up_sred < dofen_sred:
                ngl = -ngl
            speedL = baz + baz * (ngl / 90 ) * k_ngl + baz * (otkl / 90 ) * k_otkl  # Скорость левого мотора
            speedR = baz - baz * (ngl / 90 ) * k_ngl - baz * (otkl / 90 ) * k_otkl  # Скорость правого мотора
            # Передача данных 
            D1 =str(mode) + "," + str(speedL) + "," + str(speedR)
            b1 = bytes(D1, encoding='utf-8')
            ser.write(b1)
            print(ser.readline())
        cap.release()       
    else:
        print("Не удалось открыть камеру")
if __name__ == "__main__":
    show_camera()