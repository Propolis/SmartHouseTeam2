import cv2
from ultralytics import YOLO

# Загрузка модели YOLO (убедитесь, что используете правильную версию модели)
model = YOLO("yolov8n.pt")  # Используйте актуальное имя модели

# Запуск камеры
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Конвертация в серый и вычисление разницы
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray_prev, gray_current)
    prev_frame = frame.copy()

    # Пороговая обработка
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Поиск контуров движения
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Детекция только людей (класс 0 в COCO)
        results = model(frame, classes=[0], verbose=False)  # verbose=False отключает логирование

        # Отображение результатов только если есть обнаруженные люди
        if len(results[0].boxes.cls) > 0:
            annotated_frame = results[0].plot()
            cv2.imshow("YOLO Detection", annotated_frame)
        else:
            # Если люди не найдены, показать пустой кадр
            cv2.imshow("YOLO Detection", frame)
    else:
        # Если движения нет, показать исходный кадр
        cv2.imshow("YOLO Detection", frame)

    # Отображение окна с движением (опционально)
    cv2.imshow('Motion Threshold', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()