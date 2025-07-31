

from tkinter.messagebox import showerror
try:
    from jinja2 import Template
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nPIL')
    quit()
from bin.data_access_new import file_read,file_write
def deploy_render(*args,**replacers):
    JINJA_ENVIRONMENT = Template(file_read('static\\deploy.html'))


    file_write(args[0],JINJA_ENVIRONMENT.render(**replacers))