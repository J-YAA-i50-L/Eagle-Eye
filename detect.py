import cv2
from ultralytics import YOLO

# Загружаем модель
model = YOLO('Autonomous_Division/best (2).pt')

# Окрываем файл с видео
video_path = "IMG_0659.MP4"
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Чтение кадров из видио
    success, frame = cap.read()

    if success:
        # Обработка кадра
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()