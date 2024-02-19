import win32gui, win32con
import os
import math
import time


def minimizeOpenWindow():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
    pass