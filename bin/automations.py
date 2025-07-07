__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.116"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.obs import OBSObserver
from shutil import copyfile
from tkinter.filedialog import askdirectory

LP_PATH = 'lets_plays.csv'

from bin.data_access import (
    file_read,
    file_write,
    csv_write,
    cnef,
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

from tkinter.filedialog import askopenfilename as aofn

from bin.others import binps, input_episode_range

from bin.constants import (
    ERROR_002,
    ERROR_004,
    ERROR_005,
    ERROR_006,
    ERROR_007,
    AUDIO_FOLDER,
    FIXED_AUDIO_FOLDER,
    THUMBNAIL_FOLDER,
    FFMPEG_EXTRACT,
    FFMPEG_LOUDNESS_NORMALIZATION,
    FFMPEG_LIMITER,
    FFMPEG_VOLUME_APPLIER,
    FFMPEG_AUDIO_COMBINE,
    ffmpeg_run
)

from bin.thumbnail import ThumbnailGenerator

from os.path import isfile

from bin.audio_player import AudioPlayer

def obs_connect(ep: Episode):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up or a keyboard interrupt happens
    """
    OBSO = OBSObserver()
    if not OBSO.isconnected:
        err(ERROR_004)
    while OBSO.isconnected:
        try:
            print(OBSO.timecode) #! Will be changed to a one line print by using esc seqs
            OBSO.update(ep)
        except KeyboardInterrupt:
            err(ERROR_005)
            break

def create_new_lp_file():
    """
    Creates a new CSV File in Lets Play Format
    
    Already existing will cause an error message
    """
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    if not isfile(LP_PATH):
        csv_write(LP_PATH,[[binps(f'{key}: ') if key != 'version' else file_read('version.txt') for key in LP_KEYS]])
    else:
        err(ERROR_002)

def create_new_ep_file(filepath: str):
    """
    Creates a new CSV File in Episode Format
    
    Already existing will cause an error message
    """
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    
    if not isfile(filepath):
        csv_write(filepath,[[binps(f'{key}: ') for key in EP_KEYS]])
    else:
        err(ERROR_002)

def __fetch_audio(episode: Episode,i: int,lp_name: str):
    """
    Get 2 Track from the original video file & save them & their path
    """
    video_path = episode.get_video_path(i)
                                
    t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{lp_name}_track_mic.mp3',f'{AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop.mp3'
    
    inf(f'Start extract track 1 from {t1_path}')
    ffmpeg_run(FFMPEG_EXTRACT,{'__IN__':video_path,'__OUT__':t1_path,'__MAPPING__':str(1)})
    #extract_audio(video_path,t1_path,1)

    episode.set_audio_mic_path(i,t1_path)
    
    inf(f'Start extract track 2 from {t2_path}')
    ffmpeg_run(FFMPEG_EXTRACT,{'__IN__':video_path,'__OUT__':t2_path,'__MAPPING__':str(2)})
    #extract_audio(video_path,t2_path,2)
    
    episode.set_audio_desktop_path(i,t2_path)
    
    episode.save()

def fetch_audio():
    cnef(AUDIO_FOLDER)
    letsplay = LetsPlay(LP_PATH)
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    if res is not None:
        lp,epr = res
        lp_name = letsplay.get_name(lp)
        ep_path = letsplay.get_episode_path(lp)
        if epr[0] == epr[1]:
            __fetch_audio(Episode(ep_path),epr[0],lp_name)
        else:
            episode = Episode(ep_path)
            for i in range(epr[0],epr[1]):
                __fetch_audio(episode,i,lp_name)
  
def __fix_audio(episode: Episode,i: int, lp_name):
    """
    Take the audio & uses limiter & loudness normalization to fix the most issues in the mic record.
    
    It fixes only the first Track.
    """
    audio_mic_path = episode.get_audio_mic_path(i)
    audio_desktop_path = episode.get_audio_desktop_path(i)
    
    t1_path, t2_path = f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_mic_ln.mp3',f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop_ln.mp3'
    
    t3_path, t4_path = f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_mic_fixed.mp3',f'{FIXED_AUDIO_FOLDER}{i+1}_{lp_name}_track_desktop_fixed.mp3'
    
    inf(f'Start normalize track 1 to {t1_path}')
    #loudness_normalization(audio_mic_path, t1_path)
    ffmpeg_run(FFMPEG_LOUDNESS_NORMALIZATION,{'__IN__': audio_mic_path,'__OUT__':t1_path})
    inf(f'Start limit track 1 to {t3_path}')
    #limiter(t1_path, t3_path)
    ffmpeg_run(FFMPEG_LIMITER,{'__IN__': t1_path,'__OUT__':t3_path})
    
    #inf(f'Start normalize track 2 to {t2_path}')
    #loudness_normalization(audio_desktop_path, t2_path)
    
    #inf(f'Start limit track 2 to {t4_path}')
    #limiter(t2_path, t4_path)

def fix_audio():
    cnef(FIXED_AUDIO_FOLDER)
    letsplay = LetsPlay(LP_PATH)
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    if res is not None:
        lp,epr = res
        lp_name = letsplay.get_name(lp)
        ep_path = letsplay.get_episode_path(lp)
        ep = Episode(ep_path)
        if epr[0] == epr[1]:
            __fix_audio(ep,epr[0],lp_name)
        else:
            
            for i in range(epr[0],epr[1]):
                __fix_audio(ep,i,lp_name)
                
def __gen_thumbnail(
    thumbnail_gen: ThumbnailGenerator,
    lp_name: str,
    episode: Episode,
    i: int,
    tad: dict):
    """
    Generate a thumbnail
    Based on the given tad elements will be placed.
    Saves the image & their path
    """

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

def gen_thumbnail():
    letsplay = LetsPlay(LP_PATH)
    TG = ThumbnailGenerator()
    cnef(THUMBNAIL_FOLDER)
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    if res is not None:
        lp,epr = res
        lp_name = letsplay.get_name(lp)
        ep_path = letsplay.get_episode_path(lp)
        eps = Episode(ep_path)
        inf('Please answer the filedialog')
        tad = aofn(filetypes=[['JSON','*.json']])
        if epr[0] == epr[1]:
            __gen_thumbnail(TG,lp_name,eps,epr[0],tad)
            
        else:
            
            for i in range(epr[0],epr[1]):
                __gen_thumbnail(TG,lp_name,eps,i,tad)

def compare_audio():
    # final audio path
    # {episode_number}_{letsplay_name}_final.mp3
    letsplay = LetsPlay(LP_PATH)
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    if res is not None:
        lp,epr = res
        ep_path = letsplay.get_episode_path(lp)
        ep = Episode(ep_path)
        if epr[0] == epr[1]:
            final_path = f'{epr[0]}_{letsplay.get_game_name(lp)}.mp3'
            mic = ep.get_audio_mic_path(epr[0])
            desk = ep.get_audio_desktop_path(epr[0])
            
            AP = AudioPlayer(mic, desk)
            AP.run()
            volume = AP.vol
            del AP
            ffmpeg_run(FFMPEG_AUDIO_COMBINE,{'__IN1__':mic,'__IN2__': desk,'__VOLUME1__': str(1.0),'__VOLUME2__': str(volume),'__OUT__':'out.mp3'})
            print(mic, desk, volume)
            ep.set_final_audio_path(epr[0],final_path)
            ep.save()
        else:
            for i in range(epr[0],epr[1]):
                final_path = f'{i}_{letsplay.get_game_name(lp)}.mp3'
                mic = ep.get_audio_mic_path(i)
                desk = ep.get_audio_desktop_path(i)
                inf(f'{mic} {desk}')
                AP = AudioPlayer(mic, desk)
                AP.run()
                volume = AP.vol
                del AP
                ffmpeg_run(FFMPEG_VOLUME_APPLIER,{'__IN__':desk,'__VOLUME__': str(volume)})
                ffmpeg_run(FFMPEG_AUDIO_COMBINE,{'__IN__':mic,'__OUT__':final_path})
                print(mic, desk, volume)
                ep.set_final_audio_path(i,final_path)
                ep.save()
 
def deploy(lp: LetsPlay, ep: Episode,id: int):
    """
    Deploying is for moving lets play data & files to other folders & drives
    
    This will create on the top one markdown file that contains essential data for the videoupload
    
    The user only need to copy & paste
    """
    
    
    #getting lets play info
    # name etc. to write it in the header: follows below
    name = lp.get_name(id)
    game_name = lp.get_game_name(id)
    eps = ep
    
    # Creating Markdown Header
    MD = f"""
# {name}
{game_name}
{eps.row} episodes
    """
    #ask the user about the target destination for the files
    # will print an error & return if empty
    dst = askdirectory() + '/'
    if not dst:
        err(ERROR_006)
        return
    
    
    for i in range(eps.row):
        """
        In this loop we do a lot:
        - fetch the data from the episode
            We only need the final_video_path
            And the thumbnail_path
        - We create two new paths thats the destinations for video & thumbnail
        - Copying the files over to the new location
        - Append essential data to the Markdown
        """
        
        
        video_path = eps.get_final_video_path(i)
        thumbnail_path = eps.get_thumbnail_path(i)
        
        if not isfile(video_path) or not isfile(thumbnail_path):
            err(ERROR_007)
            return
        vpe = video_path.split('.')[1]
        
        new_video_path = f'{dst}{i+1}_video_{game_name}.{vpe}'
        new_thumbnail_path = f'{dst}{i+1}_thumbnail_{game_name}.png'
        
        copyfile(video_path,new_video_path)
        copyfile(thumbnail_path,new_thumbnail_path)
        
        MD += f"""
## {i}
- {new_video_path.split('/')[-1]}
- ![IMAGE]({new_thumbnail_path.split('/')[-1]})
        """
    
    #At the end we write all stuff in MD to disk
    file_write('test.md',MD)