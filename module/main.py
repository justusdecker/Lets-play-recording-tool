from src.api.kivy_modules import BoxLayout, Button
from src.api.obsws import OBSWSClient
from threading import Thread
from time import sleep
from src.api.msgbox import msgbox, SoundFlags, MSGBoxPresets

class OBSView(BoxLayout):
    is_watching: bool = False
    thread = None
    ...
    def toggle_watching_state(self, *_): 
        if self.is_watching:
            self.is_watching = False
        self.__update_recording_information()
        
    def __update_recording_information(self, *_): 
        if self.thread is None and not self.is_watching:
            print('created_thread')
            self.is_watching = True
            self.thread = Thread(target=self.__uri)
            self.thread.start()
            
            
    def __uri(self, ): 
        obs_connection = OBSWSClient(password='KLj31bU8H2vrYQg6')
        if obs_connection.connect() is not None:
            self.ids.timer.text = 'Connected to OBS'
        
        while self.is_watching:
            result = obs_connection.call("GetOutputStatus",{"outputName": 'adv_file_output'})
            if 'error' in result:
                msgbox('error', result['error'], MSGBoxPresets.SYSTEM_ALERT, SoundFlags.ERROR)
                break
            try:
                
                self.ids.timer.text = result['d']['responseData']['outputTimecode']
            except Exception as E:
                ...
            sleep(0.02)
        self.ids.timer.text = 'Disconnected'
        self.is_watching = False
        self.thread = None
            
    def reconnect_to_obs(self): ...
    
    
class MenuSub(BoxLayout):
    ...
    
class StartView(BoxLayout):
    ...
    
def overwrite(x: BoxLayout):
    
    x.clear_widgets()
    for i in range(4):
        x.add_widget(Button(text=f'{i}',size_hint_y = None, height = 40, on_press = lambda _instance: overwrite(x)))
    
def start():
    # Your code here
    ...