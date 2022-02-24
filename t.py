import time
import random

from windowcapture import WindowCapture
import pyautogui
from pynput.mouse import Button, Controller
from matplotlib import pyplot as plt


# https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI&index=2
def main():
    while True:
        time.sleep(1)
        print(pyautogui.position())

    # (680, 628)
    # (796, 804)
    # 58
    # 88

main()
