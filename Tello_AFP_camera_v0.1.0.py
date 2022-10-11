import socket
import time
import sys
import cv2
import subprocess
import tkinter as tk
from tkinter import ttk
import datetime

#UDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.10.1", 8889)

#映像受信
socket.sendto("streamon".encode("UTF-8"), address)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
#capture = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1") #UDP受け取り用
capture = cv2.VideoCapture(0) #パソコン内蔵カメラ

while(True):
    let, frame = capture.read()
    resize_frame = cv2.resize(frame, dsize=(256,144)) #1280x720 #640x480

    #グレースケール変換
    gray_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)

    #検出
    face = cascade.detectMultiScale(gray_frame)

    #四角をつける
    for rect in face:
        cv2.rectangle(gray_frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=1)

    #時間取得
    nowtime = datetime.datetime.now()
    strnowtime = nowtime.strftime("%Y-%m-%d %H:%M:%S")

    #時間の下に図形を描画
    cv2.rectangle(gray_frame,
        pt1=(0, 0),
        pt2=(95, 10),
        color=(255, 255, 255),
        thickness=-1)

    #ウィンドウに文字を描画
    cv2.putText(gray_frame,
        text=strnowtime,
        org=(0, 10),
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