import os
import Settings.JSON_file_methods as jsn
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QMessageBox
from Settings.SettingsWindow import SettingsWindow


class SideBar(QWidget):
    """Class that contains the sidebar to be added to the QDocketWidget in the main Application window"""
    def __init__(self):
        super().__init__()
        self.side_menu_layout = QVBoxLayout()
        self.side_menu_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        # Set spacing between buttons to 0
        self.side_menu_layout.setSpacing(0)

        self.settings_button = QPushButton()
        self.settings_button.clicked.connect(self.settings_button_clicked)
        self.settings_button.setIcon(QIcon("Settings/images/settings_icon.png"))
        self.settings_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.settings_button.setStyleSheet("background-color: transparent;border: none; padding: 0px;")
        self.settings_button.setIconSize(QSize(32, 19))  # Set the size of the icon
        self.settings_button.setFixedSize(35, 20)


        self.file_explorer_button = QPushButton()
        file_expl_tool_tip_text = "Opens folder which contains downloads"
        self.file_explorer_button.setToolTip(file_expl_tool_tip_text)
        self.file_explorer_button.clicked.connect(self.file_explorer_button_clicked)
        self.file_explorer_button.setIcon(QIcon("Settings/images/file_explorer_icon.png"))
        self.file_explorer_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.file_explorer_button.setStyleSheet(
            "background-color: transparent; border: none; padding: 0px;"
        )
        self.file_explorer_button.setIconSize(QSize(32, 19))  # Set the size of the icon
        self.file_explorer_button.setFixedSize(35, 20)

        self.side_menu_layout.addWidget(self.file_explorer_button)
        self.side_menu_layout.addWidget(self.settings_button)
        self.setLayout(self.side_menu_layout)

    def settings_button_clicked(self):
        """Opens the settings window"""
        settings_window = SettingsWindow()
        settings_window.exec()

    def file_explorer_button_clicked(self):
        """Opens the file location where the videos/audios are being downloaded"""
        file_path = jsn.read_json_file_path()
        os.startfile(file_path)
