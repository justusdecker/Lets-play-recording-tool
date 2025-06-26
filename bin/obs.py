import obsws_python as obsws
from websocket import _exceptions
from bin.data_access import json_read
class OBSObserver:
    def __init__(self):
        self.settings = json_read('settings.json')
    @property
    def isconnected(self) -> bool:
        if hasattr(self,'client'):
            self.client.get_stats()
            return True
        return False
    def connect(self):
        try:
            self.client = obsws.ReqClient(host=self.settings['ip'], port=self.settings['port'], password=self.settings['pw'],timeout=self.settings['timeout'])
            
        except WindowsError as E:
            print('WindowsError')
        except _exceptions.WebSocketTimeoutException as E:
            print('WebsocketTimeout')