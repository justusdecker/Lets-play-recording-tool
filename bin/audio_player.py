#from pydub import AudioSegment

# Pydub is broken
# playsound
# wave
#pyaudio noplayback

import pygame as pg

class AudioPlayer:
    def __init__(self,t1,t2):
        self.isrunning = True
        self.display = pg.display.set_mode((300,200))
        pg.font.init()
        self.font = pg.font.Font(pg.font.get_default_font(),80)
        self.vol = 1
    def run(self):
        self.update()
    def update(self):
        while self.isrunning:
            
            self.display.blit(self.font.render('00:00',False,(255,255,255)))
            self.display.blit(self.font.render(f'{self.vol}',False,(255,255,255)),(0,self.font.get_height()))
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.isrunning = False
                if e.type == pg.KEYDOWN:
                    
                    # Set the volume for the next prehearing
                    if e.key == pg.K_2:
                        self.vol += 0.05
                    if e.key == pg.K_8:
                        self.vol -= 0.05
                    if e.key == pg.K_6:
                        self.vol += 0.01
                    if e.key == pg.K_4:
                        self.vol -= 0.01
                
                    # keep the volume in range!
                    if self.vol > 1:
                        self.vol = 1
                    elif self.vol < 0:
                        self.vol = 0
                    
AP = AudioPlayer('','')
AP.run()