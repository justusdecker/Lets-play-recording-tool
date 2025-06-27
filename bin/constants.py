from bin.text_manipulation import *
from bin.data_access import file_read

COPYRIGHT = f"{bold('LPRT')} {italic(file_read('version.txt'))} - (c) Justus Decker 2024 - 2025"

MENU_MESSAGE = f"""
{COPYRIGHT}

{bold('Main >')}

Select your option:
(1) Record - {color816(bold('ALPHA'),35)}
(2) Automation - {color816(bold('ALPHA'),35)}
(3) {color816(strikethrough('Deploy'),31)}
(5) Data
(0) Exit
"""

MENU_AUTOMATION_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Automations >')}

Select your option:
(1) {color816(strikethrough('Thumbnail Generate'),31)}
(2) {color816(strikethrough('Fetch Audio'),31)}
(3) {color816(strikethrough('Fix Audio'),31)}
(4) {color816(strikethrough('Render'),31)}
(5) Back
"""

MENU_DATA_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Data')}

Select your option:
(1) {color816(strikethrough('Create a new file'),31)}
(2) Create a new entry - {color816(bold('ALPHA'),35)}
(3) {color816(strikethrough('Update'),31)}
(4) {color816(strikethrough('Read'),31)}
(5) {color816(strikethrough('Delete'),fg=31)}
(0) Exit
"""

MENU_DATA_CREATE_ENTRY_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Data > Create a new entry')}

Select your option:
(1) {color816(strikethrough('Lets Play'),31)}
(2) {color816(strikethrough('Episode'),31)}
(3) {color816(strikethrough('Thumbnail Automation Data'),31)}
(0) Exit
"""

MENU_DATA_READ_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Data > Read')}

Select your option:
(1) {color816(strikethrough('Lets Play'),31)}
(2) {color816(strikethrough('Episode'),31)}
(3) {color816(strikethrough('Thumbnail Automation Data'),31)}
(0) Exit
"""

MENU_DATA_UPDATE_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Data > Update')}

Select your option:
(1) {color816(strikethrough('Lets Play'),31)}
(2) {color816(strikethrough('Episode'),31)}
(3) {color816(strikethrough('Thumbnail Automation Data'),31)}
(0) Exit
"""

USER_INPUT_NUM_UNMATCHED = color816(bold('This option does not exist'),31)

