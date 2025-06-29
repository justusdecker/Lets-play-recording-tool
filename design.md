# LPRT

## What is LPRT?

LPRT is a recording, editing & distribution Tool for Let's Players like me

all the data is stored in `csv` & `json`.
Easy access & edit your data using a text-editor or Excel-like apps

## Current Development State

Work in progress(pre alpha)

- [x] Terminal Stuff(No practical usage! Only command inputs etc.)
- [x] Recording(Saving Data etc.)
- [ ] Automation(Thumbnails)
- [ ] Automation(Audio Fetch)
- [ ] Automation(Audio Fix)
- [ ] Automation(Combine Video & Audio)
- [ ] Deploy(COMING SOON!)
- [ ] Distribute(COMING SOON!)

> [!CAUTION]
> So many bugs may appear!
> Some bugs can lead to data loss. **BE CAREFUL!**

## How to use?

### Programs you need

> [!IMPORTANT]
> All of the programs are needed to fully function!
https://ffmpeg.org/


[![FFMPEG](https://img.shields.io/badge/FFMPEG-007808?style=flat-square&logo=ffmpeg&logoColor=ffffff)](https://ffmpeg.org/)
[![OBS](https://img.shields.io/badge/obsstudio-302E31?style=flat-square&logo=obsstudio&logoColor=ffffff)](https://obsproject.com/de)

### Recording

Connecting LPRT to OBS
---
1. Open OBS
2. Click on the `tools` dropdown
3. Click on `Websocket Server-Settings`
4. Activate `Websocket Server`
5. Set your `port`
6. Activate `authentification`!
7. Generate a new password
8. Click on show `Connection information`
9. Copy `ip`, `port` & `password`
10. Create a file named `settings.json` in `root`, copy & paste the lines below & replace your information with the placeholders!
    ```
    {
        "ip": "{your ip}",
        "port": {your port},
        "pw": "{your password}",
        "timeout": 1
    }
    ```
11. Now you are ready to go!

Troubleshooting
---
Sometimes your ip changes & LPRT will not recognize these changes.
You need to manually adjust the ip adress in `settings.json`



