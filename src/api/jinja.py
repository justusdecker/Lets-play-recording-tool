from jinja2 import Template
def render_template(text: str, **replacers):
    return Template(text).render(**replacers)