import os
import cv2
import numpy as np
import tensorflow as tf
from threading import Thread, Lock
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Пути к файлам модели YOLOv3-tiny
weights_path = "yolov3-tiny.weights"
model_path = "yolov3-tiny.cfg"
classes_path = "coco.names"

# Загрузка модели YOLOv3-tiny
net = cv2.dnn.readNet(weights_path, model_path)

# Загрузка названий классов
with open(classes_path, "r") as f:
    class_names = f.read().strip().split("\n")

# Индекс класса "человек" в COCO
person_class_id = class_names.index("person")

# Настройка порога уверенности и NMS
confidence_threshold = 0.5  # Порог уверенности (уменьшен)
nms_threshold = 0.4  # Порог для NMS (увеличен)

# Глобальные переменные для многопоточности
frame_lock = Lock()
current_frame = None
processed_frame = None

# Загрузка предобученной модели FaceNet
def load_facenet_model():
    # Загрузка модели FaceNet
    model = tf.keras.models.load_model("facenet_keras.h5", compile=False)
    return model

try:
    model = load_facenet_model()
except Exception as e:
    print(f"Ошибка загрузки модели FaceNet: {e}")
    print("Попробуйте скачать модель заново или использовать другую версию TensorFlow.")
    exit()

# Функция для извлечения эмбеддингов
def get_embedding(model, face_image):
    face_image = face_image.astype("float32")
    face_image = (face_image - 127.5) / 128.0
    face_image = np.expand_dims(face_image, axis=0)
    embedding = model.predict(face_image)
    return embedding[0]

# Загрузка данных
def load_data(data_dir):
    faces = []
    labels = []
    for person_name in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, person_name)
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (160, 160))  # FaceNet требует изображения 160x160
            embedding = get_embedding(model, img)
            faces.append(embedding)
            labels.append(person_name)
    return np.array(faces), np.array(labels)

# Загрузка данных
data_dir = "data"
faces, labels = load_data(data_dir)

# Кодирование меток
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(faces, labels_encoded, test_size=0.2, random_state=42)

# Обучение классификатора (SVM)
classifier = SVC(kernel="linear", probability=True)
classifier.fit(X_train, y_train)

# Оценка точности
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность классификатора: {accuracy * 100:.2f}%")

# Функция для захвата кадров с камеры
def capture_frames():
    global current_frame
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Захваченный кадр сохраняется в глобальную переменную
        with frame_lock:
            current_frame = frame

    cap.release()

# Функция для обработки кадров
def process_frames():
    global processed_frame

    while True:
        with frame_lock:
            if current_frame is None:
                continue
            frame = current_frame.copy()

        # Преобразование кадра в blob (уменьшенный размер 320x320)
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (320, 320), swapRB=True, crop=False)
        net.setInput(blob)

        # Получение результатов обнаружения
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        detections = net.forward(output_layers)

        # Списки для хранения bounding box, уверенностей и классов
        boxes = []
        confidences = []
        class_ids = []

        # Перебор всех обнаруженных объектов
        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Проверка уверенности и класса
                if confidence > confidence_threshold and class_id == person_class_id:
                    # Координаты bounding box
                    box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    (center_x, center_y, box_width, box_height) = box.astype("int")

                    x = int(center_x - (box_width / 2))
                    y = int(center_y - (box_height / 2))

                    # Добавляем bounding box, уверенность и класс в списки
                    boxes.append([x, y, int(box_width), int(box_height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Применение Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

        # Отрисовка прямоугольников после NMS
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                # Обрезаем область лица
                face = frame[y:y + h, x:x + w]
                if face.size == 0:
                    continue

                # Преобразуем лицо для FaceNet
                face_resized = cv2.resize(face, (160, 160))
                embedding = get_embedding(model, face_resized)

                # Предсказание имени
                prediction = classifier.predict([embedding])
                name = label_encoder.inverse_transform(prediction)[0]

                # Отрисовка прямоугольника и имени
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Сохранение обработанного кадра
        with frame_lock:
            processed_frame = frame

# Запуск потоков
capture_thread = Thread(target=capture_frames)
process_thread = Thread(target=process_frames)

capture_thread.start()
process_thread.start()

# Основной цикл для отображения кадров
while True:
    with frame_lock:
        if processed_frame is not None:
            # Отображение обработанного кадра
            cv2.imshow("Real-time Person Detection", processed_frame)

    # Выход по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ожидание завершения потоков
capture_thread.join()
process_thread.join()

# Освобождение ресурсов
cv2.destroyAllWindows()