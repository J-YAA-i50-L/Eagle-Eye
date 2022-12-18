import cv2
import numpy as np
from numpy.lib.function_base import copy
from GreenEye import Eagle
# Подключение дополнительных модулей

img_size = [400, 450]
height = img_size[0]
width = img_size[1]
polygons = np.array([(width // 2 - 80, height // 1.4), (width // 2 + 80, height // 1.4),
                     (width, height), (0, height)])
masks = np.float32([(width // 2 - 80, height // 1.4), (width // 2 + 80, height // 1.4),
                    (width, height), (0, height)])
masks_transfotm = np.array(masks, dtype=np.int32)
vid = np.float32([[0, img_size[0]],
                 [450, img_size[0]],
                 [450, 0], [0, 0]])

cap = cv2.VideoCapture(r"road_Trim1.mp4")

if not cap.isOpened():
    print('не найдени файл')
    exit()

while cv2.waitKey(1) != 27:
    reading = val, img = cap.read()  # Чтение кадров
    if not val:  # Если кадры кончились
        print('Работа завершена')
        exit()
    try:
        Eagle(reading, polygons, masks, masks_transfotm)  # Создаем класс Eagle
    except:
        pass

