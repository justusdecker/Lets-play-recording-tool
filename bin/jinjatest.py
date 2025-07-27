
from jinja2 import Template
from bin.data_access import file_read,file_write
def deploy_render(*args,**replacers):
    JINJA_ENVIRONMENT = Template(file_read('static\\deploy.html'))


    file_write(args[0],JINJA_ENVIRONMENT.render(**replacers))