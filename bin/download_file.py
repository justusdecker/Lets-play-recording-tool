import requests
import zipfile
from io import BytesIO

def download_file(url: str, filepath: str | None = None, mode: bool = False) -> BytesIO | None:
    """
    
    Mode:
        True: Returns None & saves file to disk
        False: Returns BytesIO
    """
    r = requests.get(url)
    if mode:
        with open(filepath, 'wb') as file:
            file.write(r.content)
    else:
        return BytesIO(r.content)


def download_ffmpeg():
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    ffmpeg_path = 'ffmpeg.exe'
    ffprobe_path = 'ffprobe.exe'
    ffplay_path = 'ffplay.exe'
    fetch_from = 'bin\\'
    file = download_file(url)
    
    zip = zipfile.ZipFile(file)
    print(zip.getinfo()[0])
    with open('ffmpeg.exe','wb') as f:
        
        f.write(zip.read(f'{zip.getinfo()[0].filename}/bin/ffmpeg.exe'))