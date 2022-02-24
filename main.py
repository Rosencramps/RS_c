import os
import time
import random
import cv2 as cv
import numpy as np
from windowcapture import WindowCapture
import pyautogui
from pynput.mouse import Controller  # https://pypi.org/project/pynput/
import pynput.keyboard as kb


# https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI&index=2
def main():
    window = WindowCapture('RuneLite - Rosencramps')
    time.sleep(5)
    mouse = Controller()
    mouse.scroll(0, random.randint(30, 37) * -1)
    time.sleep(.5)
    # mouse.scroll(0, -30)

    dump_inventory(window)
    run_bot(window)


def run_bot(window):
    # changing inventory_size from 28(actual) to random for fishing
    inventory_size = random.randint(2, 4)
    while True:
        for i in range(inventory_size):
            screenshot = window.get_screenshot()
            needle_box = find_needle(screenshot)

            if needle_box == 0:  # tries again to find a needle
                # pyautogui.moveTo((120, 120), duration=1) # move cursor out of the way of a potential needle
                time.sleep(7)
                needle_box = find_needle(screenshot)
                if needle_box == 0:
                    print("==== Confidence Too Low! ====")
                    run_bot(window)

            click_point_x = needle_box[0][0] + int((needle_box[1][0] - needle_box[0][0]) / 2)
            click_point_y = needle_box[0][1] + int((needle_box[1][1] - needle_box[0][1]) / 2)
            center_point = click_point_x, click_point_y  # x,y of needle center on window
            click_point = window.get_screen_position(center_point)  # x,y on entire screen

            # visuals
            # cv.rectangle(screenshot, needle_box[0], needle_box[1], color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
            # cv.drawMarker(screenshot, center_point, (0, 0, 255), cv.MARKER_CROSS)
            # cv.imwrite('result.jpg', screenshot)
            # cv.imshow('bot vision', screenshot)

            click_needle(click_point)
            if random.randint(0, 35) == 0:  # afk once every 37 times
                time.sleep(random.randint(37, 100))
            time.sleep(random.uniform(25.5, 39.3))

        dump_inventory(window)


def dump_inventory(window):
    screenshot = window.get_screenshot()

    # for needle in os.listdir(path='inv_needles'):
        # path = str('inv_needles/' + needle)
    needle_img = cv.imread('inv_needles/N1.png', cv.IMREAD_UNCHANGED)
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    result = cv.matchTemplate(screenshot, needle_img, cv.TM_CCOEFF_NORMED)
    keyboard = kb.Controller()

    locations = np.where(result >= .68)
    locations = list(zip(*locations[::-1]))

    # list of [x, y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)

    rectangles, weight = cv.groupRectangles(rectangles, 1, 0.5)

    click_points = []
    if len(rectangles):
        for (x, y, w, h) in rectangles:
            center_x = x + int(w / 2) + random.randint(-10, 10)
            center_y = y + int(h / 2) + random.randint(-10, 10)
            img_center = center_x, center_y
            point = window.get_screen_position(img_center)
            click_points.append(point)

    random.shuffle(click_points)
    with keyboard.pressed(kb.Key.shift):
        for point in click_points:
            pyautogui.moveTo(point, duration=random.uniform(0.1, 0.3))
            pyautogui.click()
            time.sleep(random.uniform(0.02, 0.1))


def find_needle(haystack_img):
    location = None
    confidence = 0
    needle_w = 0
    needle_h = 0
    for needle in os.listdir(path='needles'):
        path = str('needles/' + needle)
        needle_img = cv.imread(path, cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > confidence:
            confidence = max_val
            location = max_loc
            needle_w = needle_img.shape[1]
            needle_h = needle_img.shape[0]

    top_left = location
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    print(confidence)
    ret_val = (top_left, bottom_right) if confidence > 0.65 else 0
    return ret_val


def click_needle(click_point):
    fishing_title_negation = 25    # To move center point of fishing location under the fish name banner
    cp = (click_point[0] + random.randint(-10, 10), click_point[1] + random.randint(-10, 10) + fishing_title_negation)
    click_point = cp

    mouse = Controller()
    movement_speed = random.uniform(.3, 1.1)
    x = mouse.position[0]
    y = mouse.position[1]
    mid_x = int(abs(x - click_point[0]) / 2)
    mid_x += x if x < click_point[0] else click_point[0]
    mid_y = int(abs(y - click_point[1]) / 2)
    mid_y += y if y < click_point[1] else click_point[1]

    # creating possible random midpoint to visit half the time
    if random.randint(0, 1) == 0:
        lr = random.randint(0, 1)
        if lr:
            mid_x += random.randint(0, 35)
            mid_y += random.randint(0, 35)
        else:
            mid_x -= random.randint(0, 35)
            mid_y -= random.randint(0, 35)
        midpoint = (mid_x, mid_y)
        pyautogui.moveTo(midpoint, duration=movement_speed)

    # random miss
    if random.randint(0, 7) == 0:
        print("miss")
        mx = random.randint(35, 45)
        if random.randint(0, 1) == 0:
            mx *= -1
        my = random.randint(35, 45)
        if random.randint(0, 1) == 0:
            my *= -1
        miss = click_point[0] + mx, click_point[1] + my
        pyautogui.moveTo(miss, duration=movement_speed)
        pyautogui.click()
        pyautogui.moveTo(click_point, duration=random.uniform(.13, .19))
        pyautogui.click()
    else:
        print("no miss")
        pyautogui.moveTo(click_point, duration=movement_speed)
        pyautogui.click()
        time.sleep(random.uniform(.1, .3))

    # move away 7 out of 8 times
    if random.randint(0, 7) != 0:
        move_away = (click_point[0] + random.randint(-240, 240), click_point[1] + random.randint(-240, 240))
        pyautogui.moveTo(move_away, duration=movement_speed)


main()
