from requests import get
from io import BytesIO
from requests.exceptions import HTTPError, RequestException
import zipfile

from src.api.msgbox import msgbox, MSGBoxPresets, SoundFlags

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
    if filepath is None: raise TypeError()
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
        msgbox(
            'Cannot download file',
            f'Statuscode: {file.response.status_code}',
            MSGBoxPresets.SYSTEM_ALERT,
            SoundFlags.ERROR
        )
        
        return
    zip = zipfile.ZipFile(file)
    for ext in ['ffmpeg.exe','ffprobe.exe','ffplay.exe']:
        with open(ext,'wb') as f:
            f.write(zip.read(f'{zip.infolist()[0].filename}bin/{ext}'))