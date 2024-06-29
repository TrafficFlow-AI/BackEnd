from speed_track import SpeedTrack
from queue_detection import QueueTrack
from flask import Flask, render_template_string, Response
import time

speed_tracker = SpeedTrack()
queue_manager = QueueTrack()

app = Flask(__name__)

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
    while True:
        time.sleep(1)
        yield f"data: {speed_tracker.json_data}\n\n"

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
    while True:
        time.sleep(1)
        yield f"data: {queue_manager.counts_display}\n\n"
        
if __name__ == '__main__':
    app.run(debug=True)#,host="192.168.111.109")