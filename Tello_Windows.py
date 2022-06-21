import sys
import subprocess
import tkinter as tk
from tkinter import ttk
import tello_state


def status():
    subprocess.Popen(["python", "tello_state.py"], shell=True)

def endapp():
    sys.exit()

root = tk.Tk()
root.title("Tello Terminal")
root.geometry("256x144")

label = ttk.Label(root, text = u"--Telloを接続してから実行すること！--")

button_01 = ttk.Button(
    root,
    text ="run",
    command = status
)

button_02 = ttk.Button(
    root,
    text ="exit",
    command = endapp
)

version = ttk.Label(root, text = "Ver 0.1.0")



label.pack()
button_01.pack()
button_02.pack()
version.pack(side=tk.RIGHT)

root.mainloop()