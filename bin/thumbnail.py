__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.5.10"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Production"

from pygame.surfarray import make_surface
from pygame.transform import scale, flip, rotate, scale_by
from pygame import Surface,SRCALPHA,Color,mask


from numpy import rot90

from random import random as rnd, randint as ri

from os.path import isfile

from bin.data_access import json_read
from pygame.image import save as img_save, load as img_load
from bin.constants import DEFAULT_THUMBNAIL_SIZE, ffmpeg_run, FFMPEG_GET_FRAME, FFMPEG_GET_LENGTH
from pygame.font import Font, init, get_default_font
init()

def get_time_va(filepath: str):
    time_or_error = ffmpeg_run(FFMPEG_GET_LENGTH,{'__IN__':filepath},True)
    try:
        return float(time_or_error.replace('\n',''))
    except :
        return None

def get_thumbnail(filepath: str) -> Surface:
    t = rnd() * get_time_va(filepath)
    ffmpeg_run(FFMPEG_GET_FRAME,{'__IN__': filepath, '__TIME__': t})
    return img_load('temp.png')


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
        print((f'[Thumbnail Generate]: {video_path}',94))
        _bg, _logo, _text = json_read(tad_path)
        bg = self.__render_background(video_path,frame,_bg)
        bg_pos = (
            (1280//2) - (bg[0].get_width() // 2), 
            (720//2) - (bg[0].get_height() // 2)
            )
        logo = self.__render_logo(_logo)
        if _logo['center']:
            x = (1280//2) - (logo[0].get_width() // 2) + _logo['pos'][0]
            y = _logo['pos'][1]
            print(x,y)
            logo = logo[0], (x,y)
        
        text_r = self.__render_text(_text,text)
        if _text['center']:
            x = (1280//2) - (text_r[0].get_width() // 2) + _text['pos'][0]
            y = _text['pos'][1]
            print(x,y)
            text_r = text_r[0], (x,y)
            
        print(_logo)
        img = self.__comp_render(
            [(bg[0],bg_pos) if _bg['center'] else bg,
            logo,
            text_r]
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
            self.image = get_thumbnail(file)
            # TODO -> old code: frame if frame >= 0 and frame  <= self.video_src.duration else 0 
            
            _returnImage: Surface = scale(self.image,DEFAULT_THUMBNAIL_SIZE)
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
        
        # Manipulate pos
        rx,ry = tad['r_pos']
        rx, ry = ri(*rx), ri(*ry)
        mpx = tad['pos'][0] + rx
        mpy = tad['pos'][1] + ry
        img = self.__get_src_image(filepath, frame)
        
        a, b = tad['r_rot']
        a, b = int(a * 100), int(b * 100)
        r = tad['rot'] + (ri(a, b) / 100)
        if r:
            img = rotate(img, r)
        
        a, b = tad['r_scale']
        a, b = int(a * 100), int(b * 100)
        s = tad['scale'] + (ri(a, b) / 100)
        if s != 1:
            img = scale_by(img, s)

        return img,(mpx, mpy)