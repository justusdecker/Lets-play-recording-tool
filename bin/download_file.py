from tkinter.messagebox import showerror
from requests import get
from requests.exceptions import HTTPError, RequestException
import zipfile
from io import BytesIO

def download_file(url: str, filepath: str | None = None, mode: bool = False) -> BytesIO | HTTPError | RequestException | bool:
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
    try:
        r = get(url)
        r.raise_for_status()
        if mode:
            with open(filepath, 'wb') as file:
                file.write(r.content)
        else:
            return BytesIO(r.content)
    except (HTTPError, RequestException) as E:
        return E
          
def download_ffmpeg():
    """
    Downloads FFMPEG from gyan.dev
    """
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    file = download_file(url)
    if file is not None and file is not BytesIO:
        showerror('Cannot download file', f'Statuscode: {file.response.status_code}')
        return
    zip = zipfile.ZipFile(file)
    for ext in ['ffmpeg.exe','ffprobe.exe','ffplay.exe']:
        with open(ext,'wb') as f:
            f.write(zip.read(f'{zip.infolist()[0].filename}bin/{ext}'))
from bin.constants import VERSION 
def get_newest_version_number():
    """ Gets the newest version number Major.Minor Format """
    try:
        r = get('https://justusdecker.pythonanywhere.com/api/version')
        r.raise_for_status()
        return r.json()
    except (HTTPError, RequestException) as E:
        return {'version': ''.join(VERSION.split('.')[0:2])}
        