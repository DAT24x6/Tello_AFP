import sys
import subprocess
from tkinter import *
from tkinter import ttk


def status():
    subprocess.Popen(["open", "tello_state.py"])

def endapp():
    sys.exit()

root = tk.Tk()
root.title("Tello Terminal for mac")
root.geometry("256x144")

label = ttk.Label(root, text=u"--Telloを接続してから実行すること！--")

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

version = ttk.Label(root, text="Build:2022/06/14")



label.pack()
button_01.pack()
button_02.pack()
version.pack(side=RIGHT)

root.mainloop()