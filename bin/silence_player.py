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
from pygame.mouse import get_pos, get_pressed
from pygame.mixer_music import (
    load,
    play,
    pause,
    get_busy,
    unload
)

from pygame.draw import rect as draw_rect, line as draw_line
from pygame.event import get as ev_get
from pygame.time import Clock
from pygame import (
    QUIT,
    KEYDOWN,
    K_RETURN,
    K_SPACE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    quit as pg_quit
)

from os.path import isfile

class AudioPlayer:
    """
    The Audio Player uses Pygame:
    
    You can change the volume of the second track
    
    Play, Pause & Generate a comp
    """
    def __init__(self, audio_list: list[list[str]]):
        self.isrunning = True
        self.display = set_mode((300,200))
        self.clk = Clock()
        self.current_episode = 0
        self.current_audio = 0
        self.audio_list = audio_list
        self.audio_pointer = [0 for i in range(len(audio_list))]
        f_init()
        m_init()
        self.font = Font(get_default_font(),80)
    def set_title(self, text: str):
        set_caption(f'[{self.current_episode}] {text} - (c) Justus Decker - LPRT Project')
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
        self.display.blit(self.font.render(f'{int(self.audio_list[self.current_episode][4]*100)}%',False,(255,255,255)),(0,self.font.get_height()))
        d_update()
        
    def titleset(self):
        if get_busy():
            self.set_title('Playing Audio')
        else:

            self.set_title('Silence Player')
    def select_audio(self,direction: int):
        
        new_location = self.current_audio + direction
        
        l = len(self.audio_list[self.current_audio])
        
        if new_location >= l:
            self.current_audio = l - 1
        elif new_location < 0:
            self.current_audio = 0
            self.audio_pointer[self.current_episode] = self.current_audio
        else:
            self.current_audio = new_location
            self.audio_pointer[self.current_episode] = self.current_audio
         
    def select_episode(self,direction: int):
        new_location = self.current_episode + direction
        
        l = len(self.audio_list)
        
        if new_location >= l:
            self.current_episode = l - 1
            
        elif new_location < 0:
            self.current_episode = 0
            self.current_audio = 0
        else:
            self.current_episode = new_location
            self.current_audio = 0
    @property
    def audio(self) -> str:
        return self.audio_list[self.current_episode][self.current_audio]
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
                    if e.key == K_UP:
                        self.select_audio(-1)
                    elif e.key == K_DOWN:
                        
                        self.select_audio(1)
                    # generate audio 2 minutes only for performance reasons(Will be changed later)
                    if e.key == K_RETURN:
                        
                        # Will be generated in a range from 0 - 5 minutes startpos + 2 minutes
                        if not get_busy():
                            unload()
                            #combine_audio(self.t1,self.t2,f'00:0{s}:00',f'00:{s+2}:00',self.vol)
                            if isfile(self.audio):
                                load(self.audio)
                                play()
                            
                    if e.key == K_SPACE:
                        if get_busy():
                            pause()
                        else:
                            if isfile(self.audio):
                                load(self.audio)
                                play()
                            else:
                                pass
        pg_quit()
        
if __name__ == "__main__":
    AP = AudioPlayer('','')
    AP.run()
    input('SLOW')