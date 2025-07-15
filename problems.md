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

