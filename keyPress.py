import time
from datetime import timedelta
from datetime import datetime

from pynput.keyboard import Key, Controller, Listener as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from pynput import keyboard as KeyBoard

import os
import ctypes

keyboard = KeyboardController()
mouse = MouseController()

#       #       #       #       #       #       #       #       #       #


#       #       #       #       #       #       #       #       #       #

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
   _fields_ = [("wVk", ctypes.c_ushort),
               ("wScan", ctypes.c_ushort),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
   _fields_ = [("uMsg", ctypes.c_ulong),
               ("wParamL", ctypes.c_short),
               ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
   _fields_ = [("dx", ctypes.c_long),
               ("dy", ctypes.c_long),
               ("mouseData", ctypes.c_ulong),
               ("dwFlags", ctypes.c_ulong),
               ("time", ctypes.c_ulong),
               ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
   _fields_ = [("ki", KeyBdInput),
               ("mi", MouseInput),
               ("hi", HardwareInput)]


class Input(ctypes.Structure):
   _fields_ = [("type", ctypes.c_ulong),
("ii", Input_I)]

def pressKey(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def releaseKey(key):
   extra = ctypes.c_ulong(0)
   ii_ = Input_I()

   flags = 0x0008 | 0x0002

   ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
   x = Input(ctypes.c_ulong(1), ii_)
   ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#       #       #       #       #       #       #       #       #       #

clickPosition = (2890, 720)

def Test():
   events = KeyBoard.Events()
   mouse.position = clickPosition

   hasEscape = False
      
   while hasEscape == False:
      mouse.click(Button.left, 1)
      time.sleep(0.025)
         
      for event in events:
         if event.key == KeyBoard.Key.esc:
            hasEscape = True
            break
         

def setClickPosition():
   clickPosition = mouse.position

def clickRepeat(inter=0.025):
   mouse.position = clickPosition

   while True:
      mouse.click(Button.left, 1)
      time.sleep(inter)


def getLoc():
    time.sleep(1)
    print(mouse.position)
   
#       #       #       #       #       #       #       #       #       #

def typeKey(key):
    pressKey(key)
    releaseKey(key)

def holdKey(key, dur):
    timeOut = time.time() + dur
    
    while time.time() < timeOut:
        typeKey(key)
        time.sleep(0.010)

#       #       #       #       #       #       #       #       #       #

clickRepeat()
