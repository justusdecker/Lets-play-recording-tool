from os import getlogin
USERNAME = getlogin()
del getlogin

COPYRIGHT = f"LPRT <VERSION_STR_MISSING> - <HASH_STR_MISSING> | GPL 3.0 - (c) Justus Decker 2024 - 2026"

DISCLAIMER = f"""
{COPYRIGHT}
Welcome to LPRT

A Let's Play automation tool that simplifies your workflow 
for recording, editing, and distribution.

Do you find a bug? Share it with us!

For Documentation, please look up the GitHub-wiki
"""

ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'

DEFAULT_THUMBNAIL_SIZE = (1280,720)

DEFAULT_OBS_SETTINGS = {
    "ip": "",
    "port": 1234,
    "pw": "",
    "timeout": 1
}

DEFAULT_TAD = {
    "bg::pos::x": 0,
    "bg::pos::y": 0,
    "bg::r_pos::x-from": 0,
    "bg::r_pos::x-to": 0,
    "bg::r_pos::y-from": 0,
    "bg::r_pos::y-to": 0,
    "bg::r_scale::from": 0,
    "bg::r_scale::to": 0,
    "bg::r_rot::from": 0,
    "bg::r_rot::to": 0,
    "bg::center": True,
    "bg::scale": 1.35,
    "bg::rot": 0,

    "logo::path": "",
    "logo::scale": 1,
    "logo::rot": 0,
    "logo::pos::x": 0,
    "logo::pos::y": 0,
    "logo::center": True,

    "text::path": "",
    "text::scale": 1,
    "text::rot": 0,
    "text::color": "",
    "text::ol_color": "",
    "text::size": 40,
    "text::pos::x": 0,
    "text::pos::y": 0,
    "text::center": True
}

from src.api.license import __LICENSE__