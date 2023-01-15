import cv2
import tensorflow as tf
import logging
import numpy as np
from datetime import datetime, timedelta

model = tf.keras.models.load_model('sqeezenet_3.h5', compile=False)
# capture frames from a camera with device index=0


def setka(cap):
    """Распознование цифр с карточек"""
    result1 = np.zeros((1, 1, 5))
    i = 0
    start_time = datetime.now()
    # loop runs if capturing has been initialized
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (160, 160))
        frame = frame.astype('float32') / 255.0
        frame1 = frame.reshape(1, 160, 160, 1)
        result = model.predict(frame1, verbose=0)
        cv2.imshow('Camera', frame)
        i += 1
        result1 += result
        if (datetime.now() - start_time) > timedelta(seconds=1) or i > 4:
            start_time = datetime.now()
            result1 = np.zeros((1, 1, 5))
            i = 0
        if float(result1.max()) > 3.5:
            result0 = result1.argmax() + 1
            break
            result1 = np.zeros((1, 1, 5))
            i = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return int(result0)
