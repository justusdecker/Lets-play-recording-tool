
from kivy.app import App, Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

# Layouts

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

# Extended Layouts

from kivy.uix.scrollview import ScrollView

# Default UIX

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from kivy.core.image import Image as CoreImage

# Advanced UIX

from kivy.uix.videoplayer import VideoPlayer

# Portfunction-relevant imports

import base64
from io import BytesIO

# Portfunctions from b64 -> Image

def b64toki(encoded_data: str, extension: str = 'png'):
    """
    Converts Base64-Encoded Image-Strings to Kivy usable Images.
    """
    decoded_data =  base64.b64decode(encoded_data.encode('ascii'))
    io_stream = BytesIO(decoded_data)
    texture = CoreImage(io_stream, ext=extension).texture
    return texture