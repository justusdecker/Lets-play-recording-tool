from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

import tkinter.ttk as ttk
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter import Toplevel, StringVar, BOTH, LEFT, HORIZONTAL, X
from bin.data_access import SQLAccess,AsciiImage, rie
from bin.thumbnail import ThumbnailGenerator
from bin.constants import *
from bin.ffmpeg import *
from bin.other import convert_from_entities, convert_to_entities
from os.path import isfile
from tools.log import LOG

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
        from bin.ui.ui_utils import change_states
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
        
        
        img = AsciiImage(ICO_REFRESH)
        self.update_title_button = ttk.Button(self.bar, image=img.image, command=self.set_video_title)
        self.update_title_button.pack(side=LEFT, padx=5)
        self.update_title_button.image = img.image
        
        
        img = AsciiImage(ICO_TAKE_THUMBNAIL)
        self.take_thumbnail_btn = ttk.Button(self.controls,image=img.image,command=self.gen_thumbnail)
        self.take_thumbnail_btn.pack(side=LEFT, padx=5)
        self.take_thumbnail_btn.image = img.image
        
    def reset(self,data,lpid):
        """ Resets to prevent errors """
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
        """
        if self.blocked: return
        self.blocked = True
        frame = self.player.get_time() * .001
        try:
            tad = SQLAccess.read_tad_path(self.lpid)
            lp_name = SQLAccess.read_letsplay_name(self.lpid)
            thumbnail_path = f'{THUMBNAIL_FOLDER}{self.rel_id}_{lp_name}_thumbnail.png'
            reoc(not tad, ERROR_009)
            reoc(not isfile(TAD_FOLDER + tad),ERROR_007 + '\nTAD Path does not exist!')
            
            rie(thumbnail_path)
            self.tg.generate(
                str(self.data[self.current_episode]),
                self.video_path,
                SQLAccess.read_tad_path(self.lpid),
                thumbnail_path,
                frame
                )
            SQLAccess.update_episode(self.lpid, self.rel_id,thumbnail_path=thumbnail_path)
            
        except AutomationError as E:
            
            showerror('ERROR','Cannot create Thumbnail.\n Dont select the last frame of a video.\nThat does not work!')
            self.blocked = False
        self.blocked = False
        
    def pause_video(self):
        """ Pauses the video """
        if not self.data: return
        return super().pause_video()
    
    def stop_video(self):
        """ Stops the video """
        if not self.data: return
        return super().stop_video()
    
    def play_video(self):
        """ 
        Plays the video
        
        Sets the Labeltext to the current video_path
        """
        if not self.data: return
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
            
