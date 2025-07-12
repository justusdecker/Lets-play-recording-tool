
import pygame as pg

from pygame.mixer import init as m_init
from pygame.font import init as f_init

from pygame.display import (
    set_caption, 
    set_mode, 
    update as d_update
    )

class GenericAudioPlayer:
    def __init__(self):
        self.display = set_mode((470,350))
        f_init()
        m_init()