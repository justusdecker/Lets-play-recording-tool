from bin.auto.workflow import GenericWorkFlow
from bin.data_access import SQLAccess, reoc, isfile, rie, cnef
from bin.constants import ERROR_007, ERROR_013, ERROR_014, AutomationError, FIXED_AUDIO_FOLDER
from bin.ffmpeg import ffmpeg_run, FFMPEG_AUDIO_PF_LN_L

import tkinter.messagebox as msgbox
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
