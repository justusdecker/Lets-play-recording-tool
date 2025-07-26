
import jinja2
def file_write(filepath : str, data : str):
    with open(filepath, 'w') as f:
        f.write(data)
def file_read(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()
template_values = {
  'title': 'this is a test',   
}
JINJA_ENVIRONMENT = jinja2.Template(file_read('static\\deploy.html'))


file_write('test.html',JINJA_ENVIRONMENT.render(title='TEST',episodes=[{'id':3},{'id':6},{'id':2},]))