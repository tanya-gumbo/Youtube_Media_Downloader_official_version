from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QButtonGroup, QPushButton, \
    QListWidgetItem, QProgressBar, QListWidget, QMessageBox
from MainApplication.download_functionality import VideoDownloader, DownloadTask


class MainLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.download_status = None
        self.youtube_link_entry = QLineEdit()
        self.link_label = QLabel("Link Entry")
        self.download_button = QPushButton("Download")
        self.main_layout = QVBoxLayout()
        self.mp3_checkbox = QCheckBox()
        self.mp4_checkbox = QCheckBox()
        self.media_format = ""
        self.checkbox_button_group = QButtonGroup()
        self.checkbox_buttons_box = QHBoxLayout()
        self.status_menu = QListWidget()
        self.thread_pool = QThreadPool()
        self.active_workers = {}
        self.define_ui()

    def define_ui(self):
        # Add entry label and entry point for Youtube link to main layout
        self.youtube_link_entry.resize(30, 60)
        user_entry_items_container = QHBoxLayout()
        user_entry_items_container.addWidget(self.link_label)
        user_entry_items_container.addWidget(self.youtube_link_entry)
        self.main_layout.addLayout(user_entry_items_container)

        # Add checkboxes to button group
        self.mp3_checkbox.setText("mp3")
        self.mp3_checkbox.clicked.connect(self.checkbox_clicked)
        self.mp4_checkbox.setText("mp4")
        self.mp4_checkbox.clicked.connect(self.checkbox_clicked)
        self.checkbox_button_group.addButton(self.mp3_checkbox)
        self.checkbox_button_group.addButton(self.mp4_checkbox)

        # add checkboxes and download button to main layout
        self.checkbox_buttons_box.addWidget(self.mp3_checkbox)
        self.checkbox_buttons_box.addWidget(self.mp4_checkbox)

        self.download_button.clicked.connect(self.download_button_clicked)
        self.checkbox_buttons_box.addWidget(self.download_button)
        self.main_layout.addLayout(self.checkbox_buttons_box)

        # Add QListWidget to the layout
        self.main_layout.addWidget(self.status_menu)
        self.setLayout(self.main_layout)

    def checkbox_clicked(self):
        """Updates the media_format variable"""
        if self.mp3_checkbox.isChecked():
            self.media_format = "mp3"
        elif self.mp4_checkbox.isChecked():
            self.media_format = "mp4"

    def add_status_menu_items(self):
        """Adds status menu items once a download is started"""
        list_item1 = QListWidgetItem()
        status_menu_items = CustomStatusMenuItems()
        list_item1.setSizeHint(status_menu_items.sizeHint())
        self.status_menu.addItem(list_item1)
        self.status_menu.setItemWidget(list_item1, status_menu_items)
        return status_menu_items

    def download_button_clicked(self):
        """Executes the download thread when the download button is clicked"""
        youtube_link = self.youtube_link_entry.text()
        self.start_download(youtube_link)

    def start_download(self, youtube_link):
        print("Download_method called")
        try:
            status_menu_items = self.add_status_menu_items()
            download_thread = VideoDownloader(youtube_link, self.media_format)
            title = download_thread.get_video_title()
            status_menu_items.set_video_title(title)
            download_thread.progress_updated.connect(status_menu_items.update_progress_bar)
            download_thread.error_occured.connect(status_menu_items.error_occured)
            download_thread.download_finished.connect(status_menu_items.update_status_label)
            download_task = DownloadTask(download_thread)
            self.thread_pool.start(download_task)
        except Exception as e:
            print(e)

    def is_thread_running(self):
        """Checks if there are any active downloads taking place"""
        active_threads = self.thread_pool.activeThreadCount()
        if active_threads > 0:
            return True
        elif active_threads == 0:
            return False

class CustomStatusMenuItems(QWidget):
    def __init__(self):
        super().__init__()
        self.progress_bar = QProgressBar()
        self.status_label = QLabel()
        self.status_label.setText("Waiting for download to start...")
        self.video_title = QLabel()
        self.custom_layout = QVBoxLayout()
        self.custom_layout.setSpacing(0)
        self.custom_layout.addWidget(self.video_title)
        self.custom_layout.addWidget(self.progress_bar)
        self.custom_layout.addWidget(self.status_label)
        self.setLayout(self.custom_layout)

    def update_progress_bar(self, progress):
        """Updates the progress bar of the download"""
        self.progress_bar.setValue(progress)
        if self.progress_bar.text() > "0":
            self.update_status_label("Downloading")

    def update_status_label(self, text):
        """Updates the status label once download is finished"""
        self.status_label.setText(text)

    def set_video_title(self, title):
        """Sets the video name of the video/audio being downloaded"""
        self.video_title.setText(title)

    def error_occured(self, error_message):
        """Sets the downstatus of the video to the error"""
        self.status_label.setText(error_message)
