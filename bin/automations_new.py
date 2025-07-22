__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.80"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.obs import OBSObserver
from bin.data_access import Episode, LetsPlay, cnef, json_write
from bin.wintoasty import toast_finished

from bin.ffmpeg import *
from bin.audacity_pipeline import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msgbox

from os import listdir
LP_PATH = 'lets_plays.csv'

from os import getlogin
from os.path import isfile
USERNAME = getlogin()
del getlogin
ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'

AUDIO_FOLDER = f'{ROOT}audio\\'
VIDEO_FOLDER = f'{ROOT}video\\'
TAD_FOLDER = f'{ROOT}tad\\'
TEMP_FOLDER = f'{ROOT}temp\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}audio_fixed\\'

# fix for issue #78
cnef(AUDIO_FOLDER)
cnef(FIXED_AUDIO_FOLDER)
cnef(THUMBNAIL_FOLDER)
cnef(VIDEO_FOLDER)
cnef(TAD_FOLDER)
cnef(TEMP_FOLDER)

DEFAULT_OBS_SETTINGS = {
    "ip": "",
    "port": 1234,
    "pw": "",
    "timeout": 1
}

if not isfile('obs_settings.json'):
        
    
    json_write('obs_settings.json',DEFAULT_OBS_SETTINGS)




from tkinter import Toplevel
from tkinter.ttk import Button, LabeledScale, Label
from bin.lprtplay import play_audio, stop_audio
from tkinter import DoubleVar

from bin.thumbnail import ThumbnailGenerator

class AudioPlayer(Toplevel):
    """
    A Tkinter Toplevel window that functions as a simple audio player.

    This player allows users to play, stop, and navigate through a list of audio
    files. It also provides a volume control and displays the current episode
    number. The audio playback functionality relies on external functions
    `stop_audio`, `ffmpeg_run`, and `play_audio`.
    """
    def __init__(self,paths):
        
        self.audio_list = paths
        print(len(paths))
        self.current_episode = 0
        super().__init__()
        self.isfinished = False
        self.title('Test')
        self.geometry('300x200')
        self.vol = DoubleVar(self,1.0)
        self.volume_slider = LabeledScale(self,self.vol,from_=0.0,to=1.0)
        self.volume_slider.grid(row=0,column=0)
        
        self.play_button = Button(self,text='Play',command=self.play)
        self.play_button.grid(row=1,column=0)
        
        self.stop_button = Button(self,text='Stop',command=self.stop)
        self.stop_button.grid(row=2,column=0)
        self.stop_button.state(['disabled'])
        
        self.down_button = Button(self,text='Down',command=self.episode_down)
        self.down_button.grid(row=3,column=0)
        
        self.curr_ep_label = Label(self,text='')
        self.curr_ep_label.grid(row=3,column=1)
        
        self.up_button = Button(self,text='Up',command=self.episode_up)
        self.up_button.grid(row=3,column=2)
        
        self.finished_button = Button(self,text='Finished', command=self.byebye)
        self.finished_button.grid(row=4,column=0)
    def stop(self,*args):
        """Stops the currently playing audio and updates button states."""
        self.stop_button.state(['disabled'])
        self.play_button.state(['!disabled'])
        stop_audio()
        
    def play(self, *args):
        """Plays the audio for the current episode."""
        print(self.audio_list[self.current_episode])
        self.stop_button.state(['!disabled'])
        self.play_button.state(['disabled'])
        stop_audio()
        ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{'__IN1__':self.audio_list[self.current_episode][1],'__IN2__': self.audio_list[self.current_episode][2],'__VOLUME1__': str(1.0),'__VOLUME2__': str(self.audio_list[self.current_episode][4]),'__OUT__':'temp.mp3'})
        play_audio('temp.mp3')
        
    def byebye(self, *args):
        """Closes the AudioPlayer window and sets the `isfinished` flag to True."""
        self.destroy()
        self.isfinished = True
    def get_volume(self) -> float:
        """Retrieves the current volume level from the volume slider."""
        return float(f'{self.vol.get():.2f}')
    
    def episode_down(self,*args):
        """
        Navigates to the previous audio episode in the list.

        If the current episode is already the first one, it stays at index 0.
        It updates the current episode index, saves the current volume for the
        new episode, and updates the episode label.
        """
        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location
        self.audio_list[self.current_episode][4] = self.get_volume()
        self.curr_ep_label.configure(text=f'{self.current_episode}')
            
    def episode_up(self,*args):
        """
        Navigates to the next audio episode in the list.

        If the current episode is already the last one, it stays at the last index.
        It updates the current episode index, saves the current volume for the
        new episode, and updates the episode label.
        """
        new_location = self.current_episode + 1
        
        l = len(self.audio_list)
        
        if new_location > l - 1:
            self.current_episode = l - 1
            

        else:
            self.current_episode = new_location
        self.audio_list[self.current_episode][4] = self.get_volume()
        self.curr_ep_label.configure(text=f'{self.current_episode}')
        
def obs_connect(ep: Episode,el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        el.btn_connect.configure(text= 'Settings File does not exist!')
        return
    if not OBSO.isconnected:
        el.btn_connect.configure(text= 'No Connection!')
        return
    while OBSO.isconnected:
        el.btn_connect.configure(text= 'Connection established')
        try:
            el.label.configure(text= OBSO.timecode)
            OBSO.update(ep)
        except:
            el.btn_connect.configure(text= 'Unexpected Error happened')
            print('Unexpected Error happened')

class GenericWorkFlow:
    def __init__(self, folder: str, finish_message: str,lpid,epr):
        """
        Initializes a GenericWorkFlow instance, setting up paths, messages,
        and "LetsPlay" episode-related attributes.

        This class serves as a base for workflows that interact with the `LetsPlay` class, 
        managing episode-specific data and providing a windows toast message
        to signal workflow completion.
        """
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        
        self.letsplay = LetsPlay(LP_PATH)
        self.lpid,self.epr = lpid,epr
        self.lp_name = self.letsplay.get_name(self.lpid)
        self.ep_path = self.letsplay.get_episode_path(self.lpid)
        self.episode = Episode(self.ep_path)
    @property
    def rng(self) -> tuple[int,int]:
        """
        Returns the effective episode range as a tuple (start, end).

        The end of the range is inclusive. If the start and end episodes
        in `epr` are the same, the end of the returned range is incremented by 1
        to ensure a valid range for iteration (e.g., (5,5) becomes (5,6)).

        Returns:
            tuple[int, int]: A tuple representing the (start_episode, end_episode)
                             for the workflow.
        """
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
        
    def user_workflow(self):
        """
        Executes the primary user-facing part of the workflow.

        This method currently triggers a 'toast' notification indicating
        the workflow has finished, using the provided `finish_message`
        """
        toast_finished(self.finish_message)
    


class GenerateThumbnailWF(GenericWorkFlow):
    """
    Generating Thumbnails based on the thumbnail automation data
    """
    def __init__(self,lpid,epr,app):
        super().__init__(folder = THUMBNAIL_FOLDER, finish_message = 'Thumbnail Generation',lpid=lpid,epr=epr)
        self.user_workflow(app)
        
    def user_workflow(self):
        TG = ThumbnailGenerator()
        tad = self.letsplay.get_tad_path(self.lpid)

        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
            if not tad:
                return
            p = f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
            #? This generates all images in batch.
            #! If you want to overwrite a single image goto the Fix Image Tab
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
    A workflow class designed to extract audio tracks from video files for a
    given "LetsPlay" episode range.

    This class extends `GenericWorkFlow` and specializes in automating the
    process of extracting microphone and desktop audio tracks from video files,
    saving them to a specified audio folder, and updating the episode's
    metadata with the paths to the extracted audio files. It also provides
    progress updates via an application's progress bar.
    """
    def __init__(self,lpid,epr,app):
        """
        This constructor calls the parent `GenericWorkFlow`'s constructor,
        setting up the audio extraction folder and a finish message.
        It then immediately initiates the audio extraction process by calling
        its own `user_workflow` method, passing the application instance for
        progress updates.
        """
        super().__init__(folder=AUDIO_FOLDER, finish_message='Audio extraction finished',lpid=lpid,epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        """
        Executes the audio extraction process for each episode within the
        defined range.

        For each episode:
        1. Retrieves the video path.
        2. Defines output paths for microphone and desktop audio tracks.
        3. Uses `ffmpeg_run` to extract both audio tracks from the video.
        4. Updates the application's progress bar.
        5. Stores the paths of the extracted audio files in the episode's metadata.
        6. Saves the updated episode metadata.

        After processing all episodes, it re-enables the application's start button
        and calls the parent `user_workflow` to display the completion message.
        """
        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
                       
            t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic.aac',f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop.aac'
            
            ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':t1_path, '__OUT2__':t2_path})
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_audio_mic_path(i,t1_path)
            self.episode.set_audio_desktop_path(i,t2_path)
            
            self.episode.save()

        app.start_btn.state(['!disabled'])
        super().user_workflow()

class FixAudioWF(GenericWorkFlow):
    """
    A workflow class designed to apply various audio processing filters to
    microphone audio tracks extracted from "LetsPlay" videos.

    This class extends `GenericWorkFlow` and specializes in automating the
    process of enhancing microphone audio quality by applying a sequence of
    filters (Lowpass, Highpass, Loudness Normalize, Limiter). It saves the
    processed audio to the `FIXED_AUDIO_FOLDER`, updates the episode's metadata
    with the path to the fixed audio file, and provides progress updates
    via an application's progress bar.
    """
    def __init__(self,lpid, epr,app):
        """
        This constructor calls the parent `GenericWorkFlow`'s constructor,
        setting up the fixed audio folder and a finish message.
        It then immediately initiates the audio fixing process by calling
        its own `user_workflow` method, passing the application instance for
        progress updates.
        """
        super().__init__(FIXED_AUDIO_FOLDER, 'Audio Fix', lpid, epr)
        self.user_workflow(app)
        
    def user_workflow(self,app):
        """
        Executes the audio fixing process for each microphone audio track
        within the defined episode range.

        For each episode:
        1. Retrieves the path to the original microphone audio track.
        2. Defines the destination path for the fixed audio file.
        3. Ensures a temporary folder exists (`cnef` to create/ensure folder).
        4. Uses `ffmpeg_run` to apply a predefined set of audio filters
           (Lowpass, Highpass, Loudness Normalize, Limiter) to the microphone track.
           (`FFMPEG_AUDIO_PF_LN_L` and `ffmpeg_run` are assumed external).
        5. Updates the application's progress bar.
        6. Stores the path of the fixed audio file in the episode's metadata
           as `audio_mic_edit1_path`.
        7. Saves the updated episode metadata.

        After processing all episodes, it re-enables the application's start button
        and calls the parent `user_workflow` to display the completion message.
        """
        for i in range(*self.rng): 
            audio_mic_path = self.episode.get_audio_mic_path(i)
            # Filters
            # - Lowpass
            # - Highpass
            # - Loudness Normalize
            # - Limiter
            dest = f'{FIXED_AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic_fixed.aac'
            
            cnef(TEMP_FOLDER)
            
            ffmpeg_run(FFMPEG_AUDIO_PF_LN_L,{'__IN__': audio_mic_path,'__OUT__':dest})
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_audio_mic_edit1_path(i,dest)
            self.episode.save()
        app.start_btn.state(['!disabled'])
        super().user_workflow()

class SendToAudacityWF(GenericWorkFlow):
    """
    A workflow class designed to integrate with Audacity for further audio
    processing, specifically for importing fixed microphone audio tracks and
    then handling the exported results.

    This class extends `GenericWorkFlow` and automates the process of:
    1. Establishing a connection with Audacity via its mod-pipe.
    2. Importing processed microphone audio tracks into Audacity.
    3. Guiding the user through the export process in Audacity (manual step for Noise Reduction).
    4. Converting the exported audio files to AAC format.
    5. Updating the episode's metadata with the paths to the final processed audio files.
    It also provides error handling and progress updates via an application's progress bar.
    """
    def __init__(self,lpid, epr,app):
        """
        This constructor calls the parent `GenericWorkFlow`'s constructor,
        setting up a folder and a finish message. It then immediately initiates the Audacity
        integration process by calling its own `user_workflow` method,
        passing the application instance for UI and progress updates.
        """
        super().__init__(folder = FIXED_AUDIO_FOLDER, finish_message = 'Audacity Send',lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self, app):
        """
        Executes the process of sending audio to Audacity, handling user interaction,
        and processing exported results.
        
        The workflow performs the following steps:
        1. **Pipe Creation:** Attempts to create a pipe connection to Audacity. If it fails
           (e.g., Audacity is not open or mod-pipe is not enabled), it displays an error
           message and re-enables the start button.
        2. **User Confirmation:** Prompts the user to confirm if they want to send data to Audacity.
        3. **Audio Import (if confirmed):**
           - Iterates through each episode in the defined range.
           - Retrieves the path to the previously fixed microphone audio track (`audio_mic_edit1_path`).
           - Sends an "Import2" command to Audacity to import the audio file.
           - Handles errors if Audacity is not reachable during import.
           - Updates the application's progress bar.
           - **Note:** The Noise Reduction step is explicitly mentioned as not automated
             and requires manual intervention in Audacity.
        4. **Import Completion Toast:** Displays a "Finished Importing" toast message.
        5. **Exported Results Handling:**
           - Prompts the user to select a directory where Audacity's exported files are located.
           - Validates if the number of exported files matches the number of episodes. If not,
             it displays an error.
           - Iterates through the exported files:
             - Extracts the episode number from the filename.
             - Converts the exported audio file to AAC format using `ffmpeg_run`
               (`FFMPEG_CONVERT_AUDIO_TYPE` is assumed external).
             - Updates the episode's metadata with the path to the newly converted AAC file
               as `audio_mic_edit2_path`.
             - Saves the updated episode metadata.
        6. **Finalization:** Re-enables the application's start button and calls the
           parent `user_workflow` to display the overall completion message.
        """
        try:
            create_pipe()
        except:
            msgbox.showerror('ERROR','Did you open Audacity & enabled the mod-pipe?')
            app.start_btn.state(['!disabled'])
            return
        ui = msgbox.askyesno('LPRT to AC','Do you want to send data to Audacity?')
        
        if ui:
            
            for i in range(*self.rng): 
                filepath = self.episode.get_audio_mic_edit1_path(i)
                if do_command(f'Import2: filename="{filepath}"') is None:
                    msgbox.showerror('ERROR','Audacity is not reachable!')
                    app.start_btn.state(['!disabled'])
                    return
                app.pb.step((1 / (self.rng[1] + 1))*100)
                #! The Noise Reduction is not automated
                # do_command from the audacity pipeline
        toast_finished('Finished Importing')
        results_path = askdirectory() + '/'
        files = listdir(results_path)
        if self.episode.row != len(files):
            msgbox.showerror('ERROR','Did you miss some episodes?')
            app.start_btn.state(['!disabled'])
            return
        for file in files:
            ep = int(file.split('_-')[1].split('.')[0]) - 1
            old = results_path + file
            new = old.split('.')[0] + '.aac'
            ffmpeg_run(FFMPEG_CONVERT_AUDIO_TYPE,{'__IN__': old, '__OUT__': new})
            #remove()
            self.episode.set_audio_mic_edit2_path(ep, new)
            self.episode.save()
        app.start_btn.state(['!disabled'])
        super().user_workflow()

class CompareAndRenderWF(GenericWorkFlow):
    """
    A workflow class responsible for allowing the user to compare and adjust audio
    levels for episodes, then combining these adjusted audio tracks with
    their respective video files to produce final rendered videos.
    
    This class extends `GenericWorkFlow` and orchestrates the following:
    1. Interactive audio volume adjustment using an `AudioPlayer` GUI.
    2. Combining microphone and desktop audio tracks based on user-adjusted volumes.
    3. Rendering the combined audio with the original video to create final video files.
    4. Updating episode metadata with the paths to the final rendered videos.
    It provides progress updates via an application's progress bar.
    """
    def __init__(self,lpid, epr,app):
        """
        This constructor calls the parent `GenericWorkFlow`'s constructor,
        setting up a temporary folder (`TEMP_FOLDER`) for intermediate files
        and a finish message.
        It then immediately initiates the comparison and rendering process by
        calling its own `user_workflow` method, passing the application instance
        for UI and progress updates.
        """
        super().__init__(folder=TEMP_FOLDER, finish_message="CAAR",lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        """
        Executes the main logic for audio comparison, combination, and video rendering.

        The workflow performs the following steps:
        1.  **Audio Player Initialization:**
            -   Prepares a list of audio and video paths for the `AudioPlayer`.
            -   Launches an `AudioPlayer` instance, allowing the user to interactively
                adjust the volume levels for each episode's desktop audio track relative
                to the microphone track.
            -   Pauses execution until the `AudioPlayer` window is closed by the user.
            -   Retrieves the user-adjusted volume settings from the `AudioPlayer`.
        2.  **Audio Combination:**
            -   Initializes an empty `rendering_queue`.
            -   Iterates through the results obtained from the `AudioPlayer` (episode index,
                microphone path, desktop path, video path, adjusted desktop volume).
            -   For each episode, it combines the microphone and desktop audio tracks
                using `ffmpeg_run` and `FFMPEG_AUDIO_COMBINE`,
                applying the user-adjusted desktop volume.
            -   Saves the combined audio to a temporary MP3 file.
            -   Adds the video path, temporary combined audio path, and episode index
                to the `rendering_queue`.
            -   Displays a toast message indicating audio combination is complete.
        3.  **Video Rendering:**
            -   Constructs a dynamic path ending for the final video files, incorporating
                the game name from the "LetsPlay" ID.
            -   Ensures the `VIDEO_FOLDER` exists (`cnef` to create/ensure folder).
            -   Iterates through the `rendering_queue`.
            -   For each item, it defines the `final_path` for the rendered video.
            -   Uses `ffmpeg_run` and `FFMPEG_VIDEO_RENDER`
                to combine the original video with the newly combined audio track.
            -   Updates the application's progress bar.
            -   Sets the path to the final rendered video in the episode's metadata.
            -   Saves the updated episode metadata.
        4.  **Finalization:** Calls the parent `user_workflow` to display the overall
            completion message.
        """
        rendering_queue = []

        paths = [[i, self.episode.get_audio_mic_edit1_path(i), self.episode.get_audio_desktop_path(i), self.episode.get_video_path(i),1.0] for i in range(*self.rng)]

        volap = AudioPlayer(paths)
        while not volap.isfinished:
            pass
        result = volap.audio_list
        
        for i, mic, desk, vid, vol in result:
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'

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
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'

            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_final_video_path(index,final_path)
            self.episode.save()
        super().user_workflow()