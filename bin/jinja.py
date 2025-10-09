from bin.welcome_popup import WELCOME
from bin.translation import gtran
WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')

from tkinter.messagebox import showerror

from jinja2 import Template

from bin.data_access import file_read,file_write
from bin.constants import DEPLOY_HTML
def deploy_render(*args,**replacers):
    """
    Renders the default template ´deploy´ for easy upload.
    """
    JINJA_ENVIRONMENT = Template(DEPLOY_HTML)
    file_write(args[0],JINJA_ENVIRONMENT.render(**replacers))