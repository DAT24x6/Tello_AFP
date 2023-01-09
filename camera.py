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

#Status用UDP受信

#学習データ読み込み
cascade = cv2.CascadeClassifier("cascade/haarcascade_frontalface_alt.xml")
#cascade = cv2.CascadeClassifier("cascade/haarcascade_fullbody.xml")
#cascade = cv2.CascadeClassifier("cascade/haarcascade_upperbody.xml")

capture = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1") #UDP受け取り用
#capture = cv2.VideoCapture(0) #パソコン内蔵カメラ

#録画の設定
cap_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) #横幅
cap_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) #縦幅
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) #総フレーム
fps = int(capture.get(cv2.CAP_PROP_FPS)) #フレームレート
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') #保存形式
rec_config = cv2.VideoWriter('rec.mp4', fourcc, fps, (cap_width, cap_height))

#映像が取得出来たらTrue.
Rece_Video = capture.isOpened()

#受信チェック
if Rece_Video == False:
    print("Failed to receve video.")
    exit()

while(Rece_Video):
    let, frame = capture.read()
    resize_frame = cv2.resize(frame, dsize=(256,144)) #1280x720 #640x480

    #グレースケール変換
    gray_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)

    #検出
    face = cascade.detectMultiScale(gray_frame)
    print(len(face))

    #mp4ファイル出力
    rec_config.write(frame)


    #認識座標のアンパック
    if len(face) == 0:
        pass
    elif len(face[0]) == 4:
        x, y, width, height = face[0]

        #顔認識の中心座標
        face_x = x
        face_y = y

        face_width = width #-1
        face_height = height #-1

        face_half_width = face_width//2
        face_half_height = face_height//2
        
        face_central_x = x + face_half_width
        face_central_y = y + face_half_height

        face_position = face_half_width + face_half_height
        face_central = face_central_x + face_central_y

        print("face_width :"+str(face_width))
        print("face_height :"+str(face_height))
        print("face_position(認識の縦横サイズ) :"+str(face_position))
        print("face_central(顔の中心) :"+str(face_central))
        
        #顔の中心に点を表示, 四角をつける
        cv2.rectangle(gray_frame, (x, y), (x + width, y + height), (255, 255, 255), thickness=1)
        cv2.circle(gray_frame, (face_central_x, face_central_y), 1, (255, 255, 255), thickness=-1)

        #リサイズ画像の中心座標
        resize_width = 255
        resize_height = 143
        resize_width //= 2 #127
        resize_height //= 2 #71
        resize_central = resize_width + resize_height #198


        if face_position < 40:
            socket.sendto("forward 20".encode("UTF-8"), address)
            print("send to forward!")

        if face_position > 60:
            socket.sendto("back 20".encode("UTF-8"), address)
            print("send to back!")

        if face_central < 140:
            socket.sendto("left 20".encode("UTF-8"), address)
            print("send to Left!")

        if face_central > 200:
            socket.sendto("right 20".encode("UTF-8"), address)
            print("send to Right!")
        
        

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
        text="Face:"+str(face),
        org=(0, 10),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.25,
        color=(0, 0, 0),
        thickness=1,
        lineType=cv2.LINE_AA)

    #ウィンドウ表示
    cv2.imshow("DEBUG",gray_frame)
    #cv2.imshow("Video",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.destroyWindow("Video")
        cv2.destroyWindow("DEBUG")
        break

