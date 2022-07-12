import socket
import time
import sys
import cv2
import subprocess
import tkinter as tk
from tkinter import ttk


#UDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.10.1", 8889)


#映像受信
def camera():
    socket.sendto("streamon".encode("UTF-8"), address)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    capture = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1") #UDP受け取り用
    #capture = cv2.VideoCapture(0) パソコン内蔵カメラ

    while(True):
        ret, frame = capture.read()
        resize_frame = cv2.resize(frame, dsize=(640,480)) #1280x720

        #検出
        face = cascade.detectMultiScale(resize_frame)

        #四角をつける
        for rect in face:
            cv2.rectangle(resize_frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)

        #ウィンドウ表示
        cv2.imshow("Video",resize_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

#制御系
def emergency():
    socket.sendto("emergency".encode("UTF-8"), address)
    state.set ("----Status:[Emergency stop]----")

def endApp():
    sys.exit()

def start():
    socket.sendto("command".encode("UTF-8"), address)
    state.set ("----Status:[Standby(SDK Mode)]----")

def takeoff():
    socket.sendto("takeoff".encode("UTF-8"), address)
    state.set ("----Status:[Take off]----")

def land():
    socket.sendto("land".encode("UTF-8"), address)
    state.set ("----Status:[Landing]----")

def leftTurn():
    socket.sendto("ccw 360".encode("UTF-8"), address)
    state.set ("----Status:[Left turn]----")

def rightTurn():
    socket.sendto("cw 360".encode("UTF-8"), address)
    state.set ("----Status:[Right turn]----")
    
def flip_front():
    socket.sendto("flip f".encode("UTF-8"), address)
    state.set ("----Status:[Front flip]----")

def flip_back():
    socket.sendto("flip b".encode("UTF-8"), address)
    state.set ("----Status:[Back flip]----")

def all():
    state.set ("----Status:[All Running]----")
    time.sleep(2)
    socket.sendto("ccw 360".encode("UTF-8"), address)
    time.sleep(6)
    socket.sendto("cw 360".encode("UTF-8"), address)
    time.sleep(6)
    socket.sendto("flip f".encode("UTF-8"), address)
    time.sleep(3)
    socket.sendto("flip b".encode("UTF-8"), address)
    time.sleep(3)
    socket.sendto("land".encode("UTF-8"), address)
    


#Tkinter
root =tk.Tk()
root.title("Tello AFP")
#root.geometry("256x256")

state = tk.StringVar(value = "----Status:[Default Mode]----")

label = ttk.Label(root, text= u"---Telloを接続してから実行すること---")
status = ttk.Label(root, textvariable = state, relief = tk.RIDGE)

button_00 = ttk.Button(
    root,
    text ="緊急停止",
    command = emergency
)

button_01  = ttk.Button(
    root,
    text = "起動",
    command = start
)

button_02 = ttk.Button(
    root,
    text = "離陸",
    command = takeoff
)

button_03 = ttk.Button(
    root,
    text = "着陸",
    command = land
)

button_04 = ttk.Button(
    root,
    text = "左に360度旋回",
    command = leftTurn
)

button_05 = ttk.Button(
    root,
    text = "右に360度旋回",
    command = rightTurn
)

button_06 = ttk.Button(
    root,
    text = "前にフリップ",
    command = flip_front
)

button_07 = ttk.Button(
    root,
    text = "後ろにフリップ",
    command = flip_back
)

button_08 = ttk.Button(
    root,
    text = "全てを実行",
    command = all
)

button_09 = ttk.Button(
    root,
    text = "カメラ起動",
    command = camera
)

button_10 = ttk.Button(
    root,
    text = "終了",
    command = endApp
)

version = ttk.Label(root, text = "Ver 0.3.0")


label.pack()
status.pack()
button_00.pack()
button_01.pack()
button_02.pack()
button_03.pack()
button_04.pack()
button_05.pack()
button_06.pack()
button_07.pack()
button_08.pack()
button_09.pack()
button_10.pack()
version.pack(side=tk.RIGHT)

root.mainloop()