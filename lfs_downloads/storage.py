import os
from django.core.files.storage import FileSystemStorage

from .settings import LFS_DOWNLOADS_PRIVATE_FOLDER, LFS_DOWNLOADS_DOWNLOAD_LIMIT


class LFSDownloadsHiddenStorage(FileSystemStorage):
    def __init__(self, location=LFS_DOWNLOADS_PRIVATE_FOLDER, base_url=None):
        self.location = os.path.abspath(location)
        self.base_url = base_url
