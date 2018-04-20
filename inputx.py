import threading
import shared
from ctypes import *
import win32api, win32con, win32gui, win32ui
import time
import pywinauto
import win32com.client
import wx

class Cli(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gdi= windll.LoadLibrary("c:\\windows\\system32\\gdi32.dll")
        self.hwnd_game = -1
        self.hwnd_cli = -1
        self.wDC = -1

    def click(self, x,y):
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def drag(self, x1,y1,x2,y2):
        win32api.SetCursorPos((x1,y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x2-x1,x2-x2,0,0)
        win32api.SetCursorPos((x2,y2))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)

    def getWindows(self, hwnd, lParam):
        if 'BlueStacks' in win32gui.GetWindowText(hwnd):
            self.hwnd_game = hwnd;
        if 'Windows PowerShell' in win32gui.GetWindowText(hwnd):
            self.hwnd_cli = hwnd;

    def test(self, x,y):
        pixel = self.gdi.GetPixel(self.wDC,x,y)

    def testcol(self, x,y):
        for i in range(0, 30):
            what = win32gui.ScreenToClient(self.hwnd_game, (x+i, y))
            pixel = self.gdi.GetPixel(self.wDC, what[0], what[1])
            r = pixel & 0x0000ff
            g = (pixel & 0x00ff00) >> 8
            b = (pixel & 0xff0000) >> 16

    def get_bmp():
        _ = wx.App()  # Need to create an App instance before doing anything
        screen = wx.ScreenDC()
        screen_size = screen.GetSize()
        scren_size_x = screen_size[1] / 2
        scren_size_y = screen_size[0] / 2

        mul = 2.6

        bmp = wx.Bitmap(scren_size_x * mul, scren_size_y * mul)
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, scren_size_x* mul, scren_size_y* mul, screen, 0, 0)
        del mem  # Release bitmap
        
        return bmp

    def test_pixel(self, args):    
        _ = wx.App()  # Need to create an App instance before doing anything
        x = (int)(args[0])
        y = (int)(args[1])

        x = (int)(x * 2.6)
        y = (int)(y * 2.6)
        
        screen = wx.ScreenDC()
        screen_size = screen.GetSize()
        scren_size_x = screen_size[1] / 2
        scren_size_y = screen_size[0] / 2

        bmp = self.get_bmp()
        apd = wx.AlphaPixelData(bmp, wx.Rect(0, 0, scren_size_x, scren_size_y))
        pixels = apd.GetPixels()

        pixels.MoveTo(apd, x, y)
        pixel = pixels.Get()

        print(f"pixel ({x},{y}): {pixel}")

        bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)

    def SetForegroundWindow(self, hwnd):
        return
        #win32gui.SetForegroundWindow(hwnd)

    def focus(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        pywinauto.win32functions.SetForegroundWindow(self.hwnd_cli)

    def init_game_window(self, args = None):
        self.send_gui('init_game_window')

    def init(self, args = None):
        win32gui.EnumWindows(self.getWindows, None)
        self.wDC = win32gui.GetWindowDC(self.hwnd_game)
        win32gui.SetForegroundWindow(self.hwnd_game)
        self.focus()

    def send_gui(self, command, *kargs):
        command = command + ' ' + ' '.join(str(e) for e in kargs)
        shared.messages.put(command)

    def startx(self, args = None):
        self.click(211, 370)

    def reset(self, args = None):
        self.click(372, 86)

    def back(self, args = None):
        self.click(33, 801)

    def move_piece(self, slot, x, y):
        self.drag(84, 633, x, y)

    def cmd_move_piece(self, args = None):      
        x = int(args[0])
        y = int(args[1])
        self.move_piece(1, x, y)

    def cmd_exit(self, args = None):
        self.send_gui('exit')

    def run_command(self, command):
        split = command.split()
        command = 'cmd_' + split[0]
        args = split[1:]
        method = getattr(self, command, lambda: "Invalid cli command")
        #if method:
        try:
            method(args)
        except Exception as e: 
            print("cli command threw an exception")
        self.focus()
        #else:
         #   print("command not found")

    def run(self):
        self.init()
        xinput = "";
        while xinput != "exit":
            xinput = input("> ");
            self.run_command(xinput)
                
        win32gui.ReleaseDC(self.hwnd_game, self.wDC)