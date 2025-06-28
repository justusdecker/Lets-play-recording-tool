from pygame.surfarray import make_surface
from pygame.transform import scale, flip, rotate, scale_by
from pygame import Surface,SRCALPHA,Color,mask

from numpy import rot90

from random import random as rnd

from os.path import isfile

from bin.data_access import json_read
from moviepy.video.io.VideoFileClip import VideoFileClip
from pygame.image import save as img_save, load as img_load
from bin.constants import DEFAULT_THUMBNAIL_SIZE
from pygame.font import Font, init, get_default_font
init()

def outlining(image: Surface,color: tuple[int]=(0,0,0,255)) -> Surface:
    shade = mask.from_surface(image).to_surface()
    shade.set_colorkey((0,0,0))


    normal = Surface((image.get_width()*1.05,image.get_height()*1.05),SRCALPHA)

    for x in range(shade.get_width()):
        for y in range(shade.get_height()):
            if shade.get_at((x,y)) != Color(0,0,0,255):
                normal.set_at((x,y),color)

    surface = Surface(image.get_size(),SRCALPHA) 
    for pos in [(-2,0),(2,0),(0,-2),(0,2)]: #outline offset
        surface.blit(normal,pos)
    surface.blit(image,(0,0))
class ThumbnailGenerator:
    def __init__(self, 
                 filepath: str,
                 videopath: str):
        self.videopath = videopath
        self.data = json_read(filepath)
    
    def generate(self,
                 text: str,
                 video_path: str,
                 tad_path: str,
                 save_to_path: str,
                 frame: float = -1,
                 
                 ):
        _bg, _logo, _text = json_read(tad_path)
        surface = self.__render_background(video_path,frame)
        text_surface = self.__render_text(_text['path'],_text['size'],text)
        self.__comp_render(
            (self.__get_src_image(video_path,frame),_bg['pos'])
            )
    def __get_src_image(self, 
                      file: str, 
                      frame: float | int = -1
                      ): # should not be none!
        """
        Get a frame from a video
        -----
        
        .. file::
            - Must be a string
            - Can be a relative or absolut path
        .. frame::
            - Must be numeric
            - ``frame`` can be -1 or from ``0`` to ``video length``.
            - Possible crash if ``frame`` > ``video length ``
        
        **ATTENTION**
            ``video_src`` will only be updated if the ``file`` path changes

        """
        
        # What happens here?
        #Creates a new Surface from a videoframe.
        # At first get a numpy like object from VideoFileClip.get
        # The result must be rotated to show up correctly
        # Then a Surface will be created, scaled & flipped at the x axis.
        
        if isfile(file):
            
            if self.videopath != file: 
                # Create a new Video Source to get images from
                self.video_src = VideoFileClip(file,audio=False)

            if frame == -1: 
                # Frame is not valid so take a random value from 0 to video.duration
                frame = rnd()*(self.video_src.duration)
            
            # Sets the index for the last image. Use: Pick the last Thumbnail
            self.idx = frame if frame >= 0 and frame  <= self.video_src.duration else 0 

            _returnImage: Surface = make_surface(rot90(self.video_src.get_frame(self.idx)))
            _returnImage: Surface = scale(_returnImage,self.default_size)
            _returnImage: Surface = flip(_returnImage,True,False)
            
            return _returnImage
        raise FileNotFoundError('Your Image does not exist!')
    
    def __comp_render(self,objs: list[tuple[Surface,tuple[int,int]]]):
        COMP = Surface(DEFAULT_THUMBNAIL_SIZE,SRCALPHA)
        for obj,pos in objs:
            COMP.blit(obj,pos)
    
    def __render_text(self,
                 font_path: str,
                 font_size: int = 20,
                 text: str= '',
                 color=(0,0,0,255)
                 ) -> Surface:
        """
        Returns the Text Image with outline
        """

        if not isfile(font_path):
            font = Font(get_default_font(),font_size)
        else:
            font = Font(font_path,font_size)
        
        img: Surface = font.render(text,False,color)
        
        timg = outlining(img,color)
        
        return timg
    
    def __render_logo(self, filepath: str) -> tuple[Surface, tuple[int, int]]:
        if not isfile(filepath):
            # File does not exist so return an empty logo
            return Surface((1,1),SRCALPHA),(0,0)
        surf = img_load(entry['path'])
            
        surf = scale(surf,self.default_size)
        
        surf = scale_by(surf,entry['scale'])
        
        surf = rotate(surf,entry['rot'])
        
        cropping()
        
        x = int(entry['pos'][0] - (surf.get_width() *.5))
            
        y = int(entry['pos'][1] - (surf.get_height() *.5))
        
        return surf, (x,y)
    def __render_background(self, filepath: str, frame: float): #Here rotation, color manipulation will be added
        return self.__get_src_image(filepath, frame)