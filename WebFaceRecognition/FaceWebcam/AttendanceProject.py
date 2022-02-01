import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

#inisiasi path
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)

#membaca gambar didalam path
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#mencari encoding dari gambar didalam path
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# def markAttendance(name):
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList:
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S')
#             f.writelines(f'\n{name},{dtString}')

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        lines = []
        nameList = []
        dateList = []
        now = datetime.now()
        dtHour = now.strftime('%H:%M:%S')
        dtDay = now.strftime('%m/%d/%Y')
        i=0
        for line in myDataList:
            entry = line.split(',')
            lines.append(entry)
            nameList.append(entry[0])
            if lines[i][0] == name:
                dateList.append(entry[1])
            i+=1

        for i in range(0,len(lines)):
            if name not in nameList:
                f.writelines(f'{name},{dtDay},{dtHour}\n')
            elif lines[i][0] == name and dtDay not in dateList:
                f.writelines(f'{name},{dtDay},{dtHour}\n')
                break
            elif lines[i][0] == name and dtDay in dateList:
                pass

encodeListKnown = findEncodings(images)

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

#mengambil gambar dari webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    #img = captureScreen()

    #resize gambar agar beban sistem menjadi lebih ringan
    #1/4 dari gambar aslinya
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #mencari encoding dari wajah yang ada didalam gambar dari webcam
    #bisa mendeteksi beberapa wajah sekaligus
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            markAttendance(name)
        else:
            name = 'Unknown'
            #print(name)
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)





