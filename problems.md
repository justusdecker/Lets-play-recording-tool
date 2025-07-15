# OnStart

# Path Generation

|path|name|usage|
|---|---|---|
|C:/%Users%/lprt|root|root folder|
|`root`/audio|audio|extracted audio|
|`root`/video|video|final video|
|`root`/temp|temp|all temporary files e.g. for type convert|
|`root`/audio_fixed|audio_fixed|HP-LP-LN-L results|
|`root`/thumbnails|thumbnails|generated thumbnails|
|`root`/tad|tad|Thumbnail Automation Data|

# Creating Essential Files

|path|
|---|
|`root`/settings.json|
|`root`/letsplays.csv|
|`root`/logo.ico|

# Edgees

|Condition|result|
|---|---|
|LP File is empty|User cannot enter any automation menu!|
|Selected EP File is empty|User cannot enter any automation menu!|
|LP File is broken -> Wrong `row` or `col` count|Program will safeclose!|
|EP File is broken -> Wrong `row` or `col` count|Program will safeclose!|


all of the above: -> with an appropiate warning message

# The Submenu -> Automation System is crap

The submenus currently:

```python
ifs = binpi(f'Did you want to overwrite thumbnail[{i+1}]?\n[1]Yes\n[2]No\n')
if ifs == 1:
    while 1:
        TG.generate(
            str(i+1),
            video_path,
            tad,
            f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
            )
        ok = binpi('Okay\n[1]Yes\n[2]No\n')
        if ok == 1:
            break
else:
    while 1:
        TG.generate(
            str(i+1),
            video_path,
            tad,
            f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
            )
        ok = binpi('Okay\n[1]Yes\n[2]No\n')
        if ok == 1:
            break
```
will be changed to pseudo code:
```python
ifs = binpi(f'Did you want to overwrite thumbnail[{i+1}]?\n[1]Yes\n[2]No\n')
while 1:
    if ifs == 1: break
    TG.generate(
        str(i+1),
        video_path,
        tad,
        f'{THUMBNAIL_FOLDER}{i+1}_{self.lp_name}_thumbnail.png'
        )
    ok = binpi('Okay\n[1]Yes\n[2]No\n')
    if ok == 1:
        break
```
# Binpi

Dont forget that the binpi function will be enhanced!
currently you can input every number 0 - inf

- The new binpi function can take the legal argument: list[int]
- The function checks user_input in legal

# Remove Moviepy
- This blows up exe size
- instead we use ffmpeg to extract the thumbnail like this:
  ```batch
  ffmpeg -ss 00:15:00.00 -i test.mp4 -frames:v 1 result.png
  ```
- We get the video_length by using `ffprobe`
  ```batch
  ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 test.mp4
  ```

# Switching to sqlite

It will be easier to manage new entrys in sqlite than csv.

# Massive Storage Allocation

For 100 Videos: 20 - 30 Minutes
OBS Settings:
15 k/bits video
192k mic
192k desk
64k sync

- Audacity will take for at least 200 GB of disk space -> can be removed after noise reduction & audio edit
- 500 MB to 3 GB Audio temps
- 200 GB final video
- 200 GB raw
More or less than 600 GB. A bit to much i think.
Mostly about 400 GB usage, if you dont forget to delete some data!
