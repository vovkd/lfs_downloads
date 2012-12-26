from django.conf import settings

LFS_DOWNLOADS_PUBLIC_FOLDER = getattr(settings, 'LFS_DOWNLOADS_PUBLIC_FOLDER')
LFS_DOWNLOADS_PRIVATE_FOLDER = getattr(settings, 'LFS_DOWNLOADS_PRIVATE_FOLDER')
LFS_DOWNLOADS_DOWNLOAD_LIMIT = getattr(settings, 'LFS_DOWNLOADS_DOWNLOAD_LIMIT', 3)
