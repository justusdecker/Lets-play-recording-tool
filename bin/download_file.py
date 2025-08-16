import requests
import zipfile
from io import BytesIO

def download_file(url: str, filepath: str | None = None, mode: bool = False) -> BytesIO | None:
    """
    Downloads a file from the Internet.

    Mode:
        True: 
            Returns None & saves file to disk
            filepath must be specified
        False: 
            Returns BytesIO
            filepath can be all. It is never used anyway
    """
    r = requests.get(url)
    if mode:
        with open(filepath, 'wb') as file:
            file.write(r.content)
    else:
        return BytesIO(r.content)


def download_ffmpeg():
    """
    Downloads FFMPEG from gyan.dev
    """
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    file = download_file(url)
    zip = zipfile.ZipFile(file)
    for ext in ['ffmpeg.exe','ffprobe.exe','ffplay.exe']:
        with open(ext,'wb') as f:
            f.write(zip.read(f'{zip.infolist()[0].filename}bin/{ext}'))