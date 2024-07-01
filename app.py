from speed_track import SpeedTrack
from queue_detection import QueueTrack
from flask import Flask, render_template_string, Response
from flask_cors import CORS

# make directori data
import os
os.makedirs("data", exist_ok=True)

import time
import json

# download video of google drive
import gdown

# comprobar si existe data/videotrafico.mp4
if os.path.exists("data/videotrafico.mp4"):
    print("El archivo 'data/videotrafico.mp4' ya existe.")
else:
    url = "https://drive.google.com/file/d/1KEFYs9bs7-MdMTpsVRflW9Ql7N4nPYaN/view?usp=sharing"
    output = "data/videotrafico.mp4"
    gdown.download(url, output, fuzzy=True)
    
if os.path.exists("data/videotrafico2.mp4"):
    print("El archivo 'data/videotrafico2.mp4' ya existe.")
else:
    url_1 = "https://drive.google.com/file/d/1KEYciT7TmfMvD388O3hrUmJF3UMuXk3i/view?usp=sharing"
    output_1 = "data/videotrafico2.mp4"
    gdown.download(url, output_1, fuzzy=True)

speed_tracker = SpeedTrack()
queue_manager = QueueTrack()

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/speed_estimation')
def speed_estimation():
    """
    Route decorator for the '/speed_estimation' endpoint.
    Returns a response with the speed data obtained from the `speed_tracker` object.
    The response is in the format of 'multipart/x-mixed-replace; boundary=frame'.
    """
    return Response(speed_tracker.get_speed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_speed_data')
def get_speed_data():
    """
    A route handler function that continuously yields the latest `json_data` from the `speed_tracker` object.

    Returns:
        A generator that yields the latest `json_data` as a string in the format "data: {json_data}".
    """
    def generate():
        while True:
            time.sleep(1)
            yield f"data: {speed_tracker.json_data}\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/queue_detection')
def queue_detection():
    """
    A route handler function for the '/queue_detection' endpoint.

    This function returns a Flask Response object that contains the output of the `queue_management` method
    of the `queue_manager` object. The output is in the format of 'multipart/x-mixed-replace; boundary=frame'.

    Returns:
        A Flask Response object containing the output of the `queue_management` method.
    """
    return Response(queue_manager.queue_management(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_queue_data')
def get_queue_data():
    """
    A route handler function that continuously yields the latest `json_data` from the `speed_tracker` object.

    Returns:
        A generator that yields the latest `json_data` as a string in the format "data: {json_data}".
    """
    def generate():
        while True:
            time.sleep(1)
            count = queue_manager.counts_display

            json_data = {
                'counts': count}
            json_data_1 = json.dumps(json_data)
            yield f"data: {json_data_1}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)