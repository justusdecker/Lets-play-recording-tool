from bin.audio import extract_audio, loudness_normalization, limiter
from bin.obs import OBSObserver
from shutil import copyfile
from tkinter.filedialog import askdirectory

LP_PATH = 'lets_plays.csv'

from bin.data_access import (
    file_read,
    file_write,
    csv_write,
    Episode,
    LetsPlay,
    EP_KEYS,
    LP_KEYS
)

from bin.text_manipulation import (
    inf,
    err,
    color816
)

from bin.others import binps

from bin.constants import (
    ERROR_002,
    ERROR_004,
    ERROR_005,
    ERROR_006,
    AUDIO_FOLDER,
    FIXED_AUDIO_FOLDER,
    THUMBNAIL_FOLDER
)

from bin.thumbnail import ThumbnailGenerator

from os.path import isfile

def obs_connect(ep: Episode):
    OBSO = OBSObserver()
    if not OBSO.isconnected:
        err(ERROR_004)
    while OBSO.isconnected:
        try:
            print(OBSO.timecode)
            OBSO.update(ep)
            
        except KeyboardInterrupt:
            err(ERROR_005)
            break

def create_new_lp_file():
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    if not isfile(LP_PATH):
        csv_write(LP_PATH,[[binps(f'{key}: ') if key != 'version' else file_read('version.txt') for key in LP_KEYS]])
    else:
        err(ERROR_002)

def create_new_ep_file(filepath: str):
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    
    if not isfile(filepath):
        csv_write(filepath,[[binps(f'{key}: ') for key in EP_KEYS]])
    else:
        err(ERROR_002)

def fetch_audio(episode: Episode,i: int,lp_name: str):
    video_path = episode.get_video_path(i)
                                
    t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{lp_name}_track_mic.mp3',f'{AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop.mp3'
    
    inf(f'Start extract track 1 from {t1_path}')
    extract_audio(video_path,t1_path,1)

    episode.set_audio_mic_path(i,t1_path)
    
    inf(f'Start extract track 2 from {t2_path}')
    extract_audio(video_path,t2_path,2)
    
    episode.set_audio_desktop_path(i,t2_path)
    
    episode.save()
  
def fix_audio(episode: Episode,i: int, lp_name):

    audio_mic_path = episode.get_audio_mic_path(i)
    audio_desktop_path = episode.get_audio_desktop_path(i)
    
    t1_path, t2_path = f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_mic_ln.mp3',f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop_ln.mp3'
    
    t3_path, t4_path = f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_mic_fixed.mp3',f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop_fixed.mp3'
    
    inf(f'Start normalize track 1 to {t1_path}')
    loudness_normalization(audio_mic_path, t1_path)
    
    inf(f'Start limit track 1 to {t3_path}')
    limiter(t1_path, t3_path)
    
    #inf(f'Start normalize track 2 to {t2_path}')
    #loudness_normalization(audio_desktop_path, t2_path)
    
    #inf(f'Start limit track 2 to {t4_path}')
    #limiter(t2_path, t4_path)

def gen_thumbnail(
    thumbnail_gen: ThumbnailGenerator,
    lp_name: str,
    episode: Episode,
    i: int,
    tad: dict):

    video_path = episode.get_video_path(i)
    if not tad:
        return
    p = f'{THUMBNAIL_FOLDER}{i+1}_{lp_name}_thumbnail.png'
    thumbnail_gen.generate(
        str(i+1),
        video_path,
        tad,
        f'{THUMBNAIL_FOLDER}{i+1}_{lp_name}_thumbnail.png'
        )
    episode.set_thumbnail_path(i,p)
    episode.save()


def generate_markdown(lp: LetsPlay, ep: Episode,id: int):
    #getting info
    name = lp.get_name(id)
    game_name = lp.get_game_name(id)
    eps = ep
    # Creating Markdown Header
    MD = f"""
# {name}
{game_name}
{eps.row} episodes
    """
    #copy & paste data
    
    dst = askdirectory()
    print(dst)
    if not dst:
        #dst is not set! Return
        err(ERROR_006)
        return
    
    
    
   
    for i in range(eps.row):
        video_path, audio_mic, audio_desk, thumbnail, _ = eps.read(i)
        #copyfile(video_path,dst + '')
        MD += f"""
## {i}
- {video_path}
- ![IMAGE]({thumbnail})
        """
    
    file_write('test.md',MD)