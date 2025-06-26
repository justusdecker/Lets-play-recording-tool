import obsws_python as obsws
from websocket import _exceptions
from bin.data_access import json_read

OUTPUT_TYPE = 'adv_file_output'
class OBSObserver:
    def __init__(self):
        self.settings = json_read('settings.json')
        self.connect()
    @property
    def isconnected(self) -> bool:
        if hasattr(self,'client'):
            try:
                self.client.get_stats()
                return True
            except:
                return False
        return False
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
    def timecode(self) -> int:
        """Get The Current Time In String Form"""
        return str(self.client.get_output_status(OUTPUT_TYPE).output_timecode)