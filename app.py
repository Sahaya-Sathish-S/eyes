from flask import Flask, render_template, Response
import cv2
from detector import detect_eye

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame, eyes = detect_eye(frame)

        if eyes >= 2:
            result = "Eyes Detected"
        else:
            result = "No Eyes"

        cv2.putText(frame, result, (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0),2)

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)