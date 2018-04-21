from tkinter import *
import time
import win32gui
import win32api
import win32con
import threading
import cli
import shared
import queue
import pywinauto

class Gui():
    def __init__(self):
        self.WIDTH = 500
        self.HEIGHT = 500
        self.X = 0
        self.Y = 0
        self.LINEWIDTH = 2
        self.TRANSCOLOUR = 'blue'
        self.title = 'bot-gui'
        self.old = ()
        self.hwnd_tk = 0
        self.hwnd_game = 0
        self.hwnd_cli = 0
        self.running = 0

    def cmd_exit(self, args = None):
        self.running = 0;

    def cmd_cross_m(self, args = None):
        x = int(args[0])
        y = int(args[1])
        self.cross_m((x, y))

    def run_command(self, command):
        split = command.split()
        command = "cmd_" + split[0]
        args = split[1:]
        method = getattr(self, command, lambda: "Invalid gui command")
        method(args)

    def mouse_to_win32(self, pos):
        xpad = 3
        ypad = -68
        return (int(pos[0] * 2.5) + xpad, int(pos[1] * 2.5) + ypad)

    def cross(self, pos):
        size = 10
        lw = 4
        self.canvas.create_line(pos[0] - size, pos[1] - size, pos[0] + size, pos[1] + size, width=lw)
        self.canvas.create_line(pos[0] - size, pos[1] + size, pos[0] + size, pos[1] - size, width=lw)

    def cross_m(self, pos):
        self.cross(self.mouse_to_win32(pos))

    def run(self):
        win32gui.EnumWindows(self.enumHandler, None)

        rect = win32gui.GetWindowRect(self.hwnd_game)

        self.X = rect[0]
        self.Y = rect[1]
        self.WIDTH = rect[2] - self.X
        self.HEIGHT = rect[3] - self.Y
        self.tk = Tk()
        self.tk.title(self.title)
        self.tk.lift()
        self.tk.wm_attributes("-topmost", True)
        self.tk.wm_attributes("-transparentcolor", self.TRANSCOLOUR)
        self.tk.geometry('%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, self.X - 20, self.Y))

        self.canvas = Canvas(self.tk, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.canvas.config(cursor='tcross')
        self.canvas.create_rectangle(self.X, self.Y, self.WIDTH, self.HEIGHT, fill=self.TRANSCOLOUR, outline=self.TRANSCOLOUR)

        win32gui.EnumWindows(self.enumHandler, None)

        self.tk.bind('<Visibility>', self.putOnTop)
        self.tk.focus()

        self.running = 1

        while self.running == 1:
            try:
                self.tk.update()
                time.sleep(0.01)
                item = None
                try:
                    command = shared.messages.get(block=False)  
                    self.run_command(command)
                except queue.Empty:
                    item = None
                if (item):
                    shared.messages.task_done()
                #canvas.delete("all")
                self.create_rectangle(20, 20, 20 + shared.s, 20 + shared.s)
            except Exception as e:
                running = 0
                print("error %r" % (e))

        self.tk.destroy()
        self.tk.quit()
        self.running = 0


    def create_rectangle(self, x1,y1,x2,y2):
        self.canvas.create_rectangle(x1,y1,x2,y2)

    def putOnTop(self, event):
        event.widget.unbind('<Visibility>')
        event.widget.update()
        event.widget.lift()
        event.widget.bind('<Visibility>', self.putOnTop)

    def enumHandler(self,  hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if self.title in window_text:
                self.hwnd_tk = hwnd
            if 'BlueStacks' in window_text:
                self.hwnd_game = hwnd;
            if 'Windows PowerShell' in window_text:
                self.hwnd_cli = hwnd;

