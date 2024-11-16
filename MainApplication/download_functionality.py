import yt_dlp
from PyQt6.QtCore import QDir, QThread, pyqtSignal, QRunnable, QObject
from imageio.plugins.ffmpeg import download
from Settings import JSON_file_methods as jsn
"""Error log: Doesn't download mp3 version of the same video. So if video version exists, video is not downloaded
We need to add functionality that handles errors better 
"""


class VideoDownloader(QObject):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str)

    def __init__(self, link, media_format):
        super().__init__()
        self.download_link = link
        self.media_format = media_format
        self.download_path = ""
        self.get_download_path()
        self.remove_after_second_equals()

    def run(self):
        print("The file path is", self.download_path)

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
            except Exception as e:
                print(f"An error occurred: {e}")

    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = int(float(d['_percent_str'].strip('%')))
                self.progress_updated.emit(percent)
            except (ValueError, KeyError):
                pass

    def get_video_title(self):
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(self.download_link, download=False)
                video_title = info.get('title', 'Unknown')
                return video_title
        except Exception as e:
            return f"Error: {e}"

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