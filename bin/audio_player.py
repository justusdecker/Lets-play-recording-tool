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
        self.font = pg.font.Font(pg.font.get_default_font())
    def run(self):
        self.update()
    def update(self):
        while self.isrunning:
            
            self.display.blit(self.font.render('00:00',False,(255,255,255)))
            
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.isrunning = False
AP = AudioPlayer('','')
AP.run()