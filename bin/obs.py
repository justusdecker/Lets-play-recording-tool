__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.3.106"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Production"
try: #Fix for issue: #124
    import obsws_python as obsws
    from websocket import _exceptions
except:
    from tkinter.messagebox import showerror
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nobs_ws')
    quit()

from bin.data_access import json_read
from bin.constants import OBS_SETTINGS_PATH
from os.path import isfile

from bin.data_access import SQLAccess

OUTPUT_TYPE = 'adv_file_output'
class OBSObserver:
    """
    A wrapper for the obs_ws API
    """
    def __init__(self):
        self.failed = False
        if not isfile(OBS_SETTINGS_PATH):
            self.failed = True
            return
        
        self.settings = json_read(OBS_SETTINGS_PATH) #! UNSAFE: Check exist if not return error
        self.connect()
        self.recording_flag = False #used for one_time operations like on_start
    def update(self,id):
        """
        Call this method to check on_start & on_stop events
        """
        self.connect() # Reconnect
        if self.isrecording and not self.recording_flag: # Recording started
            self.recording_flag = True
            SQLAccess.create_episode(id, self.filepath)

        elif not self.isrecording and self.recording_flag: # Recording stopped
            self.recording_flag = False
    def connect(self):
        """
        connects to the API
        
        Needs the `settings.json`
        """
        if self.isconnected:
           return 
        try:
            self.client = obsws.ReqClient(host=self.settings['ip'], port=self.settings['port'], password=self.settings['pw'],timeout=self.settings['timeout'])
        except WindowsError as E:
            print('WindowsError')
        except _exceptions.WebSocketTimeoutException as E:
            print('WebsocketTimeout')
        except ValueError:
            print('Hostname invalid!')
    @property
    def isconnected(self) -> bool:
        """
        Get the connection state
        """
        if hasattr(self,'client'):
            try:
                self.client.get_stats()
                return True
            except:
                return False
        return False
    @property
    def isrecording(self) -> bool:
        """
        Get the recording state
        """
        return self.timecode != '00:00:00.000'
    @property
    def filepath(self) -> str:
        """
        Gets the current filepath from the obs_ws API
        """
        return str(self.client.get_output_settings(OUTPUT_TYPE).output_settings['path'])
    @property
    def time_in_seconds(self) -> int:
        """
        Get the recording time in seconds
        """
        hms, _ = self.timecode.split('.')
        h,m,s = hms.split(':')
        h, m = int(h) * 3600, int(m) * 60 
        return h + m + int(s)
    @property
    def timecode(self) -> str:
        """Get The Current Time In String Form"""
        return str(self.client.get_output_status(OUTPUT_TYPE).output_timecode) if self.isconnected else '00:00:00.000'
    
    