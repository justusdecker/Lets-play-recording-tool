from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from bin.constants import *

from pygame.transform import scale, flip, rotate, scale_by, rotozoom
from pygame import Surface,SRCALPHA,Color,mask

from random import random as rnd, randint as ri

from os.path import isfile

from bin.data_access import json_read,rie
from pygame.image import save as img_save, load as img_load
from bin.ffmpeg import ffmpeg_run, FFMPEG_GET_FRAME, FFMPEG_GET_LENGTH
from pygame.font import Font, init, get_default_font
init()

def get_time_va(filepath: str):
    time_or_error = ffmpeg_run(FFMPEG_GET_LENGTH,{'__IN__':filepath},True)
    try:
        return float(time_or_error.replace('\n',''))
    except Exception as E:
        print(E)
        return None

def get_thumbnail(filepath: str,frame:None) -> Surface:
    if frame == -1:
        t = rnd() * get_time_va(filepath)
    else:
        t = frame
    print(t,frame,get_time_va(filepath),filepath)
    rie(f'{TEMP_FOLDER}temp.png')
    ffmpeg_run(FFMPEG_GET_FRAME,{'__IN__': filepath, '__TIME__': t})
    reoc(not isfile(f'{TEMP_FOLDER}temp.png'),ERROR_007)
    return img_load(f'{TEMP_FOLDER}temp.png')


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
class ImageTextRenderer:
    #10 chars from 0 to 9
    #image width must be even
    #image width / 10
    def __init__(self,img: str):
        
        sprite_map = img_load(img)
        img_array = []
        
        if sprite_map.get_width() % 2:
            raise Exception('Image width must be even!')

        self.offset_x = sprite_map.get_width() // 10
        
        for x in range(10):
            sprite_char = Surface((sprite_map.get_width() // 10,sprite_map.get_height()), SRCALPHA)
            sprite_char.blit(sprite_map,(0,0),(x*self.offset_x,0,self.offset_x,sprite_map.get_height()))
            img_array.append(sprite_char)
        self.chars = {key: img for img, key in zip(img_array,'0123456789')}

    def draw(self,text:str) -> Surface:
        font = Surface((self.offset_x*len(text),self.chars['0'].get_height()),SRCALPHA)
        for idx,char in enumerate(text):
            if char in self.chars:
                font.blit(self.chars[char],(self.offset_x*idx,0))

        return font
    def get_blit_data(self):return self.data , self.offset_pos

class ThumbnailGenerator:
    """
    A class used to generate custom thumbnails by composing a background (from a video frame or solid color), 
    a text overlay, and a logo, based on a Thumbnail Automation Data (TAD) configuration file.

    This generator allows for dynamic positioning, scaling, rotation, 
    and styling of each component to create visually appealing thumbnails.
    """
    def __init__(self): pass
    
    def generate(self,
                 text: str,
                 video_path: str | None,
                 tad_path: str,
                 save_to_path: str,
                 frame: float = -1,
                 
                 ):
        """
        Generates a thumbnail image by combining a background, logo, and text overlay, and saves it to the specified path.

    The thumbnail's appearance (background, logo, text styles, positions, rotations, and scales) 
    is determined by the configuration loaded from the Thumbnail Automation Data (TAD) file.

    Args:

    text (str): The text content to be rendered on the thumbnail.

    video_path (str | None): The file path to the video from which a background frame will be extracted. If None, a solid dark grey background is used.

    tad_path (str): The relative or absolute path to the Thumbnail Automation Data (TAD) JSON configuration file.

    save_to_path (str): The file path (including filename and extension, e.g., '.png') where the generated thumbnail will be saved.

    frame (float, optional): The timestamp (in seconds) of the specific frame to extract from the video. If -1, a random frame is chosen. Defaults to -1.
        """
        
        print((f'[Thumbnail Generate]: {video_path}',94))
        self.tad = json_read(TAD_FOLDER + tad_path)
        if video_path is None:
            bg = Surface((1280,720))
            bg.fill((34,34,34))
        else:
            bg = self.__render_background(video_path,frame)
        bg_pos = (
            (1280//2) - (bg.get_width() // 2), 
            (720//2) - (bg.get_height() // 2)
            )
        logo = self.__render_logo()
        if self.tad['logo::center']:
            x = (1280//2) - (logo.get_width() // 2) + self.tad['logo::pos::x']
            y = self.tad['logo::pos::y']
            print(x,y)
            logo = logo, (x,y)
        
        text_r = self.__render_text(text)
        if self.tad['text::center']:
            x = (1280//2) - (text_r.get_width() // 2) + self.tad['text::pos::x']
            y = self.tad['text::pos::y']
            print(x,y)
            text_r = text_r, (x,y)

        img = self.__comp_render(
            [(bg,bg_pos) if self.tad['bg::center'] else bg,
            logo,
            text_r]
            )
        
        self.__save(save_to_path,img)
        
    def __save(self,
               filepath: str,
               surf: Surface):
        """
        Saves a given Pygame Surface to a specified file path as an image.

        Args:

        filepath (str): The full path including the filename and extension (e.g., '.png') where the image will be saved.

        surf (pygame.Surface): The Pygame Surface object to be saved.
        """
        img_save(surf,filepath)
        
    def __get_src_image(self, 
                      file: str, 
                      frame: float | int = -1
                      ): # should not be none!
        """
        Get a frame from a video or load an image file to be used as a source image.

        This method retrieves a specific frame from a video file using get_thumbnail, scales it to DEFAULT_THUMBNAIL_SIZE, 
        and flips it horizontally before returning it as a Pygame Surface. If the input file does not exist, a FileNotFoundError is raised.
        
        Args:

        file (str): The path to the video file.

            Must be a string.

            Can be a relative or absolute path.

            frame (float | int, optional): The timestamp (in seconds) of the frame to extract.

            Must be numeric.

            frame can be -1 (for a random frame) or from 0 to the video length.

            Possible crash if frame > video length. Defaults to -1.

        Returns:

            pygame.Surface: A Pygame Surface object representing the processed video frame.

        Raises:

            FileNotFoundError: If the specified file does not exist.

        .. attention::

            video_src will only be updated if the file path changes.
            See issue #249
        """
        
        # What happens here?
        #Creates a new Surface from a videoframe.
        # At first get a numpy like object from VideoFileClip.get
        # The result must be rotated to show up correctly
        # Then a Surface will be created, scaled & flipped at the x axis.
        
        if isfile(file):
            

            # Create a new Video Source to get images from
            self.image = get_thumbnail(file,frame)
            # TODO -> old code: frame if frame >= 0 and frame  <= self.video_src.duration else 0 
            
            _returnImage: Surface = scale(self.image,DEFAULT_THUMBNAIL_SIZE)
            _returnImage: Surface = flip(_returnImage,True,False)
            
            return _returnImage
        raise FileNotFoundError('Your Image does not exist!')
    
    def __comp_render(self,objs: list[tuple[Surface,tuple[int,int]]]) -> Surface:
        """
        Composites multiple Pygame Surface objects onto a single new Surface.

        This method creates a new Surface of DEFAULT_THUMBNAIL_SIZE with transparency (SRCALPHA) and blits each provided object onto it at its specified position.

        Args:

            objs (list[tuple[pygame.Surface, tuple[int, int]]]): A list of tuples, where each tuple contains a Pygame Surface and its (x, y) position to blit it at.

        Returns:

            pygame.Surface: The newly created composite Surface containing all blitted objects.
        """
        COMP = Surface(DEFAULT_THUMBNAIL_SIZE,SRCALPHA)
        for obj,pos in objs:
            COMP.blit(obj,pos)
        return COMP
    
    def __render_text(self,
                 text: str= ''
                 ) -> Surface:
        """
        Renders the provided text onto a Pygame Surface, applying styling (font, color, outline, scale, rotation) based on the self.tad configuration.

        The text can be rendered using either a standard font (TrueType/OpenType) or an image-based font renderer (ImageTextRenderer) depending on the text::path setting in the TAD file. An outline is always applied if specified in TAD.

        Args:

            text (str, optional): The string of text to render. Defaults to an empty string.

        Returns:

            pygame.Surface: A Pygame Surface containing the rendered and styled text.
        """
        if not isfile(self.tad['text::path']) or self.tad['text::path'].endswith('.ttf') or self.tad['text::path'].endswith('.otf'):
            if not isfile(self.tad['text::path']):
                font = Font(get_default_font(),self.tad['text::size'])
            else:
                font = Font(self.tad['text::path'],self.tad['text::size'])
            
            img: Surface = font.render(text,False,Color(self.tad['text::color']) if self.tad['text::color'] else (255,255,255))

        elif self.tad['text::path'].endswith('.png'):
            img = ImageTextRenderer(self.tad['text::path']).draw(text)
            
            
        timg = outlining(img,Color(self.tad['text::ol_color']) if self.tad['text::ol_color'] else (1,1,1))
            
        timg = scale_by(timg,self.tad['text::scale'])
        
        timg = rotate(timg,self.tad['text::rot'])
        return timg
    
    def __render_logo(self) -> Surface:
        """
        Renders the logo image based on the path, scale, and rotation defined in the self.tad configuration.

        If the logo file specified in self.tad['logo::path'] does not exist, an empty (1x1 transparent) Surface is returned.

        Returns:

            pygame.Surface: A Pygame Surface containing the loaded and styled logo.
        """
        if not isfile(self.tad['logo::path']):
            # File does not exist so return an empty logo
            return Surface((1,1),SRCALPHA)
        surf = img_load(self.tad['logo::path'])
        
        surf = scale_by(surf,self.tad['logo::scale'])
        
        surf = rotate(surf,self.tad['logo::rot'])
        
        #center image position calculation [x,y] [w,h]
        # x - (w / 2) & y - (h / 2)
        return surf
    def __render_background(self, filepath: str, frame: float):
        """
        Renders the background image for the thumbnail, applying positional offsets, random rotation, and random scaling based on self.tad configuration.

        This method first retrieves the source image/video frame using __get_src_image, then applies random variations to its position, rotation, and scale before returning the modified Surface.

        Args:

            filepath (str): The path to the video file or image to use as the background.

            frame (float): The specific frame (timestamp in seconds) to extract from the video.

        Returns:

            pygame.Surface: A Pygame Surface representing the prepared background image.
        """
        img = self.__get_src_image(filepath, frame)
        r_rot_from = int(self.tad['bg::r_rot::from'] * 100)
        r_rot_to = int(self.tad['bg::r_rot::to'] * 100)
        final_rot = self.tad['bg::rot'] + (ri(r_rot_from, r_rot_to) / 100)
        
        final_rot = max(-45, min(final_rot, 45))
        
        r_scale_from = self.tad['bg::r_scale::from']
        r_scale_to = self.tad['bg::r_scale::to']
        final_scale = self.tad['bg::scale'] + (ri(int(r_scale_from * 100), int(r_scale_to * 100)) / 100)

        final_scale = max(0.1, min(final_scale, 2.0))
        print(final_rot, final_scale)
        if final_rot or final_scale != 1:
            img = rotozoom(img, final_rot, final_scale)
        
        return img