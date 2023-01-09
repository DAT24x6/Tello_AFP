import socket
import time
import sys
import cv2
import numpy
#import subprocess
import tkinter as tk
from tkinter import ttk
import datetime

#UDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.10.1", 8889)

#映像受信
socket.sendto("streamon".encode("UTF-8"), address)

#学習データ読み込み
cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
#cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
#cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")

capture = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1") #UDP受け取り用
#capture = cv2.VideoCapture(0) #パソコン内蔵カメラ

while(True):
    let, frame = capture.read()
    resize_frame = cv2.resize(frame, dsize=(256,144)) #1280x720 #640x480

    #グレースケール変換
    gray_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)

    #検出
    face = cascade.detectMultiScale(gray_frame)
    print(len(face))


    #四角をつける
    for x, y, w, h in face:
        cv2.rectangle(gray_frame, (x, y), (x + w, y + h), (255, 255, 255), thickness=1)
        cv2.rectangle(gray_frame, (w // 2, h // 2), (w // 2 + 1, h // 2 + 1), (255, 255, 255), thickness=-1)
        #NEXT→中心点を描画する、ドローンの動きに反映させる。


    if len(face) == 0:
        pass
    elif len(face[0]) == 4:
        x, y, width, height = face[0]
    #faceは二次元配列だった。
    

    #顔認識の中心座標
    face_width = width #-1
    face_height = height #-1
    face_central_width = face_width//2
    face_central_height = face_height//2
    face_central = face_central_width + face_central_height
    

    #画像の中心座標
    cap_width = (capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = (capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_central_width = cap_width//2
    cap_central_height = cap_height//2
    cap_central = cap_central_width + cap_central_height


    #リサイズ画像の中心座標
    resize_width = 255
    resize_height = 143
    resize_width //= 2 #127
    resize_height //= 2 #71
    resize_central = resize_width + resize_height


    if resize_central < face_central:
        socket.sendto("left 1".encode("UTF-8"), address)

    if resize_central > face_central:
        socket.sendto("right 1".encode("UTF-8"), address)

    
        

    #時間の下に図形を描画
    cv2.rectangle(gray_frame,
        pt1=(0, 0),
        pt2=(95, 50), #95,10
        color=(255, 255, 255),
        thickness=-1)

    cv2.rectangle(gray_frame,
        pt1=(127, 71), #こっちが中心座標
        pt2=(128, 72),
        color=(255, 255, 255),
        thickness=-1)

    
    #座標の表示
    cv2.putText(gray_frame,
        text=str(face),
        org=(0, 10),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.25,
        color=(0, 0, 0),
        thickness=1,
        lineType=cv2.LINE_AA)

    cv2.putText(gray_frame,
        text="Width:"+str(face_central_width),
        org=(0, 20),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.25,
        color=(0, 0, 0),
        thickness=1,
        lineType=cv2.LINE_AA)

    cv2.putText(gray_frame,
        text="Height:"+str(face_central_height),
        org=(0, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.25,
        color=(0, 0, 0),
        thickness=1,
        lineType=cv2.LINE_AA)

    #ウィンドウ表示
    cv2.imshow("Video",gray_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyWindow("Video")
        break

