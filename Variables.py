import numpy as np

# Переменные
img_size = [450, 400]  # Размер изображения с которым мы работаем

point_up = 25
point_mid = int(400 / 2)
point_down = 400 - point_up

baz = 120
k_ngl = 1
k_deviation = 0

pred_Up_IndWhitestColumnL = 0
pred_mid_IndWhitestColumnL = 0
pred_down_IndWhitestColumnL = 0

flag_line = False

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

