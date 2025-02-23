import cv2
from ultralytics import YOLO

# Инициализация более точной модели (YOLOv8x)
model = YOLO("yolov8x.pt")  # Используем самую большую доступную версию

# Настройки детекции
CONF_THRESHOLD = 0.6  # Порог уверенности (повышаем для фильтрации ложных срабатываний)
IOU_THRESHOLD = 0.45  # Порог для Non-Maximum Suppression
DETECTION_SIZE = 640  # Размер изображения для обработки (больше = точнее)

# Инициализация фонового субтрактора для лучшего обнаружения движения
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Улучшенное обнаружение движения
    fg_mask = bg_subtractor.apply(frame)

    # Морфологические операции для очистки маски
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)

    # Поиск контуров и фильтрация по размеру
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = any(cv2.contourArea(c) > 1000 for c in contours)  # Только крупные движения

    if motion_detected:
        # Детекция с улучшенными параметрами
        results = model.predict(
            source=frame,
            conf=CONF_THRESHOLD,
            iou=IOU_THRESHOLD,
            imgsz=DETECTION_SIZE,
            classes=[0],  # Только люди
            verbose=False
        )

        # Постобработка результатов
        annotated_frame = results[0].plot()

        # Вывод информации о точности
        for box in results[0].boxes:
            if box.cls == 0:  # Проверка класса 'person'
                conf = box.conf.item()
                cv2.putText(annotated_frame, f"Human: {conf:.2f}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("YOLO Detection", annotated_frame)
    else:
        cv2.imshow("YOLO Detection", frame)

    # Отображение маски движения (опционально)
    cv2.imshow('Motion Mask', fg_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()