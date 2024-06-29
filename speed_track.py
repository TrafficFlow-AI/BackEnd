import cv2
from ultralytics import YOLO, solutions
from src.custom_speed.speed_estimation import SpeedEstimator
import torch
import json
class SpeedTrack:
    def __init__(self):
        pass
    def get_speed(self):
        # Verificar la disponibilidad de CUDA para usar GPU
        cuda_available = torch.cuda.is_available()
        device = "cuda" if cuda_available else "cpu"

        # Inicializar el modelo YOLO
        model = YOLO("yolov10n.pt", verbose=True)
        model.to(device)
        names = model.names

        # Abrir el archivo de video
        cap = cv2.VideoCapture("data/VID-20240628-WA0023.mp4")
        assert cap.isOpened(), "Error leyendo el archivo de video"

        # Obtener las dimensiones del video y los fps
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        # Crear el video writer
        video_writer = cv2.VideoWriter("speed_estimation.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        # Definir las líneas de detección de velocidad
        line_pts_2 = [(0, 600), (1500, 600)]

        # Inicializar los objetos de estimación de velocidad
        speed_obj_2 = SpeedEstimator(reg_pts=line_pts_2, names=names, view_img=True)
        
        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                print("El frame del video está vacío o el procesamiento del video ha sido completado.")
                break
            # Realizar la detección y seguimiento de objetos con YOLO
            tracks = model.track(im0, persist=True, show=False, tracker="bytetrack.yaml", classes=[2,3, 5, 7])

            # Estimar la velocidad en ambas mitadesç
            frame = speed_obj_2.estimate_speed(im0, tracks, region_color=(255, 255, 255))
            df = speed_obj_2.df_speed
            df_json = df.to_json(orient='records')
            self.json_data = json.dumps(df_json).encode('utf-8')
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
        cap.release()
        cv2.destroyAllWindows()