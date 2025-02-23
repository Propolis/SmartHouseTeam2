import cv2
import numpy as np
from ultralytics import YOLO

# Загрузка модели YOLOv8
model = YOLO("yolov8n.pt")

# Классы COCO: 0 - person, 67 - cell phone
TARGET_CLASSES = [0, 67]

# Пороги
PHONE_CONF_THRESHOLD = 0.6  # Порог уверенности для телефона
PHOTO_EDGE_THRESHOLD = 15  # Порог детекции краев на экране
EDGE_PIXEL_RATIO = 0.05  # Минимальный % "активных" пикселей для фото

# Инициализация камеры
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Детекция объектов
    results = model(frame,
                    classes=TARGET_CLASSES,
                    conf=PHONE_CONF_THRESHOLD,
                    verbose=False)

    # Копия кадра для аннотаций
    annotated_frame = results[0].plot()

    # Перебор всех обнаруженных объектов
    for box in results[0].boxes:
        class_id = int(box.cls)
        if class_id == 67:  # Если это телефон
            # Получаем координаты bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Вырезаем область телефона
            phone_roi = frame[y1:y2, x1:x2]

            if phone_roi.size == 0:
                continue

            # Анализ экрана телефона
            try:
                # Уменьшаем размер для быстрой обработки
                roi_resized = cv2.resize(phone_roi, (100, 200))
                gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)

                # Детекция краев
                edges = cv2.Canny(gray, PHOTO_EDGE_THRESHOLD, PHOTO_EDGE_THRESHOLD * 3)

                # Расчет процента "активных" пикселей
                edge_pixels = np.sum(edges > 0)
                total_pixels = edges.size
                edge_ratio = edge_pixels / total_pixels

                # Если достаточно краев - считаем что есть фото
                if edge_ratio > EDGE_PIXEL_RATIO:
                    # Рисуем красную рамку и текст
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, 'Phone with Photo!', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            except:
                pass

    # Отображение результата
    cv2.imshow("Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()