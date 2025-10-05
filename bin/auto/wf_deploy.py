from bin.auto.workflow import GenericWorkFlow
from bin.data_access import SQLAccess, reoc, isfile, rie, cnef
from bin.constants import TEMP_FOLDER, DEPLOY_FOLDER, ERROR_006, ERROR_007, ERROR_013, DEPLOY_CSS, AutomationError
from shutil import copyfile
from bin.jinja import deploy_render
from bin.xmsgbox import xqu, xerr
from subprocess import Popen
from bin.data_access import SQLAccess, cnef,file_write, try_delete_file
from tkinter.filedialog import askdirectory
from os import listdir,remove
from bin.ui.progress_bar_manager import ProgressBarManager

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
            if app.mfp_enabled:
                DEST = askdirectory().replace('/','\\')
            else:
                DEST = f'{DEPLOY_FOLDER}{SQLAccess.read_letsplay_name(self.lpid)}\\'
                cnef(DEST)
            reoc(not DEST,ERROR_006)
            ALL = []
            episodes = SQLAccess.read_episodes(self.lpid)
            already_there = listdir(DEST)
            if already_there:
                if app.cof_enabled.get(): 
                    print('COF')
                    for file in already_there:
                        try:
                            remove(f'{DEST}\\{file}')
                        except Exception as E:
                            print(E)
                            pass
            rng = range(*self.rng)
            
            pbm = app.pbm
            pbm : ProgressBarManager
            pbm.clean(len(rng)*2)
            
            for idx, i in enumerate(rng):
                pbm.increment()
                
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
                    "upload_at": episodes[i].upload_at
                    }
                
                #! Delete Temps
                if app.dtf_enabled.get():
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
            xerr(f'Automation Error \n{AE}')
        
        pbm.reset_task()
          
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])
