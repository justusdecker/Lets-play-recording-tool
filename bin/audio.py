__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.117"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from os.path import isfile
from moviepy.audio.io.AudioFileClip import AudioFileClip
import subprocess

def get_audio_length(filename):
    if isfile(filename):
        return AudioFileClip(filename).duration
    return -1

def combine_audio(t1: str,t2: str,st: str,et: str):
    """
    Combine two audio files
    
    .. st::
        starttime in HH:MM:SS format must be a `str`
    .. et::
        endtime in HH:MM:SS format must be a `str`
    """
    #ffmpeg -ss 00:01:00 -to 00:02:00 -i {input_file} -c copy {result_file}
    
    """
    
                    '-ss',
                    f'{st}',
                    'to',
                    f'{et}',
                    
                    
                    '-ss',
                    f'{st}',
                    'to',
                    f'{et}',
                    
                      
    """
    subprocess.run(
                (
                    'ffmpeg',
                    '-y',               # Will replace existing output
                    
                    '-i',               # Input filepath 1
                    f"{t1}",            # Input filepath 1
                    '-ss',
                    f'{st}',
                    'to',
                    f'{et}',
                    
                    '-i',               # Input filepath 2
                    f"{t2}",            # Input filepath 2
                    '-ss',
                    f'{st}',
                    'to',
                    f'{et}',
                    
                    '-filter_complex',  #for merging
                    'amerge=inputs=2',  # For merging
                    '-ac', '2',         # Set audio channel
                    f"temp.mp3"         # output filepath
                    ),
                subprocess.CREATE_NO_WINDOW,
                shell= True
                )
def extract_audio(fr:str,to:str,t:int=1):
    subprocess.run(
                (
                    'ffmpeg',
                    '-y',
                    '-i',
                    f"{fr}",
                    '-map',
                    f'0:{t}',
                    f"{to}"
                    ),
                subprocess.CREATE_NO_WINDOW,
                shell= True
                )
def loudness_normalization(filepath,savepath,decibel:int = -15):
        
    subprocess.run(
            [
                'ffmpeg',
                '-y',
                '-i',
                filepath,
                '-af',
                f'loudnorm={decibel}',
                savepath
                ],
                subprocess.CREATE_NO_WINDOW,
                shell= True
            )
def limiter(i_filename: str,
                o_filename: str,
                limiter: str = '0/-3|10/-3|20/-3'):
    subprocess.run(
            [
                'ffmpeg',
                '-y',
                '-i',
                i_filename,
                #'-c:a',     #Copy Audio. No Reencoding
                #'-af compand=0 0:1 1:{limiter}:0.01:12:0:0',
                '-af',
                f'compand=0|0:1|1:{limiter}:0.1:0:0:0',
                o_filename
                ]
            )
        
def cvt_audio(filename:str,#call
                    fr:str= '.mp3',
                    to:str= '.wav'):
    """Convert Audio Formats"""
    subprocess.run(
        [
            'ffmpeg',
            
            '-n',
            '-i',
            filename.split('.')[0] + fr,
            filename.split('.')[0] + to
            ],
            subprocess.CREATE_NO_WINDOW,
            shell= True
        )
    return filename.split('.')[0] + to

def cvtAudioNew(fileName:str,#call
                    fromType:str= '.mp3',
                    toType:str= '.wav'):
    """Convert Audio Formats"""
    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-i',
            fileName.split('.')[0] + fromType,
            'temp.wav',
            '-ac',
            '1'
            ],
            subprocess.CREATE_NO_WINDOW,
            shell=True
        )
    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-i',
            'temp.wav',
            
            '-ar',
            '8000',
            '-ac',
            '1',
            '-c:a',
            'pcm_s16le',
            fileName.split('.')[0] + toType
            ],
            subprocess.CREATE_NO_WINDOW,
            shell= True
        )
    #ffmpeg -i input.wav -ar 8000 -ac 1 -c:a pcm_s16le output.wa
    return fileName.split('.')[0] + toType