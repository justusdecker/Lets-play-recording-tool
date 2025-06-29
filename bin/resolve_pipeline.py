""""""
from os.path import isfile
from bin.data_access import file_read, file_write



class DaviniciSender:
    """
    Send Davinci Resolve one of the following instructions:
    
    <$CIMPORT> {filePath} - creates an TimeLine with given Element
    <$IMPORT> {filePath} - Load Element in existing TimeLine
    
    <$DELETETRACK> {id} - Deletes an AudioTrack with given id
    """
    def __init__(self,user=True):
        self.davinci_pipe = 'E:\\davinciResolve\\dvp.txt'
        self.user_pipe = 'E:\\davinciResolve\\up.txt'
        self.eol = '\r\n\0'
        if not user:
            
            self.project = resolve.GetProjectManager().GetCurrentProject()
            self.root_folder = self.project.GetMediaPool().GetRootFolder()
            resolve.OpenPage('edit')
        else:
            resolve = ''
    def send_to_davinci(self,command):
        """
        From user to davinci
        """
        try:
            if not isfile(self.davinci_pipe):
                file_write(self.davinci_pipe,'')
            file_write(self.davinci_pipe,command)
        except PermissionError as E:
            print(E)
            
    def send_to_user(self,msg):
        """
        From davinci to user
        """
        try:
            if not isfile(self.davinci_pipe):
                file_write(self.davinci_pipe,'')
            file_write(self.davinci_pipe,msg)
        except PermissionError as E:
            print(E)
            
    def recv_from_user(self):
        """
        Davinci result
        """
        try:
            if not isfile(self.user_pipe):
                file_write(self.user_pipe,'')
            return file_read(self.user_pipe)
        except PermissionError as E:
            print(E)
    
    def clean(self,typ: bool):
        file_write(self.davinci_pipe if typ else self.user_pipe,'')
        
    def check_commands(self,msg:str):
        if msg.startswith('import'):
            if '<' in msg:
                media = loads(msg.split('<')[1])
                #DVRSF.addMedia(media)
                #DVRSF.getElements(media)
                print('import')
            
            self.clean()
        if msg.startswith('reset'):
            print('reset')
            self.clean()
        if msg.startswith('addRender'):
            #DVRSF.addRenderJob()
            self.clean()
        if msg.startswith('render'):
            #DVRSF.render()
            print('render')
            self.clean()
        if ':' in msg:
            msg.split()
    
    def get_element_names(self,search_for:str='mp4'):
        #Shows all Files in ClipList
        {}
        return {idx: clip.GetName() for idx,clip in enumerate(self.root_folder.GetClipList()) if clip.GetName().endswith(f'.{search_for}')}

    def timeline_append(self,media):
        self.project.GetMediaPool().CreateTimelineFromClips('test', media)
        
    def create_new_episode(self,episode_number: int, clips_by_name: list[str]):
        resolve.GetMediaStorage().CreateTimelineFromClips(str(episode_number), [clips_by_name])
       
    def add_media(self,media):
        resolve.GetMediaStorage().AddItemListToMediaPool(media) 

    def delete_tracks(self):
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',1)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',2)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().AddTrack('audio','stereo')

    def getElements(self,searchFor=list):
        _ret = []
        for item in searchFor:
            for clip in self.rootFolder.GetClipList():
                if clip.GetName() == item.split('\\')[-1]:
                    _ret.append(clip)
        return _ret