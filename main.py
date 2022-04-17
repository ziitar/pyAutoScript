

from modules.process import Process
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    p = Process(screen)
    p.start()
