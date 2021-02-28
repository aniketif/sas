import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

rec=cv2.createLBPHFaceRecognizer();
rec.load("recognizer/trainningData.yml")
cascadePath="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataDet'

def getProfile(id):
    conn=sqlite3.connect("Facebase.db")
    cmd="SELECT * FROM People WHERE Roll="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile



cam=cv2.VideoCapture(0);
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX,1,1,0,1,1)
an="no match"
while True:
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        id, conf=rec.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        profile=getProfile(id)
        if(profile!=None):
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[0]),(x,y+h+30),font,255);
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+60),font,255);
        else:
            cv2.cv.PutText(cv2.cv.fromarray(img),str(an),(x,y,+h+30),font,255);
    cv2.imshow("Face",img);
    cv2.waitKey(10)
