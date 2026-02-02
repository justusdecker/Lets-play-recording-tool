<img width="128" height="128" alt="logo" src="bin\\data\\img\\logo.png" />


# LPRT

[![wakatime](https://wakatime.com/badge/user/e971c7f6-586b-4713-b710-561bca159241/project/7e61f36a-218d-416b-8bb1-640812cf9b2f.svg)](https://wakatime.com/badge/user/e971c7f6-586b-4713-b710-561bca159241/project/7e61f36a-218d-416b-8bb1-640812cf9b2f)

## What is LPRT?

LPRT is an open-source windows-only recording, editing & distribution tool or lets plays.
This tool includes features like filemanagement to make your life as a lets player much easier.
## Infovideo(German)
[![LPRT Infovideo in German Click to watch](https://img.youtube.com/vi/aoJOTMbmd3w/0.jpg)](https://www.youtube.com/watch?v=aoJOTMbmd3w)

## Features
- Your recordings cannot mix up anymore - You dont need to rename / handle your recordings in general. LPRT saves the paths for further editing & distribution.
- Warns you before the maximum length is exceeded and alerts you if it is exceeded.
- Automated Thumbnail Generation - You can generate Thumbnails in batch.
- Audio Extraction - Tired of Unbalanced audio volume? Thats a thing of the past.
- Audio Fix - Automated Audio Effect applying e.g. Highpass, Lowpass & Loudness Normalization.
- Audacity Integration - To edit your audio further you can use Audacity & reimport the audio back into LPRT.(Noise Reduction)
- Ultra fast Video rendering.
- Audio volume comparison.
- Thumbnail generation will watching the preview of your video & title setting to make the upload process easier.
- Deploying - Provides an easy to use HMTL File(with all the upload essential data) and Exporting your data to an external drive(optional)
- Easy to use in-built Filemanagement
- AI generated title suggestions

## What do you need? - (Standalone)
> [!NOTE]
> No worry. This might be a bit overwhelming at first!
> We have a detailed installationguide right [here](https://github.com/justusdecker/Lets-play-recording-tool/wiki/Setup)
> 
- A computer that can play the games you are recording. Can work on slower system. Recommended specs: A non-potato GPU & at least 16 GB RAM
- Third Party Software
  - OBS Studio
  - Audacity - 3.0.0
  - FFMPEG for Audacity
  - FFMPEG - (downloads automatically)
  - [libpng16-16.dll](https://github.com/pnggroup/libpng) - (unpacks automatically)

> [!NOTE]
> FFMPEG & libpng16-16.dll downloading / installing automatically.

> [!IMPORTANT]
> All of the programs are needed to make LPRT fully function!
## What do you need? - (For Developers)

You need [this](requirements.txt) libraries & [the programs here](#what-do-you-need---standalone) too.

## State of Development

The most essential features are implemented right now. A bug here and there may appear.(gotta catch them all🦍)
You can get the current state [here](https://github.com/justusdecker/Lets-play-recording-tool/milestones)

> [!CAUTION]
> A few bugs / User error can lead to data loss(Only your lets plays!). **BE CAREFUL!**
> For this case. You can backup your videos etc. anytime by using the FileManager! 


## Join LPRT-development

If you are interested in LPRT, its programming, artworks, testing or something like that, you're welcome to participate in the development of LPRT.

Information about what you can do and be found in the [wiki](https://github.com/justusdecker/Lets-play-recording-tool/wiki)

You have an idea or suggestions? Make sure to file an issue & wait for replies!
Maybe there are different ideas, improvements, or hints or maybe your feature is not welcome / needed at the moment.

## How to compile yourself
run `compile.bat` from the `./tools` directory.

You must change the paths for images etc. in the spec file yourself.

---
---


# The v2.0 Update

## Deploy improvements

### Faster, easier & less errors

The `letsplay` table in `lprt_data.db` will become another row: `jitle`

The full title will be (default)
```jinja
{{ %episode_title% }} | {{ %letsplay_name% }} {{ %letsplay_emoji% }} #{{ %episode_number% }}
```
> The result will be e.g.:
> 
> `something happened` | `valheim` `😁` #`123`
> 
> `something happened | valheim 😁 #123`

This upgrade results in a faster, less error-prone, and easier way to retrieve video titles.

[HTML Emoji Codes 🍋🍑🍄](https://www.w3schools.com/html/html_emojis.asp)

For more info #382

***

### The view.html becomes an upgrade

A function will be added that copies the desired text with a single click.

***

### Upload_at

A workflow will be added that sets the upload_at value for all selected episodes.
This value will be shown in view.html.
Faster & less error-prone

For more info #380 #381

## remove existing files if wanted

This option is for clearing the output folder before the automation.

## Translation

Translation will be added with `v1.1`
> [!NOTE]
> For now only German & English are supported!

## Help everywhere

Help windows will be added for each automation.

## Removing the popups

All unnecessary setting pop-ups will be removed and replaced by the main window settings.

## Audacity Integration will be removed!

To further streamline this step, Audacity will be removed from the workflow and replaced by SOX.

It is handier, causes fewer problems, and, most importantly, is automatable. Another key aspect is the user experience; downloading Audacity and A-FFMPEG is ~~pina~~ 🤬

This will be the last feature of the v2.0 update.

For more info #383

## Modules

Create your own modules for workflows in YAML

Currently LPRT is working with hardcoded workflows in python.

The improvement here is: you can optimize & individualize your own workflows.

Workflows will be downloadable with the LPRT API.

Example
***
```yml
name: Audio Fix
description: Apply audio processing filters to microphone tracks within a defined episode range.
include: |
    data_access        
    ffmpeg_api          
    constants           
    ui_manager         
    core_helpers
    progress_bar

ui:
  - name: lpep-selector
    inherit: lpepp
    id: lpep_selector
    mode: lp-ep
    btn_image: $ICO_RUN
  
  - name: Audio Filter Options
    inherit: audio_filters
    id: filter_options

workflow:

  steps:

    - name: Create if not exist
      call: data_access.cnef
      args:
          - $FIXED_AUDIO_FOLDER

    - name: Read Episodes
      call: data_access.SQLA_read_episodes
      id: episodes
      args:
          - $lpid
      output: episodes

    - name: Clean Progressbar
      call: progress_bar.clear
      args:
          - $rng
    
    - name: wf
      loop:
      range: 
          - $ep_start
          - $ep_end
      as: i
      enum: ci
      steps:

        - name: Increment Progressbar
          call: progress_bar.increment

        - name: Get AMP From
          call: data_access.get_audio_mic_path
          args: 
              - $episodes
              - $i
          output: audio_mic_path
        
        - name: Get AMP To
          call: data_access.get_audio_mic_path1
          args: 
              - $FIXED_AUDIO_FOLDER
              - $i
              - $lp_name
          output: audio_mic_edit_path1

        - name: File exist check
          call: data_access.file_exists
          args: 
              - $audio_mic_path

        - name: Remove existing result
          call: data_access.rie
          args: 
              - $audio_mic_edit_path1
        
        - name: FFMPEG Audio Fix
          call: ffmpeg_api.run
          args: 
              - FFMPEG_AUDIO_PF_LN_L
              - $audio_mic_path
              - $audio_mic_edit_path1
          
        - name: File exist check
          call: data_access.file_exists
          args: 
              - $audio_mic_edit_path1

        - name: Config Progressbar
          call: progress_bar.increment
          args:
              - $i
              - $ci
              - $rng

        - name: Update Episode
          call: data_access.SQLA_update_episodes
          args:
              - $lpid
              - $i
              - $audio_mic_edit_path1
```