__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.80"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"
from os.path import isfile
from bin.obs import OBSObserver

from bin.wintoasty import toast_finished

from bin.ffmpeg import *
from bin.audacity_pipeline import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msgbox

from os import listdir
from bin.constants import *

from tkinter import Toplevel
from tkinter.ttk import Label

from bin.thumbnail import ThumbnailGenerator
from tkinter.messagebox import showerror

from bin.player_video import VideoPlayer
from bin.player_audio import AudioPlayer
from bin.player_thumbnail import ThumbnailPreview

try: #Fix for issue: #127
    from PIL import ImageTk, Image
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nPIL')
    quit()

from bin.data_access import SQLAccess, cnef

from bin.constants import ERROR_007
   
def obs_connect(el):
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
            id = SQLAccess.get_lp_names().index(el.lp_option_var.get())
            if OBSO.time_in_seconds:
                el.recording_information_label.configure(text= f'Recording - {SQLAccess.get_episode_ammount(id)} Episodes\n{OBSO.timecode}')
            else:
                el.recording_information_label.configure(text= f'Waiting - {SQLAccess.get_episode_ammount(id)} Episodes')
            OBSO.update(id)
        except Exception as E:
            el.btn_connect.configure(text= 'Unexpected Error happened')
            print(f'Unexpected Error happened [{E}]')

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
        self.lpid,self.epr = lpid,epr
        self.lp_name = SQLAccess.get_lp_name(self.lpid)

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
        
    def user_workflow(self, app):
        TG = ThumbnailGenerator()
        TP = ThumbnailPreview()
        tad = SQLAccess.get_tad_path(self.lpid)
        print(tad)
        if not tad:
            showerror('ERROR' ,ERROR_009)
            app.start_btn.state(['!disabled'])
            return
        if not isfile(TAD_FOLDER + tad):
            showerror('ERROR' ,ERROR_007 + '\nTAD Path does not exist!')
            app.start_btn.state(['!disabled'])
            return
        check_all = msgbox.askyesno('LPRT Thumbnail Check','Do you want to check every image?')
        episodes = SQLAccess.read_episodes(self.lpid)
        for i in range(*self.rng): 
            video_path = episodes[i].video_path
            p = f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
            ok = False
            while not ok:
                TG.generate(
                            str(i+1),
                            video_path,
                            tad,
                            p
                            )
                TP.update_image(p,i)
                if check_all:
                    ok = msgbox.askyesno('LPRT Result Check','Thumbnail Result Okay?')
                else:
                    ok = True
            SQLAccess.update_episodes(self.lpid, i,thumbnail_path=p)
        app.start_btn.state(['!disabled'])
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
        episodes = SQLAccess.read_episodes(self.lpid)
        for i in range(*self.rng): 
            video_path = episodes[i].video_path
                       
            t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic.aac',f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop.aac'
            
            ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':t1_path, '__OUT2__':t2_path})
            
            app.pb.step((1 / (self.rng[1] + 1))*100)
            SQLAccess.update_episodes(self.lpid,i, audio_mic_path=t1_path, audio_desktop_path=t2_path)

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
        episodes = SQLAccess.read_episodes(self.lpid)
        for i in range(*self.rng): 
            audio_mic_path = episodes[i].audio_mic_path
            # Filters
            # - Lowpass
            # - Highpass
            # - Loudness Normalize
            # - Limiter
            dest = f'{FIXED_AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic_fixed.aac'
            
            cnef(TEMP_FOLDER)
            
            ffmpeg_run(FFMPEG_AUDIO_PF_LN_L,{'__IN__': audio_mic_path,'__OUT__':dest})
            app.pb.step((1 / (self.rng[1] + 1))*100)
            SQLAccess.update_episodes(self.lpid, i, audio_mic_path=dest)

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
        except Exception as E:
            print(E)
            msgbox.showerror('ERROR','Did you open Audacity & enabled the mod-pipe?')
            app.start_btn.state(['!disabled'])
            return
        ui = msgbox.askyesno('LPRT to AC','Do you want to send data to Audacity?')
        all_eps = len(range(*self.rng))
        if ui:
            episodes = SQLAccess.read_episodes(self.lpid)
            
            for i in range(*self.rng):
                filepath = episodes[i].audio_mic_path
                if do_command(f'Import2: filename="{filepath}"') is None:
                    msgbox.showerror('ERROR','Audacity is not reachable!')
                    app.start_btn.state(['!disabled'])
                    return
                app.pb.step((1 / (self.rng[1] + 1))*100)
                #! The Noise Reduction is not automated
                # do_command from the audacity pipeline
        print('test')
        break_pipe()
        toast_finished('Finished Importing')
        results_path = askdirectory() + '/'
        files = listdir(results_path)
        print(all_eps , len(files))
        if all_eps != len(files):
            msgbox.showerror('ERROR','Did you miss some episodes?')
            app.start_btn.state(['!disabled'])
            return
        for file in files:
            ep = int(file.split('_-')[1].split('.')[0]) - 1
            old = results_path + file
            new = old.split('.')[0] + '.aac'
            ffmpeg_run(FFMPEG_CONVERT_AUDIO_TYPE,{'__IN__': old, '__OUT__': new})
            #remove()
            SQLAccess.update_episodes(self.lpid,ep,audio_mic_edit2_path=new)
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
        episodes = SQLAccess.read_episodes(self.lpid)
        from bin.data_access import Episodes
        episodes : list[Episodes]
        paths = [[i, episodes[i].audio_mic_edit2_path, episodes[i].audio_desktop_path, episodes[i].video_path,1.0] for i in range(*self.rng)]

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

        path_ending = f'_{SQLAccess.get_lp_game_name(self.lpid)}_final.mp4'
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
            SQLAccess.update_episodes(self.lpid, index, final_video_path=final_path)
        super().user_workflow()
        


class TitleSetWF(GenericWorkFlow):

    def __init__(self,lpid, epr,app):
        
        super().__init__(folder = FIXED_AUDIO_FOLDER, finish_message = 'Title Set',lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self, app):

        app.start_btn.state(['disabled'])
        
        VideoPlayer([i + 1 for i in range(*self.rng)],self.lpid,app)

class DeployWF(GenericWorkFlow):

    def __init__(self,lpid, epr,app):

        super().__init__(folder=TEMP_FOLDER, finish_message="CAAR",lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        
        from shutil import copyfile
        from bin.jinja import deploy_render
        
        DEST = askdirectory()
        if not DEST:
            return
        
        print(self.rng)
        ALL = []
        episodes = SQLAccess.read_episodes(self.lpid)

        for i in range(*self.rng):
            old_thumbnail_path = episodes[i].thumbnail_path
            new_thumbnail_path = old_thumbnail_path.replace('/','\\').split('\\')[-1]
            
            old_video_path = episodes[i].final_video_path
            new_video_path = old_video_path.replace('/','\\').split('\\')[-1]
            
            description = SQLAccess.get_lp_description(self.lpid) #! This feature will be enhanced in 1.0
            print(new_thumbnail_path,new_video_path)
            try:
                copyfile(old_video_path,f'{DEST}\\{new_video_path}')
                copyfile(old_thumbnail_path,f'{DEST}\\{new_thumbnail_path}')
            except FileNotFoundError:
                msgbox.showerror('Something went wrong!','Data does not exist')
                return
            except Exception:
                msgbox.showerror('Something went wrong!','Unknown Error')
                return
            REP = {
                "id": i,
                "title": episodes[i].title,
                "thumbnail_path": new_thumbnail_path,
                "upload_at": ''
                }
            ALL.append(REP)
        deploy_render(f'{DEST}\\view.html', episodes=ALL,title=self.lp_name,description=description)
        copyfile('static\\style.css',f'{DEST}\\style.css')
        super().user_workflow()
