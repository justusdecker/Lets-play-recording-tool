from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

import tkinter.ttk as ttk
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter import Toplevel, StringVar, BOTH, LEFT, HORIZONTAL, X
from bin.data_access import SQLAccess,AsciiImage
from bin.thumbnail import ThumbnailGenerator
from bin.constants import *
from bin.ffmpeg import *
from bin.other import convert_from_entities, convert_to_entities

try:
    import vlc
except:
    showerror('ERROR', ERROR_008 + '\nvlc')
    quit()

CHAR_TABLE = {
        'Ä':'&Auml;',
        'Ö':'&Ouml;',
        'Ü':'&Uuml;',
        'ä':'&auml;',
        'ö':'&ouml;',
        'ü':'&uuml;',
        'ß':'&szlig;'
     }

def convert_char(c: str):
    """
    converts characters to html usesable form.
    needs refactor see issue #150
    """
    if not c in CHAR_TABLE: return c
    return CHAR_TABLE[c]

WELCOME.update_message('Instanciate VLC')

VLC_INSTANCE = vlc.Instance()
from bin.media_player import NewMediaPlayer
class NewVideoPlayer(NewMediaPlayer):
    def __init__(self,parent, data: list[int],lpid,app):
        global change_states
        from bin.ui import change_states
        self.tg = ThumbnailGenerator()
        self.data: list[int] = data
        self.current_episode = 0
        self.isfinished = False
        self.lpid = lpid
        self.blocked = False
        self.title_var = StringVar()
        
        super().__init__(parent, app, audio_only=False)
        
        ttk.Label(self.bar,text='Title: ').pack(side=LEFT, padx=5)
        self.title_setter = ttk.Entry(self.bar,textvariable=self.title_var)
        self.title_setter.pack(side=LEFT, padx=5)
        
        self.update_title_button = ttk.Button(self.bar, text="Update", command=self.set_video_title)
        self.update_title_button.pack(side=LEFT, padx=5)
        
        self.take_thumbnail_btn = ttk.Button(self.bar,text='Generate Thumbnail',command=self.gen_thumbnail)
        self.take_thumbnail_btn.pack(side=LEFT, padx=5)
        
    def reset(self,data,lpid):
        change_states([self.stop_button,self.play_button, self.pause_button, self.next_button, self.last_button, self.take_thumbnail_btn, self.update_title_button],'disabled')
        self.stop_video()
        self.data: list[int] = data
        self.current_episode = 0
        self.isfinished = False
        self.lpid = lpid
        self.blocked = False
        self.play_video()
        change_states([self.stop_button,self.play_button, self.pause_button, self.next_button, self.last_button, self.take_thumbnail_btn, self.update_title_button],'!disabled')
        
    @property
    def rel_id(self) -> int:
        """ Get the current episode id """
        return self.data[self.current_episode] - 1
    
    @property
    def video_path(self) -> str:
        """ Get the video_path """
        return SQLAccess.read_final_video_path(self.lpid,self.rel_id)
    
    @property
    def video_title(self) -> str:
        """ Get the video_title """
        return convert_from_entities(SQLAccess.read_title(self.lpid,self.rel_id))
    
    @property
    def video_ep(self) -> str:
        """ Get the current episode number """
        return self.data[self.current_episode]
    
    def gen_thumbnail(self,*args):
        """ 
        generates a thumbnail based on the current frame played
        is currently broken see issue #246
        """
        if self.blocked: return
        self.blocked = True
        length = ffmpeg_run(FFMPEG_GET_LENGTH)
        if length is None: return
        frame = self.player.get_time() * .001
        try:
            self.tg.generate(
                str(self.data[self.current_episode]),
                self.video_path,
                SQLAccess.read_tad_path(self.lpid),
                f'{THUMBNAIL_FOLDER}_generated_from_video_{self.data[self.current_episode]}.png',
                frame
                )
        except AutomationError as E:
            
            showerror('ERROR','Cannot create Thumbnail.\n Dont select the last frame of a video.\nThat does not work work!')
            self.blocked = False
        
        print('finished generating')
        self.blocked = False
    
    def play_video(self):
        self.open_file(self.video_path)
        self.title_var.set(f'{self.video_title}')
        self.current_media_label.configure(text=f'{self.rel_id+1}_{SQLAccess.read_letsplay_name(self.lpid)}')
        return super().play_video()
    
    def set_video_title(self,*args):
        """ Sets the video title & updates the database. """
        new_title = ''.join([convert_char(c) for c in self.title_var.get()])
        SQLAccess.update_episode(self.lpid, self.rel_id,title=convert_to_entities(new_title))
    
    def episode_down(self,*args):
        """ Change the selected episode. One down. """
        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location
            self.play_video()
            
    def episode_up(self,*args):
        """ Change the selected episode. One up. """
        new_location = self.current_episode + 1
        
        l = len(self.data)
        
        if new_location > l - 1:
            self.current_episode = l - 1
        else:
            self.current_episode = new_location
            self.play_video()
            
