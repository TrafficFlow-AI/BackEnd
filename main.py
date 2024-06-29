import cv2
from ultralytics import YOLO, solutions

# Cargar el modelo YOLO
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("data/videotrafico.mp4")

assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
print(w,h)
video_writer = cv2.VideoWriter("queue_management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Definir la región de interés (ROI)
queue_region = [(1520, 700), (1470, 320), (1370, 320), (1370, 700)]
#               d inf | d sup               iz. sup | iz. inf
# di - ds-
# is - ii - di - ds

queue = solutions.QueueManager(
    classes_names=model.names,
    reg_pts=queue_region,
    line_thickness=3,
    fontsize=1.0,
    region_color=(255, 144, 31),
)

car_classes = [2, 5, 7]  # Clases correspondientes a coches

while cap.isOpened():
    success, im0 = cap.read()

    if success:
        tracks = model.track(im0, show=False, persist=True, verbose=False, classes=car_classes)  # Solo clases de coches
        out = queue.process_queue(im0, tracks)
        print(f"Esto es el im0: {queue.counts}")
        
        # Dibujar el contador en la parte superior izquierda
        cv2.putText(im0, f'Count: {queue.view_queue_counts}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        video_writer.write(im0)
        cv2.imshow("queue_management", im0)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    print("Video frame is empty or video processing has been successfully completed.")
    break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
