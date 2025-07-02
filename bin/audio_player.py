# will be converted to exe & called with arguments

argv[1:2]

# will be a snippet from the original 15 seconds from the start pos
# The second time the audio will be rendered for two minutes straight

# ffmpeg -ss 00:01:00 -to 00:02:00 -i {input_file} -c copy {result_file}
# combine audio samples
# play in pygame

p2 = 'E:\\musik\\sortiert\\S3RL\\bad-boy.mp3'
p1 = 'E:\\musik\\sortiert\\S3RL\\Waifu.mp3'
from audio import combine_audio
combine_audio(p1,p2,'00:00:10','00:00:20')
import pygame as pg
from sys import argv
print(argv[1:2])

class AudioPlayer:
    def __init__(self,t1,t2):
        self.isrunning = True
        self.display = pg.display.set_mode((300,200))
        pg.font.init()
        self.font = pg.font.Font(pg.font.get_default_font(),80)
        self.vol = 1.0
    def run(self):
        """
        Here starts app the app
        """
        self.update()
    
    def render_normal(self):
        self.display.fill((24,24,24))
        self.display.blit(self.font.render('00:00',False,(255,255,255)))
        self.display.blit(self.font.render(f'{int(self.vol*100)}%',False,(255,255,255)),(0,self.font.get_height()))
        pg.display.update()
    def update(self):
        while self.isrunning:
            self.render_normal()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.isrunning = False
                if e.type == pg.KEYDOWN:
                    
                    # generate audio 2 minutes only for performance reasons(Will be changed later)
                    if e.key == pg.K_SPACE:
                        pass 
                    
                    # Set the volume for the next prehearing
                    if e.key == pg.K_KP8:
                        self.vol += 0.05
                    if e.key == pg.K_KP2:
                        self.vol -= 0.05
                    if e.key == pg.K_KP6:
                        self.vol += 0.01
                    if e.key == pg.K_KP4:
                        self.vol -= 0.01
                
                    # keep the volume in range!
                    if self.vol > 1:
                        self.vol = 1
                    elif self.vol < 0:
                        self.vol = 0
                        
                    self.vol = float(f'{self.vol:.2f}') # keeps the volume clean
                    
AP = AudioPlayer('','')
AP.run()