
import random
import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication
import cv2 as cv
import numpy as np
import os
import time
from PIL import Image as ImageGrab


script_dir = os.path.dirname(__file__)
img_dir = os.path.join(script_dir, '../imgs/')


class Utils:
    def __init__(self, hwnd, template_method, tag, filename, screen) -> None:
        super(Utils, self).__init__()
        self.hwnd = hwnd
        self.match_template_method = template_method
        self.debug = False
        self.tag = tag
        self.filename = filename
        self.screen = screen

    def background_screenshot(self, hwnd):
        """
        后台截图
        :param hwnd: 目标窗口句柄
        :return: 截图
        """
        img = self.screen.grabWindow(hwnd).toImage()
        img = img.convertToFormat(4)
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        img = np.array(ptr).reshape(img.height(), img.width(), 4)
        return img

    def force_screenshot(self, hwnd):
        """
        PIL截图方法，不能被遮挡
        :param hwnd: 目标窗口句柄
        :return: 截图
        """
        win32gui.SetForegroundWindow(hwnd)  # 窗口置顶
        time.sleep(0.2)  # 置顶后等0.2秒再截图
        x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)  # 获取窗口坐标
        grab_image = ImageGrab.grab((x1, y1, x2, y2))  # 用PIL方法截图
        im_cv2 = np.array(grab_image)  # 转换为cv2的矩阵格式
        return im_cv2

    def threshold_image(self, image):
        """
        灰度二值化
        :param image: 待处理图片
        :return: 二值化后的图片
        """
        bgr = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
        gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(
            src=gray, thresh=127, maxval=255, type=cv.THRESH_TRUNC)
        return binary

    def template_matching(self, sample_source, target_source, rate, num=1):
        """
        图像匹配
        :param sample_source: 样品
        :param target_source: 待检测图片
        :return: 二值化后的图片
        """
        sample = self.threshold_image(sample_source)
        target = self.threshold_image(target_source)

        method = self.match_template_method

        height, width = sample.shape[:2]
        res = cv.matchTemplate(image=target, templ=sample, method=method)
        if num == 1:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            print(
                f"method: {method}, min_val:{min_val}, max_val: {max_val}, min_loc:{min_loc}, max_loc: {max_loc}")
            left_top = None
            right_bottom = None
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                if min_val <= rate:
                    left_top = min_loc
                    right_bottom = (min_loc[0]+width, min_loc[1]+height)
            else:
                if max_val >= rate:
                    left_top = max_loc
                    right_bottom = (max_loc[0]+width, max_loc[1]+height)

            if self.debug is True:
                if left_top is not None and right_bottom is not None:
                    ract = cv.rectangle(target_source, left_top, right_bottom,
                                        (0, 0, 255), 2, cv.LINE_4)
                    cv.imwrite(img_dir+self.filename +
                               self.tag+'_match.jpg', ract)
                else:
                    print('匹配失败')

            if left_top is not None and right_bottom is not None:
                return (left_top, right_bottom)
        else:
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                loc = np.where(res <= rate)
            else:
                loc = np.where(res >= rate)
            return [(pt, (pt[0] + width, pt[1] + height)) for pt in zip(*loc[::-1])][0:num]

    def do_click(self, hwnd, start, movePath):
        """
        点击操作
        :param hwnd: 程序句柄
        :param start: 点击起始坐标(x,y)
        :param cy: 点击y坐标
        """
        cx, cy = start
        if self.debug is True:
            print(cx, cy, 'do_click')
        long_position = win32api.MAKELONG(cx, cy)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, long_position)
        if movePath is not None and isinstance(movePath, list):
            for moveTo in movePath:
                dx, dy = self._getPosition(moveTo, cx, cy)
                rx, ry = (cx, cy)
                offsetX = self._relate(rx, dx)
                offsetY = self._relate(ry, dy)
                randomTime = random.randint(500, 1500)
                duration = int((randomTime/1000)*25)
                current = 1
                if self.debug:
                    print(offsetX, offsetY)
                while current < duration:
                    x = (offsetX[0] * self._easeInOut(current,
                                                      1, offsetX[1], duration))
                    y = (offsetY[0] * self._easeInOut(current,
                                                      1, offsetY[1], duration))
                    position = win32api.MAKELONG(int(rx + x), int(ry + y))
                    if self.debug:
                        print(position, int(rx + x), int(ry + y))
                    win32api.SendMessage(
                        hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, position)
                    current += 1
                    time.sleep(0.04)
                long_position = win32api.MAKELONG(int(dx), int(dy))
                cx = int(dx)
                cy = int(dy)
        else:
            time.sleep(0.05)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON, long_position)

    def _getPosition(self, moveTo, rx, ry):
        if moveTo is not None and isinstance(moveTo, list):
            x, y = moveTo
            if isinstance(x, int) and isinstance(y, int):
                return (x, y)
            elif isinstance(x, str) and isinstance(y, str):
                return (rx + int(x), ry+int(y))
        return (rx, ry)

    def _relate(self, x1, x2):
        unit = 1
        if x1 > x2:
            unit = -1
        return (unit, unit * (x2-x1))

    def _easeInOut(self, currentTime, startValue, changeValue, duration):
        currentTime /= duration / 2
        if currentTime < 1:
            return changeValue / 2 * currentTime * currentTime + startValue
        currentTime -= 1
        return -changeValue / 2 * (currentTime * (currentTime - 2) - 1) + startValue
