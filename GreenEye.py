from numpy.lib.function_base import copy
import cv2
import numpy as np

img_size = [200 * 2, 450 * 2]  # Размер изображения с которым мы работаем


class Eagle:
    def __init__(self, tuple, polygons, masks, masks_t):
        self.shot, self.image = tuple
        self.polygons = polygons
        self.coords_trapezoid = masks
        self.vid_trapezoid = masks_t
        # self.vid_above = vid
        # Уменьшаем изображение согласно нужным размерам
        self.image = cv2.resize(self.image, (img_size[1], img_size[0]))
        self.image = self.image[0:250 * 2, 0:225 * 2]
        self.nest()

    def nest(self):
        cv2.imshow('image', self.image)
        self.image = self.canny(self.image)
        self.image = self.masks_canny_privat(self.image)
        cv2.polylines(self.image, [self.vid_trapezoid], True, 500)  # Выделение трапеции на изображении
        cv2.imshow('Canny', self.image)
        # M = cv2.getPerspectiveTransform(vid, vid_p)  # Создание изображения по размерам трапеции
        # warped = cv2.warpPerspective(combo, M, (450, img_size[0]), flags=cv2.INTER_LINEAR)
        # cv2.imshow("Warped", warped)

    def canny(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        return cv2.Canny(blur, 50, 100)

    def masks_canny_privat(self, image):  # Выделяем линии дорожной разметки, выделение трапеции
        polygons = self.polygons
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
        masked_image = cv2.bitwise_and(image, mask)
        lines = cv2.HoughLinesP(masked_image, 2, np.pi / 180, 100, np.array([()]), minLineLength=20, maxLineGap=5)
        lines_a = self.average_slope_intercept(masked_image, lines)
        lines_d = self.display_lines(masked_image, lines_a)
        masked_image = cv2.addWeighted(lines_d, 0.8, lines_d, 0.5, 2)
        return masked_image

    def average_slope_intercept(self, image, lines):
        left_fit = []
        right_fit = []
        while lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    left_fit.append((slope, intercept))
                else:
                    right_fit.append((slope, intercept))
            left_fit_average = np.average(left_fit, axis=0)
            left_line = self.make_coordinates(image, left_fit_average)
            right_fit_average = np.average(right_fit, axis=0)
            right_line = self.make_coordinates(image, right_fit_average)
            return np.array([left_line, right_line])

    def display_lines(self, image, lines):  # Todo:
        line_image = np.zeros_like(image)
        if lines is not None:
            for x1, y1, x2, y2 in lines:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 8)
        return line_image

    def make_coordinates(self, image, line_parameters):  # для координат
        slope, intercept = line_parameters
        y1 = image.shape[0]
        y2 = int(y1 * 0.7)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])
