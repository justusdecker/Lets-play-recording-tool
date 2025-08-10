import pygame as pg
from bin.constants import DISCLAIMER
from threading import Thread

class Welcome:
    """
    This is the welcome popup
    """
    def __init__(self):
        
        self.window = pg.display.set_mode((800,400),pg.NOFRAME)
        pg.display.set_caption('Welcome to LPRT')
        self.isrunning = True
        self.welcome = pg.image.load('bin\\data\\img\\welcome.png')
        
        self.clock = pg.time.Clock()
        pg.font.init()
        self.font = pg.font.Font(pg.font.get_default_font(),15)
        self.disclaimer = self.font.render(DISCLAIMER,True,(255,255,255))
        self.logo = pg.transform.scale(pg.image.load('bin\\data\\img\\logo.png'),(self.disclaimer.get_height(),self.disclaimer.get_height()))
        pg.display.set_icon(self.logo)
        self.font.set_point_size(20)
        self.update_message('Here i am...')
    def run(self):
        """ calls the private self.__run method """
        Thread(target=self.__run).start()
    def __run(self):
        """ runs until loading is complete """
        while self.isrunning:
            try:
                self.window.blit(self.welcome)
                self.window.blit(self.logo,(16,400-self.disclaimer.get_height()-16))
                self.window.blit(self.message,(400-(self.message.get_width()//2),200-(self.message.get_height()//2)))
                
                self.window.blit(self.disclaimer,(self.disclaimer.get_height()+32,400-self.disclaimer.get_height()-16))
                self.clock.tick(10)
                pg.display.update()
            except:
                pass
    def update_message(self,text: str):
        self.message = self.font.render(text,True,(255,255,255))
    def destroy(self):
        """ removing its existance! """
        self.isrunning = False
        pg.display.quit()
        del self
WELCOME = Welcome()
WELCOME.run()