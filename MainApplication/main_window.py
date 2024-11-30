import os
import sys
from PyQt6.QtCore import Qt, QDir, QThread, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QListWidget, QMainWindow, QDockWidget, QSpacerItem, QSizePolicy, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox
from MainApplication.main_layout import MainLayout
from Settings import JSON_file_methods as jsn
from Settings.Sidebar import SideBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_downloading = None
        self.side_bar = None
        self.main_layout = None
        self.media_format = ""
        self.status_menu = QListWidget()
        self.video_title = ""
        self.define_main_window()

    def define_main_window(self):
        """Defines the main window which will be displayed to the user"""
        self.setWindowTitle("Youtube Downloader")
        self.setGeometry(100, 100, 400, 300)

        if hasattr(sys, "_MEIPASS"):  # Check if running as a packaged app
            icon_path = os.path.join(sys._MEIPASS, "assets", "download_icon.png")
        else:
            icon_path = os.path.join("assets", "download_icon.png")

        self.setWindowIcon(QIcon(icon_path))
        try:
            self.main_layout = MainLayout()
            self.side_bar = SideBar()

            central_widget = self.main_layout
            self.setCentralWidget(central_widget)

            #Add settings Dock to container sidebar
            dock_widget = QDockWidget(self)
            dock_widget.setTitleBarWidget(QWidget())  # Remove the title bar
            dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)  # Disable features
            dock_widget.setFixedWidth(35)
            dock_widget.setWidget(self.side_bar)

            # Add settings sidebar to the window
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)

            #Add dock to the right side to offset space at the left

            right_side_spacer = QDockWidget()
            right_side_spacer.setTitleBarWidget(QWidget())
            right_side_spacer.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
            right_side_spacer.setFixedWidth(35)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_side_spacer)

        except Exception as main_window_ex:
            print("error in main_window",main_window_ex)

    def showEvent(self, event):
        """Creates the download folder for the videos/audios when the window is loaded"""
        super().showEvent(event)
        if not event.spontaneous():
            download_path = self.create_download_folder_on_startup()
            if download_path is not None:
                jsn.update_json_file_path(download_path)
                print("Json updated properly, path is", download_path)

    def create_download_folder_on_startup(self):
        """Creates the download folder on startup if it already doesn't exist"""
        try:
            desktop_path = os.path.join(QDir.homePath(), "Desktop")
            download_folder_name = "VidDownloader"
            folder_path = os.path.join(desktop_path, download_folder_name)
            default_download_folder_path = os.path.abspath(folder_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print("Made a new folder")
                return default_download_folder_path
            else:
                print('Folder already exists no need')
                return None
        except Exception as e:
            print("Exception is", e)

    def closeEvent(self, event):
        # Check if any threads are running in main_layout
        if self.main_layout.is_thread_running():
            reply = QMessageBox.question(
                self,
                "Error",
                "You cannot close the window whilst a download/ downloads are in progress",
                QMessageBox.StandardButton.Ok
            )
            event.ignore()
        else:
            event.accept()
