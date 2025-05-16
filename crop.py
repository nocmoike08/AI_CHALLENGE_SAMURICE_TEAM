import cv2
import os
from ultralytics import YOLO
from datetime import datetime
model = YOLO(r"C:\Users\PC\Documents\Zalo Received Files\project-6-at-2025-05-15-11-51-8c159b71\runs\detect\train2\weights\best.pt")
input_folder = r"C:\Users\PC\Documents\Zalo Received Files\test"
output_folder = "Canteen_Crops"
os.makedirs(output_folder, exist_ok=True)
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    frame = cv2.imread(img_path)
    results = model(frame)[0]
    for i, box in enumerate(results.boxes.xyxy.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)
        crop = frame[y1:y2, x1:x2]
        label_id = int(results.boxes.cls[i])
        label_name = model.names[label_id]
        label_folder = os.path.join(output_folder, label_name)
        os.makedirs(label_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        save_path = os.path.join(label_folder, f"{label_name}_{timestamp}.jpg")
        cv2.imwrite(save_path, crop)
print("Done cropping & saving.")

