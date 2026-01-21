<Table@'letsplays'>
    id: Integer, Primary
    tad_path: Text
    name: Text
    game_name: Text
    episode_length: Integer
    description_path: Text
    jitle: Text
    emoji: Text
<Table@'episodes'>
    id: Integer, Primary
    lpid: Integer -> 0
    video_path: Text
    audio_mic_path: Text
    audio_desktop_path: Text
    thumbnail_path: Text
    has_problem: Boolean
    audio_mic_edit_path: Text
    title: Text
    upload_at: Text
    final_video_path: Text