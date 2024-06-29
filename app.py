from speed_track import get_speed
from queue_detection import queue_management
from flask import Flask, render_template, Response

app = Flask(__name__)
    
@app.route('/speed_estimation')
def speed_estimation():
    return Response(get_speed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/queue_detection')
def queue_detection():
    return Response(queue_management(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)