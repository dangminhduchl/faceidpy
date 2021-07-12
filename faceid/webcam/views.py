from unittest.test import loader
import cv2
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
def index(request):
    return render(request,'index.html')

def stream():
    cap = cv2.VideoCapture(0)
    # Khởi tạo bộ phát hiện khuôn mặt
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    num_img = 1

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break
        # Chuyển ảnh sang màu xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        # print(faces)

        # Lặp qua các khuôn mặt nhận được để hiện thông tin
        for (x, y, w, h) in faces:
            print(num_img)
            if num_img <= 10:
                file = open("./InputImage/InputImage" + str(num_img) + ".txt", "wb")
                # mã hoá chán chê rồi save file txt rồi gửi file

                np.save(file, frame)
                num_img += 1
            # Vẽ hình chữ nhật quanh mặt
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')