__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND" # No changes in the obs_ws source code!
__version__ = ""
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from pygame.surfarray import make_surface
from pygame.transform import scale, flip, rotate, scale_by
from pygame import Surface,SRCALPHA,Color,mask
from bin.text_manipulation import color816

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
    return surface
class ThumbnailGenerator:
    def __init__(self): pass
    
    def generate(self,
                 text: str,
                 video_path: str,
                 tad_path: str,
                 save_to_path: str,
                 frame: float = -1,
                 
                 ):
        print(color816(f'[Thumbnail Generate]: {video_path}',94))
        _bg, _logo, _text = json_read(tad_path)

        img = self.__comp_render(
            [self.__render_background(video_path,frame,_bg),
            self.__render_logo(_logo),
            self.__render_text(_text,text)]
            )
        
        self.__save(save_to_path,img)
        
    def __save(self,
               filepath: str,
               surf: Surface):
        img_save(surf,filepath)
        
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
            

            # Create a new Video Source to get images from
            self.video_src = VideoFileClip(file,audio=False)

            if frame == -1: 
                # Frame is not valid so take a random value from 0 to video.duration
                frame = rnd()*(self.video_src.duration)
            
            # Sets the index for the last image. Use: Pick the last Thumbnail
            self.idx = frame if frame >= 0 and frame  <= self.video_src.duration else 0 

            _returnImage: Surface = make_surface(rot90(self.video_src.get_frame(self.idx)))
            _returnImage: Surface = scale(_returnImage,DEFAULT_THUMBNAIL_SIZE)
            _returnImage: Surface = flip(_returnImage,True,False)
            
            return _returnImage
        raise FileNotFoundError('Your Image does not exist!')
    
    def __comp_render(self,objs: list[tuple[Surface,tuple[int,int]]]) -> Surface:
        COMP = Surface(DEFAULT_THUMBNAIL_SIZE,SRCALPHA)
        for obj,pos in objs:
            COMP.blit(obj,pos)
        return COMP
    
    def __render_text(self, tad: dict,
                 text: str= ''
                 ) -> Surface:
        """
        Returns the Text Image with outline
        """

        if not 'color' in tad:
            tad['color'] = (0,0,0,255)
        if not isfile(tad['path']):
            font = Font(get_default_font(),tad['size'])
        else:
            font = Font(tad['path'],tad['size'])
        
        img: Surface = font.render(text,False,tad['color'])
        
        timg = outlining(img,tad['ol_color'])
        
        timg = scale_by(timg,tad['scale'])
        
        timg = rotate(timg,tad['rot'])
        
        return timg, tad['pos']
    
    def __render_logo(self, tad: dict) -> tuple[Surface, tuple[int, int]]:
        if not isfile(tad['path']):
            # File does not exist so return an empty logo
            return Surface((1,1),SRCALPHA),(0,0)
        surf = img_load(tad['path'])
        
        surf = scale_by(surf,tad['scale'])
        
        surf = rotate(surf,tad['rot'])
        
        #center image position calculation [x,y] [w,h]
        # x - (w / 2) & y - (h / 2)
        x, y = [a - (b * .5) for a, b in zip(tad['pos'], surf.get_size())]
        
        return surf, (x,y)
    
    def __render_background(self, filepath: str, frame: float, tad: dict): #Here rotation, color manipulation will be added
        return self.__get_src_image(filepath, frame),tad['pos']