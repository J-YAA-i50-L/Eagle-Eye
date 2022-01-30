import cv2
import numpy as np


def gray_filtr(img):  # ToDo:фильт темно-серого цвета
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # наложение серого фильтра
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)
    img = increase_brightness(gray_img, value=31)
    return img


def increase_brightness(img, value=30):  # ToDo:затемнение
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] -= value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def canny(img):  # ToDo:оператор Canny
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    return cv2.Canny(blur, 50, 100)


def make_coordinates(image, line_parameters): # для координат
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (0.7))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):

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
        left_line = make_coordinates(image, left_fit_average)
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_average)
        return np.array([left_line, right_line])


def display_lines(image, lines):  # Todo:
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 8)
    return line_image


def display_lines_dem(image, lines): # Todo:
    line_image = np.zeros_like(image)
    if lines is not None:
        n = 1
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 128, 255), 9)
            """if n == 1:
                n += 1
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 128, 255), 8)
            else:
                contours = np.array([[x1, y1], [x2, y2], [x2 - (x1 - x2) // 2, y2], [x1 - x2, y1]])
                cv2.fillPoly(line_image, pts=[contours], color=(255, 160, 0), lineType=8, shift=0, offset=None)
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 128, 255), 8)"""
    return line_image


def mask_1(image):
    height = image.shape[0]
    polygons = np.array([(200 - 10, height // 1.4), (450 - 150, height // 1.4), (450, 400), (40, 400)])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def mask_2(image):
    height = image.shape[0]
    polygons = np.array([(160, height // 1.4), (450 - 110, height // 1.4), (450, 400), (40, 400)])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def demonstrat(image):
    try:
        cany = canny(image)  # Алгоритм canny
        cany = mask_1(cany)
        lines = cv2.HoughLinesP(cany, 2, np.pi / 180, 90, np.array([()]), minLineLength=20, maxLineGap=20)
        lines_a = average_slope_intercept(cany, lines)
        lines_d = display_lines_dem(image, lines_a)
        combo = cv2.addWeighted(image, 0.8, lines_d, 0.8, 2)
        return combo
    except:
        pass
