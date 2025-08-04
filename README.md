You can get the current state [here](https://github.com/justusdecker/Lets-play-recording-tool/milestones) & More Info [here](https://github.com/justusdecker/Lets-play-recording-tool/wiki/)

> [!CAUTION]
> This Application is still in development, many bugs may appear!(gotta catch them all🦍)
> 
> Some bugs can lead to data loss. **BE CAREFUL!**

> [!IMPORTANT]
> All of the programs are needed to make LPRT fully function!

# Setup
## Connecting LPRT to OBS
### Installation

Download & Install from the [OBS Website](https://obsproject.com/de) or use the [Steam version](https://store.steampowered.com/app/1905180/OBS_Studio/)

### Further Steps
1. Open OBS
2. Click on the `tools` dropdown
3. Click on `Websocket Server-Settings`
4. Activate `Websocket Server`
6. Activate `authentification`!
7. Generate a new password
8. Click on show `Connection information`
9. Copy `ip`, `port` & `password` into `{ROOT}/obs_settings.json`. Replace your information with the placeholders!
    ```json
    {
        "ip": "{your ip}",
        "port": "{your port}",
        "pw": "{your password}",
        "timeout": 1
    }
    ```

## Connecting to Audacity
### Installation
Download & Install [Audacity](https://www.fosshub.com/Audacity-old.html) & the [FFMPEG for Audacity lib](https://lame.buanzo.org/)

> [!WARNING]
> Currently only Audacity 3.0.0 is supported.
>
> Currently only FFMPEG-Audacity 2.2.2 is supported.
>
> Other versions might not work as expected!

### Enabling the Mod-Pipe
1. Open Audacity
2. Edit > Settings > Module > enable mod-script-pipe
3. Reopen Audacity & Reopen LPRT

### Installing the FFMPEG-Audacity Lib

1. Edit > Settings > Libraries > search
2. Select the `avformat-55.dll` normally located in `C:\Program Files\FFmpeg For Audacity\`. (Only if Audacity does this not automatically)
3. Reopen Audacity

## FFMPEG Installation

1. Download a ffmpeg copy in `zip` format from [here](https://www.gyan.dev/ffmpeg/builds/)
2. Copy `ffmpeg`, `ffplay`, `ffprobe`(currently not needed!) into `C:\Windows\System32`.
3. Windows will prompt you(Admin privileges). This is normal!

> [!NOTE]
> You can skip point `2` if you know how to use Windows-PATH.(This section will be added later!)

# Troubleshooting

## IP changed
Sometimes your ip changes & LPRT will not recognize these changes.
You need to manually adjust the ip adress in `{ROOT}obs_settings.json`

## Password wrong
Simply adjust your `password` in `{ROOT}obs_settings.json`
> [!IMPORTANT]
> If you're issue is not listed here, then please create an issue for this.

## Audacity connection is sometimes pure bs
Trouble while setting up Audacity? Thats a common problem, please create an issue for this.