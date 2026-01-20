# The Version 2

The new 2.0 Update will be a complete Overhaul in terms of UI.

On top the most of the external libs that are licensed under GPL V3 will be thrown out of this project!

## The Massive Todo List 

### REWRITE

We remove most of the unused / uneccessary dependencys.

The first thing we are going to rewrite is the entire ui code.

* [ ] the entire ui in kvlang
    * [ ] msgbox -> popup
    * [ ] wintoasty -> win32api

* [ ] `obs-ws` -> Own Solution
* [x] `tkinter` -> `kivy`
* [ ] `tkcalendar` -> Own Solution
* [ ] `pygame-ce` -> `pillow`
* [ ] the entire `media-player`, `audio-player`, `thumbnail-player` & `video-player` code to match the new `kivy` requirements.
* [ ] `winotify` -> Own Solution
* [ ] Audacity -> SOX see #383

### NEW FEATURES - MINOR

* [ ] Auto Updates
* [ ] API Improvements
    * [ ] Auto crash reports
    * [ ] Workshop

### NEW FEATURES - MAJOR

#### MODULE SUPPORT

Modules will be loaded from a specific zip file.

|sub_title|filetype|description|
|---|---|---|
|SQL Database Definition|`.sql`|The User can define its own DB entrys if neccessary|
|Python SBSL(Scope-Based-Scripting-Language)|`.py`|Automate & Optimize your Lets Plays even further with python|
|KVLang Extensions|`.kv`|Write your own UI Extensions.|
|LICENSE|`license`|Yeah...|
|README|`readme`|Your Documentation|

##### SECRUITY
For Secruity Reasons most of the Features are disabled by default

You need to enable Scopes in your Settings!

|Affects|Scope-Name|function|
|---|---|---|
|Data processing|FILE_READ|read_file, read_file_as_json, ...|
|Data processing|FILE_WRITE|write_file, write_file_as_json, ...|
|Data processing|FILE_OVERWRITE|same as write with overwrite privileges.|
|Data processing|FILE_DELETE|remove_file|
|Database Access|DATABASE_READ|database_read|
|Database Access|DATABASE_WRITE|database_WRITE|
|Console Access->command|CMD_*COMMAND*|CMD("*command*")|
|Admin|ADMIN|deactivates the sandbox entirely

### SUPPORT

* [ ] Linux-compatibility(idk)
* [ ] Mac-compatibility(M2 Chip support and higher)

### REMOVE

* [ ] Old UI Code stored in `./bin/ui/`
* [ ] `./bin/welcome_popup.py`
* [ ] `./bin/welcome_popup.py`
* [ ] Old devtools -> ncu
* [ ] AI Crap. Nobody will use this right... right?

### OUTSOURCE

* [ ] Old Automation Code stored in `./bin/auto/`