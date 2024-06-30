import cv2
from ultralytics import YOLO, solutions
import torch
from src.custom_queue.queue_management import QueueManager
class QueueTrack:
    def __init__(self):
        self.counts_display = 0
            
    def queue_management(self):
        cuda_available = torch.cuda.is_available()
        device = "cuda" if cuda_available else "cpu"
        # Cargar el modelo YOLO
        model = YOLO("yolov10m.pt", verbose=True)
        model.to(device)
        cap = cv2.VideoCapture("data/videotrafico2.mp4")
        assert cap.isOpened(), "Error leyendo el archivo de video"
        
        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        new_w, new_h = w // 2, h // 2  # Nueva resolución a la mitad
        video_writer = cv2.VideoWriter("queue_management_rescaled.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (new_w, new_h))
        print(f"Original resolution: {w}x{h}, Rescaled resolution: {new_w}x{new_h}")
        
        # Definir la región de interés (ROI)
        queue_region = [(1920, 1080), (1920, 980), (1120, 500), (1000, 500), (1450, 1080)]

        queue = QueueManager(
            classes_names=model.names,
            reg_pts=queue_region,
            line_thickness=2,
            fontsize=0.75,
            region_color=(255, 144, 31),
        )

        car_classes = [2, 3, 5, 7]  # Clases correspondientes a coches

        while cap.isOpened():
            success, im0 = cap.read()

            if success:
                im0_rescaled = cv2.resize(im0, (new_w, new_h))
                tracks = model.track(im0_rescaled, show=False, persist=True, verbose=False, classes=car_classes)  # Solo clases de coches
                out = queue.process_queue(im0_rescaled, tracks)

                # Dibujar el contador en la parte superior izquierda
                # cv2.putText(im0, f'Count: {queue.view_queue_counts}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

                ret, buffer = cv2.imencode('.jpg', im0_rescaled)
                frame = buffer.tobytes()
                self.counts_display = queue.counts_display
                yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


        cap.release()
        cv2.destroyAllWindows()
