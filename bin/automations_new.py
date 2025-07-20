from bin.obs import OBSObserver
from bin.data_access import Episode

def obs_connect(ep: Episode,el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up or a keyboard interrupt happens
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
    def __init__(self, folder: str, finish_message: str):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.run()
    
    @property
    def rng(self) -> tuple[int,int]:
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
    def run(self,ep_range: list[int,int]):
        cnef(self.auto_create_folder_path)
        self.letsplay = LetsPlay(LP_PATH)
        self.ui_result = ep_range
        if self.ui_result is not None:
            self.lpid,self.epr = self.ui_result
            self.lp_name = self.letsplay.get_name(self.lpid)
            self.ep_path = self.letsplay.get_episode_path(self.lpid)
            self.episode = Episode(self.ep_path)
        
    def user_workflow(self):
        toast_finished(self.finish_message)