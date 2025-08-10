import pygame as pg
from bin.constants import DISCLAIMER
from threading import Thread

class Welcome:
    """
    This is the welcome popup
    """
    def __init__(self):
        self.window = pg.display.set_mode((800,400),pg.NOFRAME)
        self.isrunning = True
        self.welcome = pg.image.load('bin\\data\\img\\welcome.png')
        
        self.clock = pg.time.Clock()
        pg.font.init()
        font = pg.font.Font(pg.font.get_default_font(),15)
        self.font = font.render(DISCLAIMER,True,(255,255,255))
        self.logo = pg.transform.scale(pg.image.load('bin\\data\\img\\logo.png'),(self.font.get_height(),self.font.get_height()))
        
    def run(self):
        """ calls the private self.__run method """
        Thread(target=self.__run).start()
    def __run(self):
        """ runs until loading is complete """
        while self.isrunning:
            try:
                self.window.blit(self.welcome)
                self.window.blit(self.logo,(16,400-self.font.get_height()-16))
                self.window.blit(self.font,(self.font.get_height()+32,400-self.font.get_height()-16))
                self.clock.tick(10)
                pg.display.update()
            except:
                pass
    def destroy(self):
        """ removing its existance! """
        self.isrunning = False
        pg.display.quit()
        del self
        