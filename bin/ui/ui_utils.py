import tkinter.ttk as ttk
def change_states(elements: list[ttk.Button],state: str):
    """
    Changes the state of a list of Tkinter `ttk.Button` widgets.

    This function iterates through a given list of `ttk.Button` objects
    and applies a specified state to each one. This can be used to enable,
    disable, or otherwise alter the visual and interactive state of buttons.
    """
    for element in elements:

        element.state([state])