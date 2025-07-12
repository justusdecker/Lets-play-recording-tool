__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.5.13"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.obs import OBSObserver
from shutil import copyfile
from tkinter.filedialog import askdirectory

LP_PATH = 'lets_plays.csv'

from bin.data_access import *

from bin.text_manipulation import (
    inf,
    deb,
    err,
    color816
)

from bin.others import binps, input_episode_range, toast_finished

from bin.constants import *

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


class GenericWorkFlow:
    def __init__(self, folder: str, finish_message: str):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.run()
    
    @property
    def rng(self) -> tuple[int,int]:
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
    def run(self):
        cnef(self.auto_create_folder_path)
        self.letsplay = LetsPlay(LP_PATH)
        self.ui_result = input_episode_range(self.letsplay.get_episode_ammount(),self.letsplay.get_names())
        if self.ui_result is not None:
            self.lpid,self.epr = self.ui_result
            self.lp_name = self.letsplay.get_name(self.lpid)
            self.ep_path = self.letsplay.get_episode_path(self.lpid)
            self.episode = Episode(self.ep_path)
        
    def user_workflow(self):
        toast_finished(self.finish_message)

class GenerateThumbnailWF(GenericWorkFlow):
    """
    Generating Thumbnails based on the thumbnail automation data
    """
    def __init__(self):
        super().__init__(folder = THUMBNAIL_FOLDER, finish_message = 'Thumbnail Generation')
        self.user_workflow()
        
    def user_workflow(self):
        TG = ThumbnailGenerator()
        tad = self.letsplay.get_tad_path(self.lpid)
        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
            if not tad:
                return
            p = f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
            TG.generate(
                str(i+1),
                video_path,
                tad,
                f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
                )
            self.episode.set_thumbnail_path(i,p)
            self.episode.save()
        super().user_workflow()

class ExtractAudioWF(GenericWorkFlow):
    """
    Audio Extraction from Video
    """
    def __init__(self):
        super().__init__(folder=AUDIO_FOLDER, finish_message='Audio extraction finished')
        self.user_workflow()
    def user_workflow(self):
        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
                                
            t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic.aac',f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop.aac'
            
            inf(f'Start extract tracks from {video_path}')

            ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':t1_path, '__OUT2__':t2_path})

            self.episode.set_audio_mic_path(i,t1_path)
            self.episode.set_audio_desktop_path(i,t2_path)
            
            self.episode.save()
        super().user_workflow()
     
class FixAudioWF(GenericWorkFlow):
    """
    Fixes your mic recording
    
    Uses filters:
    - Lowpass
    - Highpass
    - Loudness Normalize
    - Limiter
    - & later noise reduction
    """
    def __init__(self):
        super().__init__(folder = FIXED_AUDIO_FOLDER, finish_message = 'Audio Fix')
        self.user_workflow()
    def user_workflow(self):
        
        for i in range(*self.rng): 
            audio_mic_path = self.episode.get_audio_mic_path(i)
            
            dest = f'{FIXED_AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop_fixed.mp3'
            
            cnef(TEMP_FOLDER)
            
            ffmpeg_run(FFMPEG_AUDIO_PF_LN_L,{'__IN__': audio_mic_path,'__OUT__':f'{TEMP_FOLDER}wfr1.mp3'})
            
            #! ADD NEW Noise Reduction method
            
            self.episode.set_audio_mic_edit2_path(i,dest)
            self.episode.save()
            super().user_workflow()

class GetSilenceWF(GenericWorkFlow):
    def __init__(self):
        super().__init__(folder=TEMP_FOLDER, finish_message='Extract Silence')
        self.user_workflow()
    def user_workflow(self):
        cnef(TEMP_FOLDER+self.lp_name)
        for i in range(*self.rng): 
            deb(f'[Analyze Silence] of ep: {i+1}')
            filepath = self.episode.get_audio_mic_path(i)
            result = get_silence(filepath)
            
            cnef(f'{TEMP_FOLDER}noise')
            l = len(result)
            if l > 100: # a bunch of samples so only take ...
                skipper = 10
            elif l > 50:
                skipper = 5
            else:
                skipper = 0
            deb(f'[Extract Silence] of ep: {i+1}')
            for idx,key in enumerate(result):
                if skipper != 0:
                    if idx % skipper != 0: continue
                start, end = result[key][0],result[key][1] - result[key][0]
                if start == end: continue
                
                ffmpeg_run(
                    FFMPEG_EXPORT_SILENCE,
                    {
                        '__IN__': filepath,
                        '__SS__': start,
                        '__TO__': end,
                        '__OUT__': f'{TEMP_FOLDER}noise\\{i}_{key}_{self.lp_name}.mp3'})
        super().user_workflow()

class DeployWF(GenericWorkFlow):
    """
    Deploying is for moving lets play data & files to other folders & drives
    
    This will create on the top one markdown file that contains essential data for the videoupload
    
    The user only need to copy & paste
    """
    def __init__(self):
        super().__init__(folder=TEMP_FOLDER, finish_message='Deploy')
        self.user_workflow()
    def user_workflow(self):
        #getting lets play info
    # name etc. to write it in the header: follows below
        name = self.letsplay.get_name(id)
        description = self.letsplay.get_description(id)
        game_name = self.letsplay.get_game_name(id)
        
        # Creating Markdown Header
        MD = f"""
# {name}
## {game_name}

```
{description}
```

### {self.episode.row} episodes
    """
        #ask the user about the target destination for the files
        # will print an error & return if empty
        dst = askdirectory() + '/'
        if not dst:
            err(ERROR_006)
            return
        
        
        for i in range(self.episode.row):
            """
            In this loop we do a lot:
            - fetch the data from the episode
                We only need the final_video_path
                And the thumbnail_path
            - We create two new paths thats the destinations for video & thumbnail
            - Copying the files over to the new location
            - Append essential data to the Markdown
            """
            
            
            video_path = self.episode.get_final_video_path(i)
            thumbnail_path = self.episode.get_thumbnail_path(i)
            
            if not isfile(video_path) or not isfile(thumbnail_path):
                err(ERROR_007)
                return
            vpe = video_path.split('.')[1]
            
            new_video_path = f'{dst}{i+1}_video_{game_name}.{vpe}'
            new_thumbnail_path = f'{dst}{i+1}_thumbnail_{game_name}.png'
            
            copyfile(video_path,new_video_path)
            copyfile(thumbnail_path,new_thumbnail_path)
            
            MD += f"""
#### {i}
- {new_video_path.split('/')[-1]}
- ![IMAGE]({new_thumbnail_path.split('/')[-1]})
        """
    
        #At the end we write all stuff in MD to disk
        file_write('test.md',MD)
        
        super().user_workflow()

class CompareAndRenderWF(GenericWorkFlow):
    """
    CAAR
    ---
    Audio Compare & render the results at the end
    
    Uses FFMPEG to edit audio & render video in bulk.
    
    
    .. render_queue::
        Because rendering takes a long time the paths will be stored temporary in this list. Formatted like: (video, audio, index)
    
    .. result_file_path::
        **AUDIO_FOLDER/**{`ep_index` + `1`}_{`name`}_final.mp3
    """
    def __init__(self):
        super().__init__(folder=TEMP_FOLDER, finish_message="CAAR")
        self.user_workflow()
    def user_workflow(self):
        
        rendering_queue = []

        paths = [[i, self.episode.get_audio_mic_edit2_path(i), self.episode.get_audio_desktop_path(i), self.episode.get_video_path(i)] for i in range(*self.rng)]
        AP = AudioPlayer(paths)
        AP.run()
        result = AP.audio_list
        del AP
        for i, mic, desk, vid, vol in result:
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'
            inf(f'[{i}]({vol}) - {tmp_audio_path}')
            ffmpeg_run(
                FFMPEG_AUDIO_COMBINE,
                {
                    '__IN1__':mic,
                    '__IN2__': desk,
                    '__VOLUME1__': str(1.0),
                    '__VOLUME2__': str(vol),
                    '__OUT__':tmp_audio_path
                    }
                )
            rendering_queue.append((vid, tmp_audio_path, i))
        toast_finished("[1/2] Audio combine")   

        path_ending = f'_{self.letsplay.get_game_name(self.lpid)}_final.mp4'
        cnef(VIDEO_FOLDER)
        for video, audio, index in rendering_queue:
            # Here: rendering my lord :D
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'
            inf(f'{video}\n{audio}\n{index}')
            inf(str({
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }))
            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )

            # writes the final_video_path in episodes so the user can get this video by deploy
            self.episode.set_final_video_path(index,final_path)
            self.episode.save()
        super().user_workflow()
#! compare & render

#? generate noise profile



def __generate_noise_profile(filepath: str, lp_name: str):
    ffmpeg_run(SOX_AUDIO_NOISE_REDUCTION,{'__IN__': '', '__OUT__': f'{TEMP_FOLDER}{lp_name}\\noise_profiles\\'})

def generate_noise_profile():
    cnef(TEMP_FOLDER)
    letsplay = LetsPlay(LP_PATH)
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    if res is not None:
        lp,epr = res
        lp_name = letsplay.get_name(lp)
        ep_path = letsplay.get_episode_path(lp)
        
        episode = Episode(ep_path)
        cnef(f'{TEMP_FOLDER}{lp_name}\\noise_profiles\\')
        for i in range(epr[0],epr[1]+(1 if epr[0] == epr[1] else 0)): # This is a fix for the unneccessary long approch if else bs
            # TODO Get audio snippets
            __generate_noise_profile()
            #__extract_silence(episode.get_audio_mic_path(i), lp_name, i)
            
        
    toast_finished("Fetch Audio")

def get_silence(filepath: str,silence: int = -50, duration: float = 0.5) -> dict[int, tuple[float, float]]:
    """
    Get the silence from a audiotrack
    
    Noise is considered:
        Silence below `silence`dB & the length of the silence must be at least `duration`.
    
    .. args::
        silence : threshold in decibel
            
        duration : time in seconds

    .. returns::
        dict[int, tuple[float, float]]
            {0: (`start`, `end`)...}
    """

    result = ffmpeg_run(FFMPEG_GET_SILENCE,{'__IN__':filepath, '__DUR__': duration, '__SIL__': silence})
    data = []
    for line in result.stderr.split('\n'):   
        if line.startswith('[silencedetect'):
            args = line.split(']')[1].split(' ')
            data.append(float(args[2]))
    return {i: (data[i] , data[i+1]) for i in range(0,len(data),2)}
  
    letsplay = LetsPlay(LP_PATH)
    
    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
    
    if res is not None:
        lp,epr = res
        ep_path = letsplay.get_episode_path(lp)
        ep = Episode(ep_path)

        rendering_queue = []
    
        cnef(TEMP_FOLDER)
        paths = [[i, ep.get_audio_mic_edit2_path(i), ep.get_audio_desktop_path(i), ep.get_video_path(i)] for i in range(epr[0],epr[1]+(1 if epr[0] == epr[1] else 0))]
        AP = AudioPlayer(paths)
        AP.run()
        result = AP.audio_list
        del AP
        for i, mic, desk, vid, vol in result:
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'
            inf(f'[{i}]({vol}) - {tmp_audio_path}')
            ffmpeg_run(
                FFMPEG_AUDIO_COMBINE,
                {
                    '__IN1__':mic,
                    '__IN2__': desk,
                    '__VOLUME1__': str(1.0),
                    '__VOLUME2__': str(vol),
                    '__OUT__':tmp_audio_path
                    }
                )
            rendering_queue.append((vid, tmp_audio_path, i))
        toast_finished("[1/2] Audio combine")   
        #for i in range(epr[0],epr[1]+(1 if epr[0] == epr[1] else 0)): # This is a fix for the unneccessary long approch if else bs
        #    
        #    # Get paths
        #    mic = ep.get_audio_mic_edit2_path(i)
        #    desk = ep.get_audio_desktop_path(i)
        #    vid = ep.get_video_path(i)
        #    
        #    inf(f'{mic} {desk}')
        #    
        #    
        #    # Get the audio volume for track 2 <- will be enhanced further after 1.0 to support more than 2 tracks
        #    AP = AudioPlayer(mic, desk)
        #    AP.run()
        #    volume = AP.vol
        #    del AP
        #    
        #    tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'
        #    
        #    # This combines the mic & desktop audio & apply volume manipulation
        #    ffmpeg_run(
        #        FFMPEG_AUDIO_COMBINE,
        #        {
        #            '__IN1__':mic,
        #            '__IN2__': desk,
        #            '__VOLUME1__': str(1.0),
        #            '__VOLUME2__': str(volume),
        #            '__OUT__':tmp_audio_path
        #            }
        #        )
        #    rendering_queue.append((vid, tmp_audio_path, i))
        #
        path_ending = f'_{letsplay.get_game_name(lp)}_final.mp4'
        cnef(VIDEO_FOLDER)
        for video, audio, index in rendering_queue:
            # Here: rendering my lord :D
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'
            inf(f'{video}\n{audio}\n{index}')
            inf(str({
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }))
            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )

            # writes the final_video_path in episodes so the user can get this video by deploy
            ep.set_final_video_path(index,final_path)
            ep.save()
        toast_finished("[2/2] Video Render")   

    """
    Deploying is for moving lets play data & files to other folders & drives
    
    This will create on the top one markdown file that contains essential data for the videoupload
    
    The user only need to copy & paste
    """
    
    
    #getting lets play info
    # name etc. to write it in the header: follows below
    name = lp.get_name(id)
    description = lp.get_description(id)
    game_name = lp.get_game_name(id)
    eps = ep
    
    # Creating Markdown Header
    MD = f"""
# {name}
## {game_name}

```
{description}
```

### {eps.row} episodes
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
#### {i}
- {new_video_path.split('/')[-1]}
- ![IMAGE]({new_thumbnail_path.split('/')[-1]})
        """
    
    #At the end we write all stuff in MD to disk
    file_write('test.md',MD)