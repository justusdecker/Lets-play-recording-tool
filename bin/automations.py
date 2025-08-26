from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from os.path import isfile
from bin.obs import OBSObserver
from bin.wintoasty import toast_finished
from bin.ffmpeg import *
from bin.audacity_pipeline import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msgbox
from os import listdir
from bin.constants import *
from bin.thumbnail import ThumbnailGenerator
from tkinter.messagebox import showerror

from bin.player_thumbnail import ThumbnailPreview
from shutil import copyfile
from bin.data_access import SQLAccess, cnef,rie, file_write, try_delete_file
from time import sleep
from subprocess import Popen

try:
    from bin.jinja import deploy_render
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nJinja')
    quit()
   
def obs_rec_label_set(OBSO, el,reset:bool = False):
    """
    Sets the recording label color
    """
    if reset:
        el.recording_information_label.configure(foreground='black')
        return
    epl = SQLAccess.read_episode_length(SQLAccess.read_letsplay_names().index(el.lpep_picker.v_lp.get()))
    
    if epl is None:
        el.recording_information_label.configure(foreground='black')
        return
    
    if OBSO.time_in_seconds >= epl:
        el.recording_information_label.configure(foreground='red')
        return
    elif OBSO.time_in_seconds + 30 >= epl:
        el.recording_information_label.configure(foreground='orange')
        return
    else:
        el.recording_information_label.configure(foreground='green')

def obs_connect(el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up. See issue #244
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        obs_rec_label_set(OBSO,el, True)
        el.btn_connect.configure(text= 'Settings File does not exist!')
        return
    if not OBSO.isconnected:
        obs_rec_label_set(OBSO,el, True)
        el.btn_connect.configure(text= 'No Connection!')
        return
    el.btn_connect.configure(text= 'Disconnect')
    el.btn_connect.state(["!disabled"])
    while OBSO.isconnected:
        if el.close_connection:
            OBSO.client.disconnect()
            el.btn_connect.configure(text= 'Connection closed!')
            return
        try:
            id = SQLAccess.read_letsplay_names().index(el.lpep_picker.v_lp.get())
            if OBSO.time_in_seconds:
                el.recording_information_label.configure(text= f'Recording - {SQLAccess.read_episode_ammount(id)} Episodes\n{OBSO.timecode.split(".")[0]}')
                obs_rec_label_set(OBSO,el)
            else:
                obs_rec_label_set(OBSO,el, True)
                el.recording_information_label.configure(text= f'Waiting - {SQLAccess.read_episode_ammount(id)} Episodes')
            OBSO.update(id)
        except Exception as E:
            obs_rec_label_set(OBSO,el, True)
            el.btn_connect.configure(text= 'Unexpected Error happened')
            print(f'Unexpected Error happened [{E}]')
        sleep(0.3)

class GenericWorkFlow:
    """
    This class serves as a base for workflows, 
    ---
    Inheriting from this class will provide you:
    .. rng:: This gives you the effective episode range as a tuple (start, end).
    .. user_workflow:: shows a toast notification
    .. auto_create_folder_path:: You can create this folder with the `cnef` function.
    .. lpid:: Lets Play Index
    .. finished_message:: The message that will be displayed in user_workflow.
    .. lp_name:: The Lets Play Name
    """
    def __init__(self, folder: str, finish_message: str,lpid,epr):

        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.lpid,self.epr = lpid,epr
        self.lp_name = SQLAccess.read_letsplay_name(self.lpid)

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

class OverhauledWorkFlow:
    def __init__(self, folder: str, finish_message: str,lpid,epr):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.lpid,self.epr = lpid,epr
        self.lp_name = SQLAccess.read_letsplay_name(self.lpid)
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
        
class GenerateThumbnailWF(OverhauledWorkFlow):
    """
    Generating Thumbnails based on the thumbnail automation data
    """
    def __init__(self,lpid,epr,app):
        super().__init__(folder = THUMBNAIL_FOLDER, finish_message = 'Thumbnail Generation',lpid=lpid,epr=epr)
        self.user_workflow(app)
        
    def user_workflow(self, app):
        """
        Generates Thumbnails based on the thumbnail automation data.
        
        If the user has done something wrong. A AutomationError will be thrown & catched. 
        After that the corresponding error message will be displayed.
        """
        try:
            TG = ThumbnailGenerator()
            
            TP = app.tp #+ This will be the thumbnail preview
            tad = SQLAccess.read_tad_path(self.lpid)
            
            reoc(not tad, ERROR_009)
            reoc(not isfile(TAD_FOLDER + tad),ERROR_007 + '\nTAD Path does not exist!')

            check_all = msgbox.askyesno('LPRT Thumbnail Check','Do you want to check every image?')
            episodes = SQLAccess.read_episodes(self.lpid)
            rng = range(*self.rng)
            for ci,i in enumerate(rng): 
                video_path = episodes[i].video_path
                reoc(video_path is None,ERROR_013)
                reoc(not isfile(video_path), ERROR_007)
                
                
                p = f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
                
                rie(p)
                
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
                #!app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')

                SQLAccess.update_episode(self.lpid, i,thumbnail_path=p)

            super().user_workflow()
        except AutomationError as AE:
            msgbox.showerror('Automation Error',str(AE))
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])

class ExtractAudioWF(GenericWorkFlow):
    """
    A workflow class designed to extract audio tracks from video files for a
    given "LetsPlay" episode range.
    """
    def __init__(self,lpid,epr,app):
        super().__init__(folder=AUDIO_FOLDER, finish_message='Audio extraction finished',lpid=lpid,epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        """
        Executes the audio extraction process for each episode within the
        defined range.
        
        If the user has done something wrong. A AutomationError will be thrown & catched. 
        After that the corresponding error message will be displayed.
        """
        try:
            cnef(AUDIO_FOLDER)
            episodes = SQLAccess.read_episodes(self.lpid)
            rng = range(*self.rng)
            for ci,i in enumerate(rng):
                
                video_path = episodes[i].video_path
                
                prefix = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_'
                ff = '.aac'
                mic_track_path = f'{prefix}mic{ff}'
                desktop_track_path = f'{prefix}desktop{ff}'
                ffmpeg_stream_ammount = ffmpeg_run(FFMPEG_GET_STREAM_AMMOUNT,{'__IN__':video_path},True).strip()
                reoc(not ffmpeg_stream_ammount.isdecimal(),'Something went wrong.\nThis error should not happen!\nFFPROBE HAS GIVEN BACK A NOT NUMERIC STRING')
                
                # We only do a soft edge case test here!
                # This is not very accurate. The user can use 2 video tracks or a subtitle track and the result can / will be correct.
                # In this case we dont need to worry about this case. 
                # The user has been warned to use 2 audio / 1 video track in the documentation.
                reoc(int(ffmpeg_stream_ammount) < 3,'Not enough tracks to execute this automation!')
                
                print(f'"{ffmpeg_stream_ammount}"')
                
                
                reoc(video_path is None, ERROR_013) # In case the database is corrupted or the video_file was not set!
                
                reoc(not isfile(video_path), ERROR_007) # In case the video_file is not existing
                
                rie(mic_track_path) # remove files to prevent false negative after ffmpeg_run
                rie(desktop_track_path)
                
                ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':mic_track_path, '__OUT2__':desktop_track_path}) # Uses `ffmpeg_run` to extract both audio tracks from the video.
                
                reoc(not isfile(mic_track_path) or not isfile(desktop_track_path), ERROR_014) # In case ffmpeg did not create the files
                
                app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')
                
                SQLAccess.update_episode(self.lpid,i, audio_mic_path=mic_track_path, audio_desktop_path=desktop_track_path) # Saves the updated episode metadata.
            super().user_workflow()
        except AutomationError as AE:
            msgbox.showerror('Automation Error',str(AE))
            
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])

class FixAudioWF(GenericWorkFlow):
    """
    A workflow class designed to apply various audio processing filters to
    microphone audio tracks extracted from "LetsPlay" videos.
    
    Filters: (Lowpass, Highpass, Loudness Normalize)
    
    If the user has done something wrong. A AutomationError will be thrown & catched. 
    After that the corresponding error message will be displayed.
    """
    def __init__(self,lpid, epr,app):
        super().__init__(FIXED_AUDIO_FOLDER, 'Audio Fix', lpid, epr)
        self.user_workflow(app)
        
    def user_workflow(self,app):
        """
        Executes the audio fixing process for each microphone audio track
        within the defined episode range.
        """
        
        try:
            cnef(FIXED_AUDIO_FOLDER)
            episodes = SQLAccess.read_episodes(self.lpid)
            rng = range(*self.rng)
            for ci, i in enumerate(rng): 
                audio_mic_path = episodes[i].audio_mic_path
                
                audio_mic_edit1_path = f'{FIXED_AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic_fixed.aac'
                
                reoc(audio_mic_path is None, ERROR_013) # In case the database is corrupted or the audio_mic_path was not set!
                
                reoc(not isfile(audio_mic_path), ERROR_007) # In case the audio_mic_path is not existing
                
                rie(audio_mic_edit1_path)
                
                ffmpeg_run(FFMPEG_AUDIO_PF_LN_L,{'__IN__': audio_mic_path,'__OUT__':audio_mic_edit1_path, '__FILTERS__': app.get_ffmpeg_audio_filter_string()})
                
                reoc(not isfile(audio_mic_edit1_path), ERROR_014) # In case ffmpeg did not create the file
                
                app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')
                SQLAccess.update_episode(self.lpid, i, audio_mic_edit1_path=audio_mic_edit1_path)
            
            super().user_workflow()
        except AutomationError as AE:
            msgbox.showerror('Automation Error',str(AE))
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])

class SendToAudacityWF(GenericWorkFlow):
    """
    A workflow class designed to integrate with Audacity for further audio
    processing, specifically for importing fixed microphone audio tracks and
    then handling the exported results.
    """
    def __init__(self,lpid, epr,app):
        super().__init__(folder = FIXED_AUDIO_FOLDER, finish_message = 'Audacity Send',lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self, app):
        """
        Executes the process of sending audio to Audacity, handling user interaction,
        and processing exported results.
        
        - Prompts the user to select a directory where Audacity's exported files are located.
        - Validates if the number of exported files matches the number of episodes. If not,
    
        If the user has done something wrong. A AutomationError will be thrown & catched. 
        After that the corresponding error message will be displayed.
        """
        
        
        try:
            create_pipe()
        except Exception as E:
            print(E)
            msgbox.showerror('ERROR','Did you open Audacity & enabled the mod-pipe?')
            app.start_btn.state(['!disabled'])
            return
        
        try:
            files = listdir(AC_RESULT_FOLDER)
            if files and msgbox.askyesno('Question','Clear Audacity Export Folder?'):
                for file in files:
                    try_delete_file(AC_RESULT_FOLDER+file)
                
            ui = msgbox.askyesno('LPRT to AC','Do you want to send data to Audacity?')
            rng = range(*self.rng)
            all_eps = len(rng)
            if ui:
                episodes = SQLAccess.read_episodes(self.lpid)
                
                for ci, i in enumerate(rng):
                    filepath = episodes[i].audio_mic_edit1_path
                    reoc(filepath is None,ERROR_013)
                    reoc(not isfile(filepath), ERROR_007)
                    reoc(do_command(f'Import2: filename="{filepath}"') is None,'Audacity is not reachable!')
                    app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')
            
            toast_finished('Finished Importing')
            #! See issue #303

            
            
            while not msgbox.askquestion(message='Did you finished exporting the files?'):
                pass
            files = listdir(AC_RESULT_FOLDER)
            reoc(all_eps < len(files),'Do you forget to clear the output folder?')
            reoc(all_eps > len(files),'Did you miss some episodes?')
            rng_list = list(rng)
            cnef(AC_RESULT_FOLDER)
            
            
            for file in files:
                
                reoc(not file.endswith('.ac3'),'Wrong file format!')
                reoc('_-' not in file,'Wrong filename format!')
                reoc(not file.split('_-')[1].split('.')[0].isdecimal(),'Numbering is not correct!')
                
                ep = int(file.split('_-')[1].split('.')[0]) - 1
                print(rng_list[ep])
                old = AC_RESULT_FOLDER + file
                new = FIXED_AUDIO_FOLDER+f'{rng_list[ep]}_track_mic_fixed_ac.aac'
                rie(new)
                ffmpeg_run(FFMPEG_CONVERT_AUDIO_TYPE,{'__IN__': old, '__OUT__': new})
                reoc(not isfile(new),ERROR_007)
                #remove()
                SQLAccess.update_episode(self.lpid,rng_list[ep],audio_mic_edit2_path=new)
            for i in app.lpep_picker.get_ui():
                i.state(['!disabled'])
            super().user_workflow()
        except AutomationError as AE:
            msgbox.showerror('Automation Error',str(AE))
            
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])
        try:
            break_pipe()
        except Exception as E:
            pass

def render(result,app, lpid):
    """
    Currently a workaround. Will be refactored into Compare&Render ASAP - issie #345
    """
    rendering_queue = []
    try:
        ci = 0
        for i, mic, desk, vid, vol in result:
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'
            
            rie(tmp_audio_path)
            
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
            
            reoc(not isfile(tmp_audio_path),ERROR_007)
            
            #app.progress_label.configure(text = f'Audio Combine\n{((ci+1)/len(result))*100:.1f}%\n{ci+1}/{len(result)}')
            ci += 1
            rendering_queue.append((vid, tmp_audio_path, i))
        toast_finished("[1/2] Audio combine")

        
        
        path_ending = f'_{SQLAccess.read_letsplay_game_name(lpid)}_final.mp4'
        cnef(VIDEO_FOLDER)
        ci = 0
        for video, audio, index in rendering_queue:
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'
            rie(final_path)
            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )
            reoc(not isfile(final_path),ERROR_007)
            #app.progress_label.configure(text = f'Audio Combine\n{((ci+1)/len(result))*100:.1f}%\n{ci+1}/{len(result)}')
            ci += 1
            SQLAccess.update_episode(lpid, index, final_video_path=final_path)
        toast_finished("[2/2] Audio combine")
    except AutomationError as AE:
        msgbox.showerror('Automation Error',str(AE))

class DeployWF(GenericWorkFlow):
    """
    Copies user generated data to user set destination...
    """

    def __init__(self,lpid, epr,app):
        super().__init__(folder=TEMP_FOLDER, finish_message="CAAR",lpid=lpid, epr=epr)
        self.user_workflow(app)
    
    def user_workflow(self,app):
        """
        Copies Video & Thumbnail to selected destination.
        
        Creates both `view.html` & `style.css` to make the upload process a lot easier.
        
        In the `view.html`, thumbnails & titles are embedded.
        
        If the user has done something wrong. A AutomationError will be thrown & catched. 
        After that the corresponding error message will be displayed.
        """
        try:
            data_deletion = msgbox.askyesno('Question','Do you want to delete temp files?')
            move_files = msgbox.askyesno('Question','Do you want to move the files to another path?')
            if move_files:
                DEST = askdirectory().replace('/','\\')
            else:
                DEST = f'{DEPLOY_FOLDER}{SQLAccess.read_letsplay_name(self.lpid)}\\'
                cnef(DEST)
            reoc(not DEST,ERROR_006)
            ALL = []
            episodes = SQLAccess.read_episodes(self.lpid)

            for i in range(*self.rng):
                
                
                old_thumbnail_path = episodes[i].thumbnail_path
                reoc(old_thumbnail_path is None,ERROR_013)
                reoc(not isfile(old_thumbnail_path),ERROR_007)

                new_thumbnail_path = old_thumbnail_path.replace('/','\\').split('\\')[-1]
                
                old_video_path = episodes[i].final_video_path
                
                reoc(old_video_path is None,ERROR_013)
                reoc(not isfile(old_video_path),ERROR_007)
                
                new_video_path = old_video_path.replace('/','\\').split('\\')[-1]
                
                description = SQLAccess.read_letsplay_description(self.lpid) #! This feature will be enhanced in 1.0

                copyfile(old_video_path,f'{DEST}\\{new_video_path}')
                copyfile(old_thumbnail_path,f'{DEST}\\{new_thumbnail_path}')

                REP = {
                    "id": i,
                    "title": episodes[i].title,
                    "thumbnail_path": new_thumbnail_path,
                    "upload_at": ''
                    }
                
                #! Delete Temps
                if data_deletion:
                    ep = episodes[i]
                    for file in [
                                    ep.thumbnail_path,
                                    ep.audio_mic_edit1_path,
                                    ep.audio_mic_edit2_path,
                                    ep.audio_desktop_path,
                                    ep.audio_mic_path,
                                    ep.final_video_path
                                ]:
                        try_delete_file(file)
                
                    
                ALL.append(REP)
            deploy_render(f'{DEST}\\view.html',episodes=ALL,title=self.lp_name,description=description)
            file_write(f'{DEST}\\style.css', DEPLOY_CSS)
            Popen(f'explorer {DEST}')
            super().user_workflow()
        except AutomationError as AE:
            msgbox.showerror('Automation Error',str(AE))
            
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])
