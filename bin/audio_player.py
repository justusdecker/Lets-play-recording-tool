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
    K_KP2,
    K_KP8,
    K_KP4,
    K_KP6,
    K_LEFT,
    K_RIGHT,
    quit as pg_quit
)

from os.path import isfile

from bin.constants import ffmpeg_run,FFMPEG_AUDIO_COMBINE_TRUNCATED


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
        self.audio_list = [[*i,1] for i in audio_list]# idx a1 a2 vid vol
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
        self.volume_slider()
        self.display.blit(self.font.render('00:00',False,(255,255,255)))
        self.display.blit(self.font.render(f'{int(self.audio_list[self.current_episode][4]*100)}%',False,(255,255,255)),(0,self.font.get_height()))
        d_update()
        
    def titleset(self):
        if get_busy():
            self.set_title('Playing Audio')
        else:

            self.set_title('Audio Player')
            
    def select_episode(self,direction: int):
        new_location = self.current_episode + direction
        
        l = len(self.audio_list)
        
        if new_location >= l:
            self.current_episode = l - 1
            
        elif new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location
            self.ready_to_play = False
    def volume_slider(self):
        h = 200
        
        0,200
        draw_rect(self.display,(64,64,64),(260,0,40,self.audio_list[self.current_episode][4]*200))
        
        v = self.audio_list[self.current_episode][4]
        #!! will be changed later
        if v > 0.25:
            draw_line(self.display,(255,128,128),(260,50),(300,50))
        if v > 0.5:
            draw_line(self.display,(255,128,128),(260,100),(300,100))
        if v > 0.75:
            draw_line(self.display,(255,128,128),(260,150),(300,150))
        mp = get_pressed()[0]
        x, y = get_pos()
        if mp:
            if x >= 260 and x <= 300 and y >= 0 and y <= 199:
                self.audio_list[self.current_episode][4] = y / 199
                self.audio_list[self.current_episode][4] = float(f'{self.audio_list[self.current_episode][4]:.2f}')
                draw_line(self.display,(128,255,128),(260,y),(300,y),3)
        
        
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
                            self.set_title('Generating Audio')
                            unload()
                            ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{'__IN1__':self.audio_list[self.current_episode][1],'__IN2__': self.audio_list[self.current_episode][2],'__VOLUME1__': str(1.0),'__VOLUME2__': str(self.audio_list[self.current_episode][4]),'__OUT__':'temp.mp3'})
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
                        self.audio_list[self.current_episode][4] += 0.05
                    if e.key == K_KP2:
                        self.audio_list[self.current_episode][4] -= 0.05
                    if e.key == K_KP6:
                        self.audio_list[self.current_episode][4] += 0.01
                    if e.key == K_KP4:
                        self.audio_list[self.current_episode][4] -= 0.01
                
                    # keep the volume in range!
                    if self.audio_list[self.current_episode][4] > 1:
                        self.audio_list[self.current_episode][4] = 1
                    elif self.audio_list[self.current_episode][4] < 0:
                        self.audio_list[self.current_episode][4] = 0
                        
                    self.audio_list[self.current_episode][4] = float(f'{self.audio_list[self.current_episode][4]:.2f}') # keeps the volume clean
        pg_quit()
        
if __name__ == "__main__":
    AP = AudioPlayer('','')
    AP.run()
    input('SLOW')