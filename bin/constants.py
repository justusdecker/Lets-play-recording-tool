from bin.text_manipulation import *
from bin.data_access import file_read

MENU_MESSAGE = f"""
{bold('LPRT')} {italic(file_read('version.txt'))} - (c) Justus Decker 2024 - 2025

Select your option:
(1) Record - {color816(bold('ALPHA'),35)}
(2) {color816(strikethrough('Automation'),31)}
(3) {color816(strikethrough('Deploy'),31)}
(4) {color816(strikethrough('Distribute'),fg=31)}
(5) Exit
"""

MENU_AUTOMATION_MESSAGE = f"""
Automations - Submenu

Select your option:
(1) Thumbnail Generate
(2) Fetch Audio
(3) Fix Audio
(4) Render
(5) Back
"""

USER_INPUT_NUM_UNMATCHED = color816(bold('This option does not exist'),31)