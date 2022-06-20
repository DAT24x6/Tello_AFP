import socket
import time
import sys
import subprocess
import tkinter as tk
from tkinter import ttk


#UDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('192.168.10.1' , 8889)


#自動飛行
def start():
    socket.sendto("command".encode("UTF-8"), address)

def takeoff():
    socket.sendto("takeoff".encode("UTF-8"), address)

def land():
    socket.sendto("land".encode("UTF-8"), address)

def flip_front():
    socket.sendto("flip f".encode("UTF-8"), address)

def auto_flight():
    socket.sendto("command".encode("UTF-8"), address)
    time.sleep(2)
    socket.sendto("takeoff".encode("UTF-8"), address)
    time.sleep(5)
    socket.sendto("flip f".encode("UTF-8"), address)
    time.sleep(2)
    socket.sendto("land".encode("UTF-8"), address)


#Tkinter
root =tk.Tk()
root.title("Tello AFP")
#root.geometry("256x256")

state = "Stand by"

label = ttk.Label(root, text= u"--ボタンを押すとすぐに実行されます--")
status = ttk.Label(root, text = f"Status:[{state}]")

button_01  = ttk.Button(
    root,
    text = "起動",
    command = start,
    state = "Ready"
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
    text = "前フリップ",
    command = flip_front
)

version = ttk.Label(root, text = "Ver 0.0.2")


label.pack()
status.pack()
button_01.pack()
button_02.pack()
button_03.pack()
button_04.pack()
version.pack()

root.mainloop()








