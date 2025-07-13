# LPRT

## What is LPRT?

LPRT is a recording, editing & distribution Tool for Let's Players like me

This is a terminal application so you need some terminal experience.

all the data is stored in `csv` & `json`.
Easy access & edit your data using a text-editor or Excel-like apps

## Current Development State

Work in progress(pre alpha)

- [x] Terminal Stuff(No practical usage! Only command inputs etc.)
- [x] Recording(Saving Data etc.)
- [x] Automation(Thumbnails)
- [x] Automation(Audio Fetch)
- [x] Automation(Audio Fix)
  - [x] Volume Comare & Set
  - [x] Loudness Normalization
  - [x] Noise Reduction
- [x] Automation(Combine Video & Audio)
- [ ] Deploy
- [ ] Distribute(COMING SOON!)

> [!CAUTION]
> This Application is still in development, many bugs may appear!(gotta catch them all🦍)
> 
> Some bugs can lead to data loss. **BE CAREFUL!**

## Requirements

> [!NOTE]
> I tested this app only on my own computer.
>
> More testing comes in the 0.9 update

Windows 10 64bit [R9 5900X, 32GB 3200Mhz, GTX 1660 6GB]

## Workflow (Production)

### Record

Select Option 1 in the Main Menu

Thats it! You only need to start the recording in OBS.

If you want to quit the recording menu: `STRG + C` in terminal.

> [!CAUTION]
> `STRG + C` or closing the terminal while you recording can lead to data loss!

To record you need connection to the OBS Webserver!

### Thumbnail Generation

### Audio Fetch

### Audio Fix

### Audio Compare

Audio comparing is mostly automated. 
You only need to: 
- start audio compare
- change audio volume
- apply audio volume from memory into the program

### Render

> [!NOTE]
> Rendering is currently not avaiable because some features like peak normalization cannot be automated without a significant performance impact.

Rendering will moved to resolve again.

### In Resolve

Import all needed videos LPRT will automatically create a new timeline for each episode.

For each Episode you need todo:

1. Select a timeline
2. Select the audio track
3. Press H + ENTER (This will normalize your audio to -1db)
4. Go to the "Deliver" page
5. Set the location(You only need to select the complete filepath one time, after that your only need to increase the episode number) My preset is {episode_number}_{letsplay_name}.mp4
6. Restrict bitrate to 15000 - 20000.
7. Add to render queue

If you appended all videos click "Render all"

## Programs you need

> [!IMPORTANT]
> All of the programs are needed to fully function!
https://ffmpeg.org/


[![FFMPEG](https://img.shields.io/badge/FFMPEG-007808?style=flat-square&logo=ffmpeg&logoColor=ffffff)](https://ffmpeg.org/)
[![OBS](https://img.shields.io/badge/obsstudio-302E31?style=flat-square&logo=obsstudio&logoColor=ffffff)](https://obsproject.com/de)

#### Connecting LPRT to OBS

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
    ```json
    {
        "ip": "{your ip}",
        "port": {your port},
        "pw": "{your password}",
        "timeout": 1
    }
    ```
11. Now you are ready to go!

#### Troubleshooting

##### IP changed
Sometimes your ip changes & LPRT will not recognize these changes.
You need to manually adjust the ip adress in `settings.json`
##### Password wrong
Simply adjust your `password` in `settings.json`
> [!IMPORTANT]
> If you're issue is not listed here, then please create an issue for this.
##### Known issues
###### Audio Stuff
Audio extract, limit, loudness normalize & noise reduce take ages currently.

#### First Recording

1. Open LPRT & `obs`
2. In LPRT select option `1`
3. Start Recording in `obs`
4. You see your recording time & LPRT will create a new entry in the selected episode

## File Structures

> [!CAUTION]
> Some file structures will change in development.
> Keep yourself up to date!

### Episodes

|id|key|type|
|---|---|---|
|0|video_path|`str`|
|1|audio_mic_path|`str`|
|2|audio_desktop_path|`str`|
|3|thumbnail_path|`str`|
|4|thumbnail_frame|`float`|
|5|has_problem|`bool`|
|6|audio_mic_edit1_path|`str`|
|7|audio_mic_edit2_path|`str`|
|8|audio_desktop_edit1_path|`str`|
|9|audio_desktop_edit2_path|`str`|
|10|title|`str`|
|11|episode_number|`int`|
|12|upload_at|`int`|
|13|final_video|`str`|

### Lets Play

|id|key|type|
|---|---|---|
|0|version|`str`|
|1|episode_path|`str`|
|2|tad_path|`str`|
|3|name|`str`|
|4|game_name|`str`|
|5|episode_length|`int`|
|6|description_path|`str`|


### Thumbnail Automation Data

```json
[
    {
        "pos": [0,0]
    },
    {
        "path": "test_logo.png",
        "scale": 1,
        "rot": 45,
        "pos": [100,100]
    },
    {
        "path": "",
        "scale": 2,
        "rot": -45,
        "color": [255,255,255,255],
        "ol_color": [1,1,1,255],
        "size": 40,
        "pos": [100,100]
    }
]
```


#### Background
The background is the first index currently you can define only the `fixed` Background position.
> [!NOTE]
> In the future there will be more options!
> Something like random position, rotation etc.
#### Logo
The logo is the second index. You can define:
|key|val|
|---|---|
|path|`str`|
|scale|`float` or `int`|
|rot|`float` or `int`|
|pos| `tuple` or `list` cont. `int`|
#### Text
The text is the third index. You can define:
|key|val|
|---|---|
|path|`str`|
|scale|`float` or `int`|
|rot|`float` or `int`|
|pos| `tuple` or `list` cont. `int`|
|color|`tuple` or `list` cont. **4** `int`|
|ol_color|`tuple` or `list` cont. **4** `int`|
|size|`int`|

## FFMPEG

replacers are named like: __ `value` __

### FFMPEG_DEFAULT

comes before the most commands
- Contains 'ffmpeg'
- This will be reduce terminal output
- Overwrites Files by default
- Has no replacers

### FFMPEG_CONVERT_AUDIO_TYPE

Converts Audio based on suffix like: 
`test.mp3` to `test.wav`

|key|type|desc|
|---|---|---|
|IN|`str`|Input Filepath|
|OUT|`str`|Output Filepath|

### FFMPEG_EXTRACT
An extremly fast ffmpeg command to extract 2 audio track from a video.
> [!NOTE]
> This Method is only ultra fast when you have the right audio type: `aac`, `mp3` etc.

|key|type|desc|
|---|---|---|
|IN|`str`|Input Filepath|
|OUT1|`str`|Output Filepath Mic|
|OUT2|`str`|Output Filepath Desktop|

### FFMPEG_AUDIO_COMBINE

Combine two audio tracks & apply volume changes

|key|type|desc|
|---|---|---|
|IN1|`str`|Input Filepath Mic|
|IN2|`str`|Input Filepath Desktop|
|VOLUME1|`float`|Volume for Mic|
|VOLUME2|`float`|Volume for Desktop|
|OUT|`str`|Output Filepath|

### FFMPEG_AUDIO_COMBINE_TRUNCATED

Combine two audio tracks & apply volume changes.
Cutted from `00:00:00` to `00:02:00`.

|key|type|desc|
|---|---|---|
|IN1|`str`|Input Filepath Mic|
|IN2|`str`|Input Filepath Desktop|
|VOLUME1|`float`|Volume for Mic|
|VOLUME2|`float`|Volume for Desktop|
|OUT|`str`|Output Filepath|

### FFMPEG_AUDIO_PF_LN_L

Uses:
- Highpass Filter : **13000**
- Lowpass Filter : **175**
- Loudness Normalization: **-15dB**
- Limiter : **0|0:1|1:0/-3|10/-3|20/-3:0.1:0:0:0** (Don't ask. I dont know what this means but it works)

to fix the Mic Audio Track

|key|type|desc|
|---|---|---|
|IN|`str`|Input Filepath|
|OUT|`str`|Output Filepath|

### FFMPEG_VIDEO_RENDER