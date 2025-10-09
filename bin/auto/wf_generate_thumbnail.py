from bin.auto.workflow import OverhauledWorkFlow, enable_ui
from bin.constants import THUMBNAIL_FOLDER, TAD_FOLDER, ERROR_007, ERROR_009, ERROR_013, AutomationError
from bin.data_access import SQLAccess, reoc, isfile, rie   
from bin.xmsgbox import xerr, xqu
from bin.thumbnail import ThumbnailGenerator
from bin.ui.progress_bar_manager import ProgressBarManager
from tkinter.filedialog import askdirectory
from os import listdir
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
        rng = range(*self.rng)
        pbm = app.pbm
        pbm : ProgressBarManager
        pbm.clean(len(rng))
        try:
            TG = ThumbnailGenerator()
            
            TP = app.tp #+ This will be the thumbnail preview
            
            if app.import_var.get():
                directory = askdirectory()
                if not directory:
                    raise AutomationError('Directory not set')
                thumbnails = [p for p in listdir(directory) if p.endswith('.png')]
                if len(thumbnails) != len(rng):
                    raise AutomationError('Not Equal')
            
            else:
                tad = SQLAccess.read_tad_path(self.lpid)
            
                reoc(not tad, ERROR_009)
                reoc(not isfile(TAD_FOLDER + tad),ERROR_007 + '\nTAD Path does not exist!')
            
            
            
            episodes = SQLAccess.read_episodes(self.lpid)
            
            
            
            
            for ci,i in enumerate(rng): 
                pbm.increment()
                if app.import_var.get():
                    print(thumbnails[i])
                    p = f'{directory}/{ci+1}.png'
                    TP.update_image(p,i)
                    SQLAccess.update_episode(self.lpid, i,thumbnail_path=p)
                else:
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
                        if app.check_for_each_option_var.get():
                            ok = xqu('Thumbnail Result Okay?')
                        else:
                            ok = True
                    #!app.progress_label.configure(text = f'{((ci+1)/len(rng))*100:.1f}%\n{ci+1}/{len(rng)}')

                    SQLAccess.update_episode(self.lpid, i,thumbnail_path=p)

            super().user_workflow()
        except AutomationError as AE:
            xerr(f'Automation Error\n{AE}')
        
        pbm.reset_task()
        
        enable_ui(app)
