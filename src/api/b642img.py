from kivy.core.image import Image as CoreImage
import base64
from io import BytesIO

def b64toki(encoded_data: str, extension: str = 'png'):
    """
    Converts Base64-Encoded Image-Strings to Kivy usable Images.
    """
    decoded_data =  base64.b64decode(encoded_data.encode('ascii'))
    io_stream = BytesIO(decoded_data)
    texture = CoreImage(io_stream, ext=extension).texture
    return texture