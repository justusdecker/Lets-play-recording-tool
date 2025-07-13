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
  - [ ] Noise Reduction
- [x] Automation(Combine Video & Audio)
- [ ] Deploy
- [ ] Distribute(COMING SOON!)

> [!CAUTION]
> This Application is still in development, many bugs may appear!(gotta catch them all🦍)
> 
> Some bugs can lead to data loss. **BE CAREFUL!**

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

#### First Recording

1. Open LPRT & `obs`
2. In LPRT select option `1`
3. Start Recording in `obs`
4. You see your recording time & LPRT will create a new entry in the selected episode

