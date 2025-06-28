# Thumbnail Automation Data

This is a default TAD File
---
```
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


### Background
The background is the first index currently you can define only the `fixed` Background position.
> [!NOTE]
> In the future there will be more options!
> Something like random position, rotation etc.
### Logo
The logo is the second index. You can define:
|key|val|
|---|---|
|path|`str`|
|scale|`float` or `int`|
|rot|`float` or `int`|
|pos| `tuple` or `list` cont. `int`|
### Text
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