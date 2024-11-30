import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from MainApplication.main_window import MainWindow

"""Runs the GUI"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon_path = os.path.join("assets", "taskbar_image.png")
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
