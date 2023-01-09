import socket
import time
import sys
import cv2
import numpy as np
import subprocess
import tkinter as tk
from tkinter import ttk



#UDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.10.1", 8889)


#subprocess起動
def camera():
    subprocess.Popen(["python3", "camera.py"])
            

#制御系
def emergency():
    socket.sendto("emergency".encode("UTF-8"), address)
    mainState.set("----Status :[Emergency stop]----")

def endApp():
    sys.exit()

def start():
    socket.sendto("command".encode("UTF-8"), address)
    mainState.set("----Status :[Standby(SDK Mode)]----")

def takeoff():
    socket.sendto("takeoff".encode("UTF-8"), address)
    mainState.set("----Status :[Take off]----")

def land():
    socket.sendto("land".encode("UTF-8"), address)
    mainState.set("----Status :[Landing]----")

def leftTurn():
    socket.sendto("ccw 360".encode("UTF-8"), address)
    mainState.set("----Status :[Left turn]----")

def rightTurn():
    socket.sendto("cw 360".encode("UTF-8"), address)
    mainState.set("----Status :[Right turn]----")
    
def flip_front():
    socket.sendto("flip f".encode("UTF-8"), address)
    mainState.set("----Status :[Front flip]----")

def flip_back():
    socket.sendto("flip b".encode("UTF-8"), address)
    mainState.set("----Status :[Back flip]----")


def setSpeed():

    def speed_10():
        socket.sendto("speed 10".encode("UTF-8"), address)
        speedState.set("--Current set speed :[10/s]--")

    def speed_20():
        socket.sendto("speed 20".encode("UTF-8"), address)
        speedState.set("--Current set speed :[20/s]--")

    def speed_30():
        socket.sendto("speed 30".encode("UTF-8"), address)
        speedState.set("--Current set speed :[30/s]--")

    def speed_40():
        socket.sendto("speed 40".encode("UTF-8"), address)
        speedState.set("--Current set speed :[40/s]--")

    def destroyWindow():
        speed.destroy()


    #Tkinter(speed)
    speed = tk.Toplevel()
    speed.title("Select Speed")

    speedState = tk.StringVar(value = "--Current set speed :[10/s]--")
    speedStatus = ttk.Label(speed, textvariable = speedState, relief = tk.RIDGE)

    button_speed_10 = ttk.Button(
        speed,
        text = "10cm/sに設定",
        command = speed_10
    )

    button_speed_20 = ttk.Button(
        speed,
        text = "20cm/sに設定",
        command = speed_20
    )

    button_speed_30 = ttk.Button(
        speed,
        text = "30cm/sに設定",
        command = speed_30
    )

    button_speed_40 = ttk.Button(
        speed,
        text = "40cm/sに設定",
        command = speed_40
    )

    button_destroy = ttk.Button(
        speed,
        text = "閉じる",
        command = destroyWindow
    )

    speedStatus.pack()
    button_speed_10.pack()
    button_speed_20.pack()
    button_speed_30.pack()
    button_speed_40.pack()
    button_destroy.pack()


#Tkinter(main)
main = tk.Tk()
main.title("Tello AFP")
#main.geometry("256x256")

mainState = tk.StringVar(value = "----Status :[Default Mode]----")

label = ttk.Label(main, text= u"---Telloを接続してから実行すること---")
mainStatus = ttk.Label(main, textvariable = mainState, relief = tk.RIDGE)

button_emergency = ttk.Button(
    main,
    text ="緊急停止",
    command = emergency
)

button_start  = ttk.Button(
    main,
    text = "起動",
    command = start
)

button_takeoff = ttk.Button(
    main,
    text = "離陸",
    command = takeoff
)

button_land = ttk.Button(
    main,
    text = "着陸",
    command = land
)

button_camera = ttk.Button(
    main,
    text = "カメラ起動",
    command = camera
)

button_setSpeed = ttk.Button(
    main,
    text = "飛行速度の設定",
    command = setSpeed
)

button_endApp = ttk.Button(
    main,
    text = "終了",
    command = endApp
)


version = ttk.Label(main, text = "Ver 1.0.0")


label.pack()
mainStatus.pack()
button_emergency.pack()
button_start.pack()
button_takeoff.pack()
button_land.pack()
button_camera.pack()
button_setSpeed.pack()
button_endApp.pack()
version.pack(side=tk.RIGHT)

main.mainloop()