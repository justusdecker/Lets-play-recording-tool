import obsws_python as obsws
from websocket import _exceptions
from bin.data_access import json_read

OUTPUT_TYPE = 'adv_file_output'
class OBSObserver:
    def __init__(self):
        self.settings = json_read('settings.json')
        self.connect()
        self.recording_flag = False #used for one_time operations like on_start
    
    def update(self,ep):
        self.connect() # Reconnect
        if self.isrecording and not self.recording_flag: # Recording started
            self.recording_flag = True
            ep.add(video_path=self.filepath)
            ep.save()
        elif not self.isrecording and self.recording_flag: # Recording stopped
            self.recording_flag = False
    def connect(self):
        if self.isconnected:
           return 
        try:
            self.client = obsws.ReqClient(host=self.settings['ip'], port=self.settings['port'], password=self.settings['pw'],timeout=self.settings['timeout'])
        except WindowsError as E:
            print('WindowsError')
        except _exceptions.WebSocketTimeoutException as E:
            print('WebsocketTimeout')
    
    @property
    def isconnected(self) -> bool:
        if hasattr(self,'client'):
            try:
                self.client.get_stats()
                return True
            except:
                return False
        return False
    @property
    def isrecording(self) -> bool:
        return self.timecode != '00:00:00.000'
    
    @property
    def filepath(self) -> str:
        return str(self.client.get_output_settings(OUTPUT_TYPE).output_settings['path'])
    
    @property
    def time_in_seconds(self) -> int:
        hms, _ = self.timecode.split('.')
        h,m,s = hms.split(':')
        h, m = int(h) * 3600, int(m) * 60 
        return h + m + int(s)
    
    @property
    def timecode(self) -> str:
        """Get The Current Time In String Form"""
        return str(self.client.get_output_status(OUTPUT_TYPE).output_timecode) if self.isconnected else '00:00:00.000'
    
    