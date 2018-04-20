from ctypes import *
import win32api, win32con, win32gui, win32ui
import time
import wx
#import pyscreenshot as ImageGrab
gdi= windll.LoadLibrary("c:\\windows\\system32\\gdi32.dll")

_hwnd = -1
_our_hwnd = -1
_wDC = -1

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def drag(x1,y1,x2,y2):
    win32api.SetCursorPos((x1,y1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x1,y1,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x2-x1,x2-x2,0,0)
    win32api.SetCursorPos((x2,y2))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x2,y2,0,0)

def getWindows(hwnd, lParam):
    global _hwnd, _our_hwnd
    if 'BlueStacks' in win32gui.GetWindowText(hwnd):
        _hwnd = hwnd;
    if 'Windows PowerShell' in win32gui.GetWindowText(hwnd):
        _our_hwnd = hwnd;

def move_piece(slot,x,y):
    if slot == 1:
        drag(84, 633, x, y)
def test(x,y):
    pixel = gdi.GetPixel(_wDC,x,y)
    print(pixel)

def testcol(x,y):
    for i in range(0, 30):
        what = win32gui.ScreenToClient(_hwnd, (x+i, y))
        print (x+i, y, what[0], what[1])
        pixel = gdi.GetPixel(_wDC, what[0], what[1])
        r = pixel & 0x0000ff
        g = (pixel & 0x00ff00) >> 8
        b = (pixel & 0xff0000) >> 16
        print(win32api.GetLastError())
        print(pixel, x+i,y,r, g, b)

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
    

    # frame = wx.Frame(None, title="Draw on Panel")
    # panel = wx.Panel(frame)

    # def on_paint(event):
    #     dc = wx.PaintDC(event.GetEventObject())
    #     dc.Clear()
    #     dc.SetPen(wx.Pen("RED", 4))
    #     dc.DrawLine(0, 0, 50, 50)

    # panel.Bind(wx.EVT_PAINT, on_paint)
    # frame.Show(True)

    _wDC = win32gui.GetWindowDC(0)
    while (True):
        win32gui.SetPixel(_wDC, 50, 50, 0)
        win32gui.SetPixel(_wDC, 52, 50, 0)
        win32gui.SetPixel(_wDC, 53, 50, 0)
        win32gui.SetPixel(_wDC, 54, 50, 0)
        win32gui.SetPixel(_wDC, 55, 50, 0)
        win32gui.SetPixel(_wDC, 56, 50, 0)
        win32gui.SetPixel(_wDC, 57, 50, 0)
        win32gui.SetPixel(_wDC, 58, 50, 0)
        win32gui.SetPixel(_wDC, 59, 50, 0)

    return bmp

def test_pixel(args):    
    _ = wx.App()  # Need to create an App instance before doing anything
    x = (int)(args[0])
    y = (int)(args[1])

    x = (int)(x * 2.6)
    y = (int)(y * 2.6)
    
    screen = wx.ScreenDC()
    screen_size = screen.GetSize()
    scren_size_x = screen_size[1] / 2
    scren_size_y = screen_size[0] / 2

    bmp = get_bmp()
    apd = wx.AlphaPixelData(bmp, wx.Rect(0, 0, scren_size_x, scren_size_y))
    pixels = apd.GetPixels()

    pixels.MoveTo(apd, x, y)
    pixel = pixels.Get()

    print(f"pixel ({x},{y}): {pixel}")

    bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)

def focus():
    win32gui.SetForegroundWindow(_our_hwnd)

def init(args = None):
    _ = wx.App()  # Need to create an App instance before doing anything
    win32gui.EnumWindows(getWindows, None)
    win32gui.MoveWindow(_hwnd, 0, 0, 760, 500, True)
    win32gui.SetForegroundWindow(_hwnd)
    _wDC = win32gui.GetWindowDC(_hwnd)
    focus()

def start(args = None):
    click(211, 370)

def reset(args = None):
    click(372, 86)

def back(args = None):
	click(33, 801)

def move_piece(args = None):
    move_piece(1, 200, 340)

commands = {
    'init': init,
    'start': start,
	'back': back,
    'test_pixel' : test_pixel,
    'reset': reset,
    'move_piece': move_piece
}

init()

xinput = "";
while xinput != "exit":
        xinput = input("> ");
        found = False
        for cmd in commands:
            if xinput.startswith(cmd + "" ""):
                found = True
                args = xinput.replace(cmd + " ", "")
                commands[cmd](args.split())
                focus()
        if not found:
            print("command not found")
        
win32gui.ReleaseDC(_hwnd, _wDC)