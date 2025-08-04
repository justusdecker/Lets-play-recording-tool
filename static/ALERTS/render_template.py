from jinja2 import Environment, FileSystemLoader

# --- The key change is here ---
# The loader now points to the new directory
file_loader = FileSystemLoader('static/ALERTS')
# Note: Use forward slashes '/' or double backslashes '\\' for Windows paths
# file_loader = FileSystemLoader('static\\ALERTS')

env = Environment(loader=file_loader)

# Load the main template file
template = env.get_template('index.html')

# --- Your data would go here ---
template_data = {
    'page_title': "My Jinja Documentation",
    'main_heading': "A Demonstration of Jinja Templates",
    'sample_list': [
        "This is the first item.",
        "This is the second item.",
        "The third item can contain <strong>HTML</strong>.",
    ],
    'sample_table_headers': ['Key', 'Type', 'Description'],
    'sample_table_rows': [['IN', 'str', 'Input Filepath']],
}

# Render the template with your data
rendered_html = template.render(**template_data)

# Save the output to a new HTML file
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(rendered_html)

print("Template rendered successfully and saved to output.html!")