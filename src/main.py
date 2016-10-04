import win32con, win32api, win32gui, winxpgui
import os
import struct

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

#click(10,10)

from win32api import GetSystemMetrics

class Screen:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

class MainWindow:
    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)

    def CreateWindow(self, width, height):
        className = self.RegisterClass()
        self.BuildWindow(className, width, height)

    def RegisterClass(self):
        className = "Test"
        message_map = {
           win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
        wc.cbWndExtra = 0
        wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        wc.lpszClassName = className
        # C code: wc.cbWndExtra = DLGWINDOWEXTRA + sizeof(HBRUSH) + (sizeof(COLORREF));
        wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
        #wc.hIconSm = 0
        classAtom = win32gui.RegisterClass(wc)
        return className

    def BuildWindow(self, className, width = 500, height = 400):
        style = win32con.WS_OVERLAPPEDWINDOW
        xstyle = win32con.WS_EX_LEFT
        self.hwnd = win32gui.CreateWindow(className,
                             "ThisIsJustATest",
                             style,
                             win32con.CW_USEDEFAULT,
                             win32con.CW_USEDEFAULT,
                             width,
                             height,
                             0,
                             0,
                             self.hinst,
                             None)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, 
            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        winxpgui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0,0,0), 175, win32con.LWA_ALPHA)

    def OnDestroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

    def draw_point(self,x,y,color):
#        hwnd=win32gui.WindowFromPoint((x,y))
        hdc=win32gui.GetDC(self.hwnd)
        (x1,y1)=(x,y)
#        (x1,y1)=win32gui.ScreenToClient(self.hwnd,(x,y))
        win32gui.SetPixel(hdc,x1,y1,color)
        r = 10
        win32gui.Ellipse(hdc,x1-r, y1-r, x1+r, y1+r)
        win32gui.ReleaseDC(self.hwnd,hdc)
   
screen = Screen()
w = MainWindow()
w.CreateWindow(screen.width, screen.height)
w.draw_point( 100, 100, 0xFF00FF)
win32gui.PumpMessages()

# LONG lStyle = GetWindowLong(hwnd, GWL_STYLE);
# lStyle &= ~(WS_CAPTION | WS_THICKFRAME | WS_MINIMIZE | WS_MAXIMIZE | WS_SYSMENU);
# SetWindowLong(hwnd, GWL_STYLE, lStyle);

# TODO:
#   1. draw cursor
#   2. 