
import tkinter.ttk as ttk
from bin.ui.progress_bar_manager import ProgressBarManager
from bin.ui.lpep_picker import LPEPPicker
class UI:
    def __init__(self, parent, elements: list):
        self.menu = parent.master
        self.thread = None
        self.automation_callback = None
        
        self.progress_label = ttk.Label(self,)
        self.progress_label.grid(sticky='SE',row = 0, column = 2)
        
        W = ttk.Frame(parent)
        
        AUTOMATION_ROOT = ttk.Frame(W)

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.lpep_picker = LPEPPicker(AUTOMATION_ROOT,self.run,'lp-ep')
        
        self.pbm = ProgressBarManager(AUTOMATION_ROOT)

        AUTOMATION_ROOT.pack()
        
        W.pack()
        
        for element in elements:
            name = element['name']
            id = element['id']
            master = element.get('master',None)
            if master == 'root':
                master = W
            else:
                master = getattr(self,master[1:])
            
            if 'pack' in element:
                put_mode = 'pack'
                fill = element['pack'].get('fill',None)
                padx = element['pack'].get('padx',None)
                pady = element['pack'].get('pady',None)
                
            elif 'grid' in element: #! Not used currently
                put_options = element['grid'] 
                put_mode = 'grid'
            
            print(element['name'])
            setattr(self, element['id'])