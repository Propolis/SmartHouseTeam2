import torch
import cv2
import numpy as np
from ultralytics import YOLO

VARIANCE_THRESHOLD = 0.08
CONFIDENCE_THRESHOLD = 0.5

def load_models(device):
    """
    Загружаем модели MiDaS и YOLO,
    переводим MiDaS на нужное устройство (YOLO при инициализации автоматически решает, как работать)
    """
    midas = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
    midas = midas.to(device)
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = midas_transforms.dpt_transform

    yolo = YOLO("yolov8n.pt")

    return midas, transform, yolo

def process_frame(frame, midas_model, transform, yolo_model, device):
    """
    Обрабатывает один кадр: оценивает глубину, запускает YOLO,
    рисует рамки и выводит variance/avg_depth
    """
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    input_tensor = torch.from_numpy(img_rgb).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.no_grad():
        depth_pred = midas_model(input_tensor)
        results = yolo_model(frame, classes=[0], conf=CONFIDENCE_THRESHOLD)

    depth_map = depth_pred.squeeze().cpu().numpy()
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-8)

    annotated = frame.copy()

    for box in results[0].boxes.xyxy.cpu().numpy().astype(int):
        x1, y1, x2, y2 = box
        roi_depth = depth_map[y1:y2, x1:x2]

        if roi_depth.size == 0:
            continue

        variance = roi_depth.var()
        avg_depth = roi_depth.mean()

        color = (0, 255, 0)

        if variance < VARIANCE_THRESHOLD:
            color = (0, 0, 255)
            cv2.putText(
                annotated,
                "FAKE",
                (x1, y1 - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        text = f"var={variance:.4f}, avg={avg_depth:.2f}"
        cv2.putText(
            annotated,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

    return annotated

def main():
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"Используется устройство: {device}")

    midas_model, midas_transform, yolo_model = load_models(device)

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось считать кадр с камеры.")
            break

        annotated = process_frame(frame, midas_model, midas_transform, yolo_model, device)

        cv2.imshow("YOLO + Depth Estimation", annotated)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()