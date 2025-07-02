#from pydub import AudioSegment

# generate audio sample ()
# will be a snippet from the original 15 seconds from a random position
# combine audio samples
# play in pygame

import pygame as pg

class AudioPlayer:
    def __init__(self,t1,t2):
        self.isrunning = True
        self.display = pg.display.set_mode((300,200))
        pg.font.init()
        self.font = pg.font.Font(pg.font.get_default_font(),80)
        self.vol = 1.0
    def run(self):
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