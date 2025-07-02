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
    def run(self):
        self.update()
    def update(self):
        while self.isrunning:
            
            # Back button
            # Foreward button
            # play button
            #
            
            pg.draw.rect(self.display,(25,25,25),(0,100,100,100))
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.isrunning = False
AP = AudioPlayer('','')
AP.run()