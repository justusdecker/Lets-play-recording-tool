from pygame.surfarray import make_surface
from pygame.transform import scale, flip, rotate, scale_by
from pygame import Surface,SRCALPHA,Color

from numpy import rot90

from random import random as rnd

from os.path import isfile

from bin.data_access import json_read
from moviepy.video.io.VideoFileClip import VideoFileClip
from pygame.image import save as img_save, load as img_load
from bin.constants import DEFAULT_THUMBNAIL_SIZE
from pygame.font import Font, init
init()
class ThumbnailGenerator:
    def __init__(self, 
                 filepath: str,
                 videopath: str):
        self.videopath = videopath
        self.data = json_read(filepath)
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
    def __get_text(self,
                 font_path: str,
                 font_size: int,
                 text: str,
                 outline: dict,
                 color=(255,255,255)
                 ) -> Surface:
        """
        Returns the Text Image
        """


        font = Font(font_path,font_size)
        
        img: Surface = font.render(text,False,color)
        
        # 1 is the font image size
        w1,h1 = img.get_size()
        
        # timg is used to outline text
        
        # create a new blank surface (RGBA) - USAGE OUTLINE
        timg = Surface((w1 * 1.05,h1 * 1.05),SRCALPHA)
        
        w2,h2 = timg.get_size()
        
        x = (w2 / 2) - (w1 / 2)
        
        y = (h2 / 2) - (h1 / 2)
        
        timg.blit(img,(x,y))
        
        
        
        timg = outLining(
            outline['xMinus'],
            outline['xPlus'],
            outline['yMinus'],
            outline['yPlus'],
            timg,outline['color']
            )
        
        return timg