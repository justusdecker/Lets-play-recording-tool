from bin.text_manipulation import *
from bin.data_access import file_read

MENU_MESSAGE = f"""
{bold('LPRT')} Version: {italic(file_read('version.txt'))} - (c) Justus Decker 2024 - 2025

Select your option:
(1) Record - {color816(bold('ALPHA'),35)}
(2) {color816(strikethrough('Automation'),31)}
(3) {color816(strikethrough('Deploy'),31)}
(4) {color816(strikethrough('Distribute'),fg=31)}
"""