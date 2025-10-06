from bin.auto.workflow import GenericWorkFlow, enable_ui
from bin.data_access import SQLAccess, reoc, isfile, rie, cnef
from bin.constants import FIXED_AUDIO_FOLDER, ERROR_007, ERROR_013, AutomationError, AC_RESULT_FOLDER
from bin.api.ffmpeg import ffmpeg_run, FFMPEG_CONVERT_AUDIO_TYPE
from tools.log import LOG, LOG_INFO
from bin.xmsgbox import xerr, xqu
from bin.api.audacity_pipeline import do_command, create_pipe, break_pipe
from bin.data_access import SQLAccess, cnef,rie, try_delete_file
from tools.log import LOG, LOG_ERROR
from os import listdir
from bin.wintoasty import toast_finished
from bin.ui.progress_bar_manager import ProgressBarManager

class SendToAudacityWF(GenericWorkFlow):
    """
    A workflow class designed to integrate with Audacity for further audio
    processing, specifically for importing fixed microphone audio tracks and
    then handling the exported results.
    """
    def __init__(self,lpid, epr,app):
        super().__init__(folder = FIXED_AUDIO_FOLDER, finish_message = 'Audacity Send',lpid=lpid, epr=epr)
        LOG("LP: $ EPS: $",[lpid, self.rng])
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
            LOG(f"",[str(E)],logtype=LOG_ERROR)
            xerr('Did you open Audacity & enabled the mod-pipe?')
            
            for i in app.lpep_picker.get_ui():
                i.state(['!disabled'])
            return
        
        try:
            files = listdir(AC_RESULT_FOLDER)
            if files and xqu('Clear Audacity Export Folder?'):
                for file in files:
                    try_delete_file(AC_RESULT_FOLDER+file)
                
            ui = xqu('Do you want to send data to Audacity?')
            rng = range(*self.rng)
            
            pbm = app.pbm
            pbm : ProgressBarManager
            pbm.clean(len(rng)*2)
            
            all_eps = len(rng)
            if ui:
                episodes = SQLAccess.read_episodes(self.lpid)
                
                for ci, i in enumerate(rng):
                    pbm.increment()
                    filepath = episodes[i].audio_mic_edit1_path
                    LOG("Try importing $ to Audacity", [filepath], LOG_INFO)
                    reoc(filepath is None,ERROR_013)
                    reoc(not isfile(filepath), ERROR_007)
                    reoc(do_command(f'Import2: filename="{filepath}"') is None,'Audacity is not reachable!')
                    app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')
            LOG("Finished Importing", logtype=LOG_INFO)
            toast_finished('Finished Importing')
            #! See issue #303

            
            
            while not xqu('Did you finished exporting the files?'):
                pass
            files = listdir(AC_RESULT_FOLDER)
            reoc(all_eps < len(files),'Do you forget to clear the output folder?')
            reoc(all_eps > len(files),'Did you miss some episodes?')
            rng_list = list(rng)
            cnef(AC_RESULT_FOLDER)
            
            
            for file in files:
                pbm.increment()
                reoc(not file.endswith('.ac3'),'Wrong file format!')
                reoc('_-' not in file,'Wrong filename format!')
                reoc(not file.split('_-')[1].split('.')[0].isdecimal(),'Numbering is not correct!')
                
                ep = int(file.split('_-')[1].split('.')[0]) - 1
                LOG("Convert ep $ to .aac",[rng_list[ep]+1],LOG_INFO)
                old = AC_RESULT_FOLDER + file
                new = FIXED_AUDIO_FOLDER+f'{rng_list[ep]+1}_track_mic_fixed_ac.aac'
                rie(new)
                ffmpeg_run(FFMPEG_CONVERT_AUDIO_TYPE,{'__IN__': old, '__OUT__': new})
                reoc(not isfile(new),ERROR_007)
                #remove()
                SQLAccess.update_episode(self.lpid,rng_list[ep],audio_mic_edit2_path=new)
            for i in app.lpep_picker.get_ui():
                i.state(['!disabled'])
            super().user_workflow()
        except AutomationError as AE:
            LOG("AutomationError $ ", [str(AE)],LOG_ERROR)
            xerr(f'Automation Error\n{AE}')
        
        pbm.reset_task()  
        
        enable_ui(app)
        try:
            break_pipe()
        except Exception as E:
            pass
            