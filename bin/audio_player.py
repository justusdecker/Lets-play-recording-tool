__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.146"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from pygame.mixer import init as m_init
from pygame.font import init as f_init
from pygame.display import (
    set_caption, 
    set_mode, 
    update
    )

from pygame.font import Font, get_default_font
from pygame.mixer_music import (
    load,
    play,
    pause,
    get_busy
)
from pygame.event import get as ev_get
from pygame import (
    QUIT,
    KEYDOWN,
    K_RETURN,
    K_SPACE,
    K_KP2,
    K_KP8,
    K_KP4,
    K_KP6
)

from os.path import isfile
from sys import argv
from random import randint as ri

from subprocess import run, CREATE_NO_WINDOW

f_init()
m_init()

def combine_audio(t1: str,t2: str,st: str,et: str, vol: float):
    """
    Combine two audio files
    
    .. t1::
        The mic track
    .. t2::
        The desktop track (This track will be volume modified)
    .. st::
        starttime in HH:MM:SS format must be a `str`
    .. et::
        endtime in HH:MM:SS format must be a `str`
    
    """
    #ffmpeg -ss 00:01:00 -to 00:02:00 -i {input_file} -c copy {result_file}
    
    """
    
                   add 
                   -filter:a "volume=0.5"
                    
                      
    """
    run(
                (
                    'ffmpeg',
                    '-y',               # Will replace existing output
                    
                    '-ss',
                    f'{st}',
                    '-to',
                    f'{et}',
                    '-i',               # Input filepath 2
                    f"{t2}",            # Input filepath 2

                    '-filter_complex',  #for merging
                    f'volume={vol}',  # For merging
                    '-ac', '2',         # Set audio channel
                    f"temp_t2.mp3"         # output filepath
                    ),
                CREATE_NO_WINDOW,
                shell= True
                )
    
    run(
                (
                    'ffmpeg',
                    '-y',               # Will replace existing output
                    '-ss',
                    f'{st}',
                    '-to',
                    f'{et}',
                    '-i',               # Input filepath 1
                    f"{t1}",            # Input filepath 1
                    

                    '-i',               # Input filepath 2
                    f"temp_t2.mp3",            # Input filepath 2

                    
                    '-filter_complex',  #for merging
                    'amerge=inputs=2',  # For merging
                    '-ac', '2',         # Set audio channel
                    f"temp.mp3"         # output filepath
                    ),
                CREATE_NO_WINDOW,
                shell= True
                )

def set_title(text: str):
    set_caption(f'{text} - (c) Justus Decker - LPRT Project')
'audio_player E:\musik\sortiert\S3RL\better-off-alone-s3rl-feat-tamika E:\musik\sortiert\S3RL\Waifu.mp3'
print(len(argv))
print(argv)
if len(argv) != 3:
    raise Exception("Insufficent Arguments")

class AudioPlayer:
    """
    The Audio Player uses Pygame:
    
    You can change the volume of the second track
    
    Play, Pause & Generate a comp
    """
    def __init__(self):
        self.isrunning = True
        self.display = set_mode((300,200))
        
        self.font = Font(get_default_font(),80)
        self.vol = 1.0
        
        self.t1, self.t2 = argv[1], argv[2]
        
        
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
        self.display.blit(self.font.render(f'{int(self.vol*100)}%',False,(255,255,255)),(0,self.font.get_height()))
        update()
        
    def update(self):
        """
        This method runs until the user closes the window
        """
        while self.isrunning:
            self.render()
            if get_busy():
                set_title('Playing Audio')
            else:

                set_title('Audio Player')
            for e in ev_get():
                
                if e.type == QUIT:
                    self.isrunning = False
                    
                if e.type == KEYDOWN:
                    
                    # generate audio 2 minutes only for performance reasons(Will be changed later)
                    if e.key == K_RETURN:
                        # Will be generated in a range from 0 - 5 minutes startpos + 2 minutes
                        if not get_busy():
                            set_title('Generating Audio')
                            combine_audio(self.t1,self.t2,f'00:0{ri(0,5)}:00','00:02:00',self.vol)
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
                        self.vol += 0.05
                    if e.key == K_KP2:
                        self.vol -= 0.05
                    if e.key == K_KP6:
                        self.vol += 0.01
                    if e.key == K_KP4:
                        self.vol -= 0.01
                
                    # keep the volume in range!
                    if self.vol > 1:
                        self.vol = 1
                    elif self.vol < 0:
                        self.vol = 0
                        
                    self.vol = float(f'{self.vol:.2f}') # keeps the volume clean
                    
AP = AudioPlayer()
AP.run()