# You can basically do whatever you want after it captures your face 5 times
import pyautogui as mouse

mouse.FAILSAFE = False

def terminal_open():
    mouse.moveTo(0, 0)
    mouse.leftClick()
    mouse.moveTo(46, 498)
    mouse.leftClick()
