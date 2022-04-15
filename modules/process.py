
from typing_extensions import Self
from modules.config import Config
from modules.uitils import Utils
import time
import win32gui


class Process(Utils):
    def __init__(self) -> None:
        super(Process, self).__init__()
        self.config = Config('../config/config.json')
        self.hwnd = 0
        self.program_title = ''
        self.get_active_window(self)

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
        item = self.config.getFirstItem()

        while item.next is not None:
            item = self.config.getItem(item.next)
