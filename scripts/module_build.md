# How to build a Module

## Header

```yml
name: Audio Fix
description: Apply audio processing filters to microphone tracks within a defined episode range.
include: |
    data_access        
    ffmpeg_api          
    constants           
    ui_manager         
    core_helpers
```

## Calling a function

```yml
- name: Call
      call: data_access.cnef
```

## Calling a function with a single argument

```yml
- name: Call with Argument
      call: data_access.cnef
      args: $argument
```

## Calling a function with return

```yml
- name: Call with return
      call: data_access.SQLAccess.read_episodes
      args:
        - $lpid
      output: $all_episodes
```

## Calling a function with multiple arguments

```yml
- name: Call with multiple Arguments
      call: ui_manager.pbm_clean
      args:
        - $app.pbm
        - $all_episodes.length
      output: 
            - $ep_start
            - $ep_end
```

## For loops

```yml
- name: A loop
      loop:
        range: 
            - $ep_start
            - $ep_end
      as: i
      steps:
        - name: Call
          call: data_access.cnef
```

## If Statements

```yml
- name: Check 1 Audio Path not null (reoc ERROR_013)
      check:
        expression: '$audio_mic_path == null'
      on_true:
        - call: data_access.reoc_error
          args:
            - $filepath
            - $ERROR_013
```

## Calling a function

```yml

```

## Calling a function

```yml

```