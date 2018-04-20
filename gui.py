from tkinter import *
import time
import win32gui
import win32api
import win32con
import threading
import inputx
import shared
import queue
import pywinauto

class Gui():
    def __init__(self):
        self.WIDTH = 500
        self.HEIGHT = 500
        self.LINEWIDTH = 1
        self.TRANSCOLOUR = 'blue'
        self.title = 'Virtual whiteboardot'
        self.old = ()
        self.hwnd_tk = 0
        self.hwnd_game = 0
        self.hwnd_cli = 0
        self.running = 0

    def cmd_exit(self, args = None):
        self.running = 0;

    def run_command(self, command):
        split = command.split()
        command = "cmd_" + split[0]
        args = split[1:]
        method = getattr(self, command, lambda: "Invalid gui command")
        method(args)

    def run(self):
        self.tk = Tk()
        self.tk.title(self.title)
        self.tk.lift()
        self.tk.wm_attributes("-topmost", True)
        self.tk.wm_attributes("-transparentcolor", self.TRANSCOLOUR)

        self.canvas = Canvas(self.tk, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.canvas.config(cursor='tcross')
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill=self.TRANSCOLOUR, outline=self.TRANSCOLOUR)

        win32gui.EnumWindows(self.enumHandler, None)

        self.tk.bind('<Visibility>', self.putOnTop)
        self.tk.focus()

        if self.hwnd_tk != 0:
            self.canvas.create_line(10, 10, 20, 20, width=self.LINEWIDTH)

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

