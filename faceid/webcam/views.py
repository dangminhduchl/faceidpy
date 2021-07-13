# from unittest.test import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import sqlite3
import os


def index(request):
    return render(request, 'index.html')



def getProfile(id):
    conn = sqlite3.connect("FaceBaseNew.db")
    cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(id))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile



def stream():
    cap = cv2.VideoCapture(0)
    # Khởi tạo bộ phát hiện khuôn mặt
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    num_img = 0
    frame_count = 0

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

            if (num_img < 10) and (frame_count % 10 == 0):
                file = open("./InputImage/InputImage" + str(num_img) + ".txt", "wb")
                # mã hoá chán chê rồi save file txt rồi gửi file

                np.save(file, frame)
                num_img += 1
                print("num_img: " + str(num_img))

                # nhan dang danh tinh
                if os.path.isfile("./InputImage/InputImage" + str(num_img) + ".txt"):
                    file = open("./InputImage/InputImage" + str(num_img) + ".txt", "rb")
                    img = np.load(file)
                    img = cv2.resize(img, (480, 270))
                    # giải mã

                    # Khởi tạo bộ phát hiện khuôn mặt
                    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

                    # Khởi tạo bộ nhận diện khuôn mặt
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read('recognizer/trainner.yml')
                    # Chuyển ảnh về xám
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # Phát hiện các khuôn mặt trong ảnh camera
                    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                    # print(faces)

                    # Lặp qua các khuôn mặt nhận được để hiện thông tin
                    for (x, y, w, h) in faces:

                        # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (dộ sai khác)
                        id, dist = recognizer.predict(gray[y:y + h, x:x + w])

                        # Nếu độ sai khác < 25% thì lấy profile
                        if (dist <= 25):
                            profile = getProfile(id)
                            print(str(profile[0]))
                            # vao trang ca nhan
                        else:
                            if (frame_count % 10 == 0) and (frame_count < 400):
                                print("unknown")
                                # Thong bao khuon mat chua dc xac dinh
                                break
                            if frame_count >= 400:
                                print("Time Out")
                                cap.release()
                                break
                                # out ra trang dang nhap
            # Vẽ hình chữ nhật quanh mặt
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        frame_count += 1
        print(frame_count)

        img_show = cv2.resize(frame, (720, 405))
        #cv2.imshow("img_show", img_show)
        cv2.imwrite('./show.jpg', img_show)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('show.jpg', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
