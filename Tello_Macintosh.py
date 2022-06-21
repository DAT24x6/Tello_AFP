import sys
import subprocess
import tkinter as tk
from tkinter import ttk


def status():
    subprocess.Popen(["open", "tello_state.py"])

def endapp():
    sys.exit()

root = tk.Tk()
root.title("Tello Terminal for mac")
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

version = ttk.Label(root, text= "Ver 0.1.0")



label.pack()
button_01.pack()
button_02.pack()
version.pack(side=tk.RIGHT)

root.mainloop()