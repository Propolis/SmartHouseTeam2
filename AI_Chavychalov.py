import cv2
from ultralytics import YOLO

# Загрузка модели YOLOv11 (замени путь на свою модель, если нужно)
model = YOLO("yolo11n.pt")

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
    # cv2.imshow('Picture', diff)
    prev_frame = frame
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    cv2.imshow('Picture', thresh)

    # Поиск контуров
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Обнаружено движение, запускаем YOLO
        results = model(frame)
        annotated_frame = results[0].plot()  # Аннотированное изображение
        cv2.imshow("YOLO Detection", annotated_frame)
    else:
        cv2.imshow("YOLO Detection", thresh)

    prev_frame = frame.copy()

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(0)