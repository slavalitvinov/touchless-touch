import win32con, win32api, win32gui, winxpgui, win32ui
import os
import struct
import Camera
import timer
import TouchFinder
import numpy
import pygame
import cv2
import sys
from PIL import Image
# from cv2 import Ipl2PIL
from io import StringIO

# click(10,10)
FPS = 25

from win32api import GetSystemMetrics

class Screen:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

class MainWindow:
    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)
        self.camera = Camera.Camera()
        self.finder = TouchFinder.TouchFinder()
        self.lock = 0
        self.fps_clock = pygame.time.Clock()
        self.surface_instance = None

    def CreateWindow(self, width, height):
        className = self.RegisterClass()
        self.BuildWindow(className, width, height)
        self.set_timer(100)

    def set_timer(self, delay):
        # 1 sec == 1000
        timer.set_timer(delay, self.handle_timer)

    def RegisterClass(self):
        className = "Test"
        message_map = {
#           win32con.WM_KEYDOWN: self.OnKeyDown,
           win32con.WM_DESTROY: self.OnDestroy,
        }
        wnd_proc = win32con.WNDPROCTYPE(handle_win_events)
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
#        wc.lpfnWndProc = 0
        wc.lpfnWndProc = wnd_proc
#        wc.lpfnWndProc = message_map
        wc.cbWndExtra = 0
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        wc.lpszClassName = className
        # C code: wc.cbWndExtra = DLGWINDOWEXTRA + sizeof(HBRUSH) + (sizeof(COLORREF));
        wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
        # wc.hIconSm = 0
        classAtom = win32gui.RegisterClass(wc)
        return className

    def BuildWindow(self, className, width=500, height=400):
        style = win32con.WS_OVERLAPPEDWINDOW
        xstyle = win32con.WS_EX_LEFT
        self.hwnd = win32gui.CreateWindow(className,
                             "ThisIsJustATest",
                             style,
                             win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                             width, height,
                             0, 0,
                             self.hinst,
                             None)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        winxpgui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(0,0,0), 70, win32con.LWA_ALPHA)

    def OnDestroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

    def OnKeyDown(self, hwnd, message, wparam, lparam):
        if wparam == 27:
            win32gui.PostQuitMessage(0)
            return True
        return False

    def handle_win_events(hwnd, message, wparam, lparam):
        pass

    def draw_point(self, x, y, color):
        pygame.draw.circle(self.surface(), color, (x, y), 10)
        return
#        hwnd=win32gui.WindowFromPoint((x,y))
        hdc = win32gui.GetWindowDC(self.hwnd)
        (x1, y1) = (x, y)
#        (x1,y1)=win32gui.ScreenToClient(self.hwnd,(x,y))
#        hdc.Clear()
        win32gui.SetPixel(hdc, x1, y1, color)
        r = 10
        win32gui.Ellipse(hdc, x1 - r, y1 - r, x1 + r, y1 + r)
        
        win32gui.ReleaseDC(self.hwnd, hdc)

    def surface(self):
        self.surface_instance = pygame.display.get_surface()
        if self.surface_instance is None:
            os.environ[ 'SDL_WINDOWID' ] = str(self.hwnd)
            pygame.init()
            window = pygame.display.set_mode()
            self.surface_instance = pygame.display.get_surface()
            self.surface_instance.set_alpha( 127 )
            mySurface = pygame.Surface((400,400), pygame.SRCALPHA, 32)
            mySurface.fill((0,0,0,0))
            # Draw to your surface
            self.surface_instance.blit(mySurface, (0,0))
            pygame.display.update()
        return self.surface_instance

    def draw_preview(self, x, y, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        surface = self.surface()
        img = pygame.image.fromstring(image.tostring(), (image.shape[1], image.shape[0]), 'RGB').convert().convert_alpha()
        x = 0
        y = 0
        w = img.get_width()
        h = img.get_height()
        img = pygame.transform.scale( img, (w//2, h//2) )
        x = surface.get_width() - img.get_width()
        y = surface.get_height() - img.get_height()
        surface.blit(img, (x, y))
        pygame.display.flip()

    def process_touch(self):
        self.image = self.camera.capture()
        self.draw_preview(0, 0, self.image)
        points = self.finder.find(self.image)
        for point in points:
            self.draw_point(int(point[0]), int(point[1]), 0xFFFFFF)
        pygame.display.update()

    def click(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def handle_timer(self, id, time_value):
        if self.lock:
            return
        self.lock = 1
        self.process_touch()
        self.lock = 0

    def terminate(self):
        print( 'terminate')
        self.quit = True

    def handle_events(self):
        for event in pygame.event.get():
            print( event.type )
            if event.type == pygame.QUIT: 
                self.terminate()
            elif event.type == pygame.KEYDOWN:
                self.terminate()
                if event.key == pygame.K_ESCAPE:  # event is escape key
                    self.terminate()
    
    def run(self):
        while not pygame.display.get_init():
            self.fps_clock.tick(FPS)
            win32gui.PumpWaitingMessages()
        self.quit = False
        while not self.quit:
            self.fps_clock.tick(FPS)
            pygame.event.pump()
            self.handle_events()

screen = Screen()
w = MainWindow()
w.CreateWindow(screen.width, screen.height)
w.run();
#pygame.quit()
