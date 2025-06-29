from os.path import isfile
def file_write(filepath : str, data : str):
    with open(filepath, 'w') as f:
        f.write(data)
def file_read(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()
class DavinciReceiver:
    def __init__(self):
        self.davinci_pipe = 'E:\\davinciResolve\\dvp.txt'
        self.user_pipe = 'E:\\davinciResolve\\up.txt'
        print('started Davinci Receiver')
            
    def send_to_user(self,msg):
        """
        From davinci to user
        """
        try:
            if not isfile(self.user_pipe):
                file_write(self.user_pipe,'')
            file_write(self.user_pipe,msg)
        except PermissionError as E:
            print(E)
    def recv_from_davinci(self):
        """
        Davinci result
        """
        try:
            if not isfile(self.user_pipe):
                file_write(self.davinci_pipe,'')
            return file_read(self.davinci_pipe)
        except PermissionError as E:
            print(E)
    def clean(self,typ: bool):
        file_write(self.davinci_pipe if typ else self.user_pipe,'')
    
    def check_commands(self):
        msg = self.recv_from_davinci()
        if msg.startswith('handshake'):
            print('handshake')
            self.send_to_user('handshake')
            self.clean(1)
        if msg.startswith('import'):
            if '<' in msg:
                video,audio,epNum = msg.split('<')[1],msg.split('<')[2],msg.split('<')[3]
                
                add_media([video,audio])
                vid = get_elements([video.split('\\')[-1]])
                #audio.split('\\')[-1]
                create_new_episode(int(epNum),vid)
                delete_tracks()
                aud = get_elements([audio.split('\\')[-1]])            
                timeline_append(aud)
                to_page(5)
                print('import',int(epNum))
            
            self.clean()
        if msg.startswith('reset'):
            print('reset')
            self.clean()
        if msg.startswith('delete'):
            delete_tracks()
            print('delete')
            self.clean()
        if ':' in msg:
            msg.split()
DR = DavinciReceiver()

PROJECT = resolve.GetProjectManager().GetCurrentProject()
ROOT = PROJECT.GetMediaPool().GetRootFolder()

def get_elements(search_for=list):
    _ret = []
    for item in search_for:
        for clip in ROOT.GetClipList():
            if clip.GetName() == item.split('\\')[-1]:
                _ret.append(clip)
    return _ret

def timeline_append(project, media):
    project.GetMediaPool().CreateTimelineFromClips('test', media)
    
def add_media(media):
    resolve.GetMediaStorage().AddItemListToMediaPool(media) 

def to_page(id: int):
    resolve.OpenPage({0:'media',1:'cut',2:'edit',3:'fusion',4:'color',5:'fairlight',6:'deliver'}[id])

def delete_tracks():
    resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',1)
    resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',2)
    resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().AddTrack('audio','stereo')
    
def create_new_episode(episode_number: int, clips_by_name: list[str]):
    resolve.GetMediaStorage().CreateTimelineFromClips(str(episode_number), [clips_by_name])
    
def get_element_names(self,search_for:str='mp4'):
        #Shows all Files in ClipList
        return {idx: clip.GetName() for idx,clip in enumerate(self.root_folder.GetClipList()) if clip.GetName().endswith(f'.{search_for}')}
while 1:
    DR.check_commands()