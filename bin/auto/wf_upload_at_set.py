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
from datetime import datetime as dt, timedelta as td



class UploadAtSetWF(GenericWorkFlow):
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
        
        """
        Pseudo Code:
        - Get start date
        - for each video increase `start_date + 1`
        
        """
        comb = f'{app.date.get_date()} {app.hour.get()}:{app.minutes.get()}'
        current_date: str = dt.strptime(comb,'%m/%d/%y %H:%M')

        
        print(current_date)
        
        try:
            rng = range(*self.rng)
            
            pbm = app.pbm
            pbm : ProgressBarManager
            pbm.clean(len(rng)*2)
            
            for idx, i in enumerate(rng):
                current_date += td(days=1)
                print(idx, i, current_date)
                #SQLAccess.update_upload_at(i,)
            
            super().user_workflow()
        except AutomationError as AE:
            xerr(f'Automation Error \n{AE}')
        
        pbm.reset_task()
          
        # After processing all episodes, we re-enabling the application's start button
        # and calling the parent `user_workflow` to display the completion message.
        # It does not matter whether the automation was completed or canceled.
        for i in app.lpep_picker.get_ui():
            i.state(['!disabled'])
