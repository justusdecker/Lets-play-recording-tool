from kivy.uix.widget import Widget
from typing import Callable
from bin.views.modules import Button
def button_builder(parent: Widget, on_press_callback: Callable, **kwargs):
    btn = Button(**kwargs)
    btn.bind(on_press=on_press_callback)
    parent.add_widget(btn)
    return btn