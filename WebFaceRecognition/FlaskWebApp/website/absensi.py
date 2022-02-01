# from flask import Blueprint
# #import library
# from flask import Flask, render_template, Response
# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime

# absensi = Blueprint('absensi', __name__)

# #inisiasi path
# path = 'D:\kampusmerdeka\FaceRecognition\FlaskWebApp\website\static\images\ImagesAttendance'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(os.getcwd())

# #membaca gambar didalam path
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])

# #mencari encoding dari gambar didalam path
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

# #fungsi untuk mencatat kehadiran
# def markAttendance(name):
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         lines = []
#         nameList = []
#         dateList = []
#         now = datetime.now()
#         dtHour = now.strftime('%H:%M:%S')
#         dtDay = now.strftime('%m/%d/%Y')
#         i=0
#         for line in myDataList:
#             entry = line.split(',')
#             lines.append(entry)
#             nameList.append(entry[0])
#             if lines[i][0] == name:
#                 dateList.append(entry[1])
#             i+=1

#         for i in range(0,len(lines)):
#             if name not in nameList:
#                 f.writelines(f'{name},{dtDay},{dtHour}\n')
#                 break
#             elif lines[i][0] == name and dtDay in dateList:
#                 pass    
#             elif lines[i][0] == name and dtDay not in dateList:
#                 f.writelines(f'{name},{dtDay},{dtHour}\n')
#                 break

# encodeListKnown = findEncodings(images)

# #mengakses kamera/webcam
# camera = cv2.VideoCapture(0)

# def gen_frames():  
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             frameS = cv2.resize(frame,(0,0),None,0.25,0.25)
#             frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)

#             #mencari encoding dari wajah yang ada didalam gambar dari webcam
#             #bisa mendeteksi beberapa wajah sekaligus
#             facesCurFrame = face_recognition.face_locations(frameS)
#             encodesCurFrame = face_recognition.face_encodings(frameS,facesCurFrame)

#             for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
#                 matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
#                 faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
#                 # print(faceDis)
#                 matchIndex = np.argmin(faceDis)

#                 if matches[matchIndex]:
#                     name = classNames[matchIndex].upper()
#                     markAttendance(name)
#                 else:
#                     name = 'Unknown'
#                     #print(name)
#                 y1,x2,y2,x1 = faceLoc
#                 y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#                 cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
#                 cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#                 cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @absensi.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @absensi.route('/absensi')
# def absensi():
#     return render_template("absensi.html")