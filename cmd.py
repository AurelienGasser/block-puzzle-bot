import win32gui
from re import match
def draw_line():
    print('x1,y1,x2,y2?')
    s=input()
    if match('\d+,\d+,\d+,\d+',s):
        while True:
            x1,y1,x2,y2=s.split(',')
            x1=int(x1)
            y1=int(y1)
            x2=int(x2)
            y2=int(y2)
            print(x1, y1, x2, y2)
            hwnd=win32gui.WindowFromPoint((x1,y1))
            hdc=win32gui.GetDC(0)
            x1c=x1
            y1c=y1
            #win32gui.ScreenToClient(hwnd,(x1,y1))
            x2c=x2
            y2c=y2
            #win32gui.ScreenToClient(hwnd,(x2,y2))
            win32gui.MoveToEx(hdc,x1c,y1c)
            win32gui.LineTo(hdc,x2c,y2c)
            win32gui.ReleaseDC(hwnd,hdc)
    main()
def draw_cross():
    print('x1,y1,x2,y2?')
    s=input()
    if match('\d+,\d+',s):
        x1,y1=s.split(',')
        x1=int(x1)
        y1=int(y1)
        print(x1, y1)
        hdc=win32gui.GetDC(0)
        length = 20
        win32gui.MoveToEx(hdc, x1 - length, y1 - length)
        win32gui.LineTo(hdc, x1 + length, y1 + length)
        win32gui.MoveToEx(hdc, x1 + length, y1 - length)
        win32gui.LineTo(hdc, x1 - length, y1 + length)
    main()
def draw_point():
    print('x,y,color?')
    s=input()
    if match('\d+,\d+,\d+',s):
        x,y,color=s.split(',')
        x=int(x)
        y=int(y)
        color=int(color)
        hwnd=win32gui.WindowFromPoint((x,y))
        hdc=win32gui.GetDC(hwnd)
        x1,y1=win32gui.ScreenToClient(hwnd,(x,y))
        win32gui.SetPixel(hdc,x1,y1,color)
        win32gui.ReleaseDC(hwnd,hdc)
    main()
def get_pixel_col():
    print('x,y?')
    s=input()
    if match('\d+,\d+',s):
        x,y=s.split(',')
        x=int(x)
        y=int(y)
        hwnd=win32gui.WindowFromPoint((x,y))
        hdc=win32gui.GetDC(hwnd)
        x1,y1=win32gui.ScreenToClient(hwnd,(x,y))
        color=win32gui.GetPixel(hdc,x1,y1)
        win32gui.ReleaseDC(hwnd,hdc)
        print(color)
    main()
def get_current_pos_info():
    x,y=win32gui.GetCursorPos()
    hwnd=win32gui.WindowFromPoint((x,y))
    hdc=win32gui.GetDC(hwnd)
    x1,y1=win32gui.ScreenToClient(hwnd,(x,y))
    print(x,y,win32gui.GetPixel(hdc,x1,y1))
    win32gui.ReleaseDC(hwnd,hdc)
    main()
def main():
    print('l. draw line')
#p.draw point
#g.get pixel color
#c.get current mouse position's info''')
    s=input()
    if s.lower()=='l':
        draw_line()
    if s.lower()=='p':
        draw_point()
    if s.lower()=='g':
        get_pixel_col()
    if s.lower()=='c':
        draw_cross()
main()