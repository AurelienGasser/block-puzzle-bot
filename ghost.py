from tkinter import *
import time
import win32gui
import win32api
import threading
import inputx
import shared

WIDTH = 500
HEIGHT = 500
LINEWIDTH = 1
TRANSCOLOUR = 'blue'
title = 'Virtual whiteboardot'
global old
old = ()
global HWND_t
HWND_t = 0

tk = Tk()
tk.title(title)
tk.lift()
tk.wm_attributes("-topmost", True)
tk.wm_attributes("-transparentcolor", TRANSCOLOUR)

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128

canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
canvas.pack()
canvas.config(cursor='tcross')
canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=TRANSCOLOUR, outline=TRANSCOLOUR)

def putOnTop(event):
    event.widget.unbind('<Visibility>')
    event.widget.update()
    event.widget.lift()
    event.widget.bind('<Visibility>', putOnTop)

def enumHandler(hwnd, lParam):
    global HWND_t
    if win32gui.IsWindowVisible(hwnd):
        if title in win32gui.GetWindowText(hwnd):
            HWND_t = hwnd

win32gui.EnumWindows(enumHandler, None)

tk.bind('<Visibility>', putOnTop)
tk.focus()

shared.init()

a = inputx.InputThread("Bot")
a.start()
#a.join()

els = []

def create_rectangle(x1,y1,x2,y2):
    rect = canvas.create_rectangle(x1,y1,x2,y2)
    #els.append(rect)

if HWND_t != 0:
    canvas.create_line(10, 10, 20, 20, width=LINEWIDTH)

running = 1

while running == 1:
    try:
        tk.update()
        time.sleep(0.01)
        #canvas.delete("all")
        create_rectangle(20, 20, 20 + shared.s, 20 + shared.s)
    except Exception as e:
        running = 0
        print("error %r" % (e))
