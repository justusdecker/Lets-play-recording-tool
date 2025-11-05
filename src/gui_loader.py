import os

"""
The UI will be instanciated and after that,
the tkinter_app will get this

We need:
    * The UI Class
    * The NAME Variable of the element

At the top we will get all of the lprt dependecys and gives these to exec
"""
for file in os.listdir('./pack/gui/'):
    print(file)
    with open(f'./pack/gui/{file}') as f:
        data = f.read()
    exec(data)
    print(NAME, UI())