import cv2
from ultralytics import YOLO

# Загрузка модели
model = YOLO("yolov8n.pt")  # Или ваша версия модели

# Запуск камеры
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()

# Установите желаемый порог уверенности (0.5-0.7 рекомендуется)
CONFIDENCE_THRESHOLD = 0.7  # <--- Здесь регулируем порог

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Детект движения
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray_prev, gray_current)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Детекция людей с повышенным порогом уверенности
        results = model(frame,
                        classes=[0],  # Только люди
                        conf=CONFIDENCE_THRESHOLD,  # <--- Здесь применяем порог
                        verbose=False)

        # Отображение результатов
        if len(results[0].boxes.cls) > 0:
            annotated_frame = results[0].plot()
            cv2.imshow("YOLO Detection", annotated_frame)
        else:
            cv2.imshow("YOLO Detection", frame)
    else:
        cv2.imshow("YOLO Detection", frame)

    prev_frame = frame.copy()
    cv2.imshow('Motion', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()