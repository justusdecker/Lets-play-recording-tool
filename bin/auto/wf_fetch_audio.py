from bin.auto.workflow import GenericWorkFlow
from bin.data_access import SQLAccess, reoc, isfile, rie, cnef
from bin.constants import AUDIO_FOLDER, ERROR_007, ERROR_013, ERROR_014, AutomationError
from bin.api.ffmpeg import FFMPEG_OPTIMIZED_EXTRACT, FFMPEG_GET_STREAM_AMMOUNT, ffmpeg_run
from tools.log import LOG, LOG_INFO
from bin.xmsgbox import xerr
from bin.ui.progress_bar_manager import ProgressBarManager
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
            
            pbm = app.pbm
            pbm : ProgressBarManager
            pbm.clean(len(rng))
            
            for ci,i in enumerate(rng):
                pbm.increment()
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
                
                LOG(f'"Audiostreams: $"',[ffmpeg_stream_ammount],logtype=LOG_INFO)
                
                
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
            xerr(f'Automation Error\n{AE}')
            
        pbm.reset_task()
        
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])
