from flask import Flask, Response
from flask_cors import CORS
import cv2
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    if not cap.isOpened():
        logging.error("Cannot open camera")
        return

    while True:
        success, frame = cap.read()
        if not success:
            logging.error("Failed to grab frame")
            break

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            logging.error("Failed to encode frame")
            break
        frame = buffer.tobytes()

        # Yield frame in the format required for MJPEG streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    logging.info("Video feed requested")
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    logging.info("Starting Flask server")
    app.run(host='0.0.0.0', port=5000)
