__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.3.146"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from pygame.mixer import init as m_init
from pygame.font import init as f_init
from pygame.display import (
    set_caption, 
    set_mode, 
    update as d_update
    )

from pygame.font import Font, get_default_font
from pygame.mixer_music import (
    load,
    play,
    pause,
    get_busy,
    unload
)
from pygame.event import get as ev_get
from pygame.time import Clock
from pygame import (
    QUIT,
    KEYDOWN,
    K_RETURN,
    K_SPACE,
    K_KP2,
    K_KP8,
    K_KP4,
    K_KP6,
    K_LEFT,
    K_RIGHT,
    quit as pg_quit
)

from os.path import isfile

from subprocess import run, CREATE_NO_WINDOW

from bin.constants import ffmpeg_run,FFMPEG_AUDIO_COMBINE_TRUNCATED

def set_title(text: str):
    set_caption(f'{text} - (c) Justus Decker - LPRT Project')
'audio_player E:\musik\sortiert\S3RL\better-off-alone-s3rl-feat-tamika E:\musik\sortiert\S3RL\Waifu.mp3'
class AudioPlayer:
    """
    The Audio Player uses Pygame:
    
    You can change the volume of the second track
    
    Play, Pause & Generate a comp
    """
    def __init__(self, audio_list):
        self.isrunning = True
        self.display = set_mode((300,200))
        self.clk = Clock()
        self.vol = 1.0
        self.current_episode = 0
        self.ready_to_play = False
        self.audio_list = [[*i,1] for i in audio_list]# idx a1 a2 vol
        f_init()
        m_init()
        self.font = Font(get_default_font(),80)
        
    def run(self):
        """
        Here starts app the app
        """
        self.update()
    
    def render(self):
        """
        Here renders all the elements on screen
        """
        self.display.fill((24,24,24))
        self.display.blit(self.font.render('00:00',False,(255,255,255)))
        self.display.blit(self.font.render(f'{int(self.audio_list[self.current_episode][3]*100)}%',False,(255,255,255)),(0,self.font.get_height()))
        d_update()
        
    def titleset(self):
        if get_busy():
            set_title('Playing Audio')
        else:

            set_title('Audio Player')
            
    def select_episode(self,direction: int):
        new_location = self.current_episode + direction
        
        l = len(self.audio_list)
        
        if new_location >= l:
            self.current_episode = l - 1
            
        elif new_location < 0:
            self.current_episode = 0
        else:
            self.ready_to_play = False
            
    def update(self):
        """
        This method runs until the user closes the window
        """
        while self.isrunning:
            
            self.render()
            self.titleset()
            self.clk.tick(30)
            for e in ev_get():
                
                if e.type == QUIT:
                    self.isrunning = False
                
                if e.type == KEYDOWN:
                    
                    if e.key == K_LEFT:
                        self.select_episode(-1)
                    elif e.key == K_RIGHT:
                        
                        self.select_episode(1)
                    # generate audio 2 minutes only for performance reasons(Will be changed later)
                    if e.key == K_RETURN:
                        # Will be generated in a range from 0 - 5 minutes startpos + 2 minutes
                        if not get_busy():
                            set_title('Generating Audio')
                            unload()
                            ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{'__IN1__':self.audio_list[self.current_episode][1],'__IN2__': self.audio_list[self.current_episode][2],'__VOLUME1__': str(1.0),'__VOLUME2__': str(self.audio_list[self.current_episode][3]),'__OUT__':'temp.mp3'})
                            self.ready_to_play = True
                            #combine_audio(self.t1,self.t2,f'00:0{s}:00',f'00:{s+2}:00',self.vol)
                            if isfile('temp.mp3'):
                                load('temp.mp3')
                                play()
                            
                    if e.key == K_SPACE:
                        if get_busy():
                            pause()
                        else:
                            if isfile('temp.mp3'):
                                load('temp.mp3')
                                play()
                            else:
                                pass
                    
                    # Set the volume for the next prehearing
                    if e.key == K_KP8:
                        self.audio_list[self.current_episode][3] += 0.05
                    if e.key == K_KP2:
                        self.audio_list[self.current_episode][3] -= 0.05
                    if e.key == K_KP6:
                        self.audio_list[self.current_episode][3] += 0.01
                    if e.key == K_KP4:
                        self.audio_list[self.current_episode][3] -= 0.01
                
                    # keep the volume in range!
                    if self.audio_list[self.current_episode][3] > 1:
                        self.audio_list[self.current_episode][3] = 1
                    elif self.audio_list[self.current_episode][3] < 0:
                        self.audio_list[self.current_episode][3] = 0
                        
                    self.audio_list[self.current_episode][3] = float(f'{self.audio_list[self.current_episode][3]:.2f}') # keeps the volume clean
        pg_quit()
        
if __name__ == "__main__":
    AP = AudioPlayer('','')
    AP.run()
    input('SLOW')