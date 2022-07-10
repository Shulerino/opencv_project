from flask import Flask, render_template, Response
import cv2
from pathlib import Path


app = Flask(__name__)




video_array=[]
files=Path("./videos").glob("*.mp4")
for file in files:
    camera=cv2.VideoCapture(str(file))
    video_array.append(camera)


#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)


def gen_frames(camera):  # generate frame by frame from camera
    while True:
        frames_preview=[]
        success, frame = camera.read()
        if not success:
            break
        else:
            grey_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small_frame=cv2.resize(grey_frame, (100, 100), fx=0.5, fy=0.5)
            itog_frame = cv2.imencode('.jpg', small_frame)[1].tobytes()
            frames_preview.append(itog_frame)
            for fr in frames_preview:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + fr + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed<int:number>')
def video_feed(number):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(video_array[number-1]), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)