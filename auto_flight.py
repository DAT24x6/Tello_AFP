import socket
import time
import sys
import subprocess
import tkinter as tk
from tkinter import ttk


#TelloはUDP通信
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('192.168.10.1' , 8889)


#自律飛行
def start():
    socket.sendto("command", encode("UTF-8"), address)

def takeoff():
    socket.sendto("takeoff", encode("UTF-8"), address)

def land():
    socket.sendto("land", encode("UTF-8"), address)

def flip_front():
    socket.sendto("flip f", encode("UTF-8"), address)

def auto_flight():
    socket.sendto("command", encode("UTF-8"), address)
    time.sleep(2)
    socket.sendto("takeoff", encode("UTF-8"), address)
    time.sleep(5)
    socket.sendto("flip f", encode("UTF-8"), address)
    time.sleep(2)
    socket.sendto("land", encode("UTF-8"), address)


#Tkinter
root =tk.Tk()
root.title("Auto flight")
root.geometry("256x144")

label = ttk.Label(root, text=u"--ボタンを押すとすぐに実行されます--")

standby  = ttk.Button(
    root,
    text="起動"
    command = start
)









