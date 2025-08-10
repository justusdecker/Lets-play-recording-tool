

from tkinter.messagebox import showerror
try:
    from jinja2 import Template
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nPIL')
    quit()
from bin.data_access import file_read,file_write
from bin.constants import DEPLOY_HTML
def deploy_render(*args,**replacers):
    """
    Renders the default template ´deploy´ for easy upload.
    """
    JINJA_ENVIRONMENT = Template(DEPLOY_HTML)
    file_write(args[0],JINJA_ENVIRONMENT.render(**replacers))