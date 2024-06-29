from speed_track import SpeedTrack
from queue_detection import queue_management
from flask import Flask, render_template_string, Response
import time
speed_tracker = SpeedTrack()
app = Flask(__name__)

@app.route('/speed_estimation')
def speed_estimation():
    return Response(speed_tracker.get_speed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_speed_data')
def get_speed_data():
    while True:
        time.sleep(1)
        yield f"data: {speed_tracker.json_data}\n\n"

@app.route('/queue_detection')
def queue_detection():
    return Response(queue_management(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)