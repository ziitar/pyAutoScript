
import random
from modules.config import Config, Item
import time
import win32gui
import os
import re

script_dir = os.path.dirname(__file__)
config_dir = os.path.join(os.path.abspath(
    os.path.dirname(script_dir+os.path.sep+'.')), '../config/')


class Process():
    def __init__(self, screen) -> None:
        super(Process, self).__init__()
        files = os.listdir(config_dir)
        i = 0
        files = list(filter(lambda url: re.search(
            '.+\.json$', url) is not None, files))
        for file in files:
            i += 1
            print('{0:2d} {1:10s}'.format(i, file))
        index = input('请输入需执行的配置文件序号:')
        file = files[int(index) - 1]
        self.config = Config(file)
        self.file = file
        self.hwnd = 0
        self.program_title = ''
        self.get_active_window()
        self.globalData = {}
        self.screen = screen

    def get_active_window(self, loop_times=5):
        """
        点击鼠标获取目标窗口句柄
        :param loop_times: 倒计时/循环次数
        """
        for t in range(loop_times):
            print(f'请在倒计时 [ {loop_times} ] 秒结束前，点击目标窗口')
            loop_times -= 1
            self.hwnd = win32gui.GetForegroundWindow()
            self.program_title = win32gui.GetWindowText(self.hwnd)
            print(f"目标窗口： [ {self.program_title} ] [ {self.hwnd} ] ")
            time.sleep(1)  # 每1s输出一次
        print("-----------------------------------------------------------")
        print(
            f"目标窗口: [ {self.program_title} ]")
        print("-----------------------------------------------------------")

    def start(self):
        print(f'匹配到窗口：{self.program_title},开始执行脚本')
        itemConfig = self.config.getFirstItem()
        item = Item(self.hwnd, itemConfig, self.globalData,
                    'start', self.file, self.screen)
        item.run()
        if "sleep" in itemConfig is not None and isinstance(itemConfig["sleep"], int):
            time.sleep(itemConfig["sleep"])
        if 'sleepRandom' in itemConfig and isinstance(itemConfig['sleepRandom'], float):
            time.sleep(random.random(0, itemConfig['sleepRandom']))
        if item.next is not None:
            while item.next is not None:
                tag = item.next
                itemConfig = self.config.getItem(item.next)
                if itemConfig is not None:
                    item = Item(self.hwnd, itemConfig,
                                self.globalData, tag, self.file, self.screen)
                    item.run()
                    if "sleep" in itemConfig is not None and isinstance(itemConfig["sleep"], int):
                        time.sleep(itemConfig["sleep"])
                else:
                    item.next = None
        print('脚本执行完成')
