import yt_dlp
from PyQt6.QtCore import QDir, QThread, pyqtSignal, QRunnable, QObject
from Settings import JSON_file_methods as jsn
import traceback
import re
from yt_dlp.utils import ExtractorError, DownloadError


class VideoDownloader(QObject):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str)
    error_occured = pyqtSignal(str)

    def __init__(self, link, media_format):
        super().__init__()
        self.download_link = link
        self.media_format = media_format
        self.download_path = ""
        self.get_download_path()
        self.remove_after_second_equals()

    def run(self):
        print("The file path is", self.download_path)
        print("The download link is", self.download_link)
        print("The media format is", self.media_format)

        base_config = {
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            'progress_hooks': [self.download_progress_hook]
        }

        if self.media_format == "mp3":
            base_config['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.media_format,
                'preferredquality': '0',
            }]
        else:
            base_config.pop('postprocessors', None)

        ydl_opts = base_config

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.download_link])
                self.download_finished.emit("Downloaded Successfully")
            except yt_dlp.utils.DownloadError:
                self.error_occured.emit("Network error, move to a stable network")
            except yt_dlp.utils.ExtractorError:
                self.error_occured.emit("Extraction error, try again")

    def download_progress_hook(self, d):
        # print("First entrance into method, the status is", d['status'])
        if d['status'] == 'downloading':
            try:
                clean_percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str']).strip('%')
                float_percent = float(clean_percent_str)
                int_percent = int(float_percent)
                self.progress_updated.emit(int_percent)
            except Exception:
                pass

    def get_video_title(self):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(self.download_link, download=False)
                video_title = info.get('title', 'Unknown')
                return video_title
        except Exception as e:
            error_message = "Invalid URL"
            self.error_occured.emit(error_message)

    def remove_after_second_equals(self):
        # Split the string by '='
        parts = self.download_link.split('=')

        # If there are at least two parts, join the first two parts back together with '='
        if len(parts) > 2:
            self.download_link = '='.join(parts[:2])
        else:
            print("The new url is", self.download_link)

    def get_download_path(self):
        self.download_path = jsn.read_json_file_path()

class DownloadTask(QRunnable):
    def __init__(self, downloader):
        super().__init__()
        self.downloader = downloader

    def run(self):
        self.downloader.run()