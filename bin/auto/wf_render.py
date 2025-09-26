from bin.data_access import SQLAccess, reoc, isfile, rie, cnef
from bin.constants import TEMP_FOLDER, VIDEO_FOLDER, ERROR_007, AutomationError
from bin.api.ffmpeg import ffmpeg_run, FFMPEG_AUDIO_COMBINE, FFMPEG_VIDEO_RENDER
from bin.wintoasty import toast_finished
from bin.xmsgbox import xerr

from bin.ui.progress_bar_manager import ProgressBarManager

def render(result,app, lpid):
    """
    Currently a workaround. Will be refactored into Compare&Render ASAP - issie #345
    """
    rendering_queue = []
    try:
        ci = 0
        
        pbm = app.pbm
        pbm : ProgressBarManager
        pbm.clean(len(result)*2)
        
        for i, mic, desk, vid, vol in result:
            pbm.increment()
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'
            
            rie(tmp_audio_path)
            
            ffmpeg_run(
                FFMPEG_AUDIO_COMBINE,
                {
                    '__IN1__':mic,
                    '__IN2__': desk,
                    '__VOLUME1__': str(1.0),
                    '__VOLUME2__': str(vol),
                    '__OUT__':tmp_audio_path
                    }
                )
            
            reoc(not isfile(tmp_audio_path),ERROR_007)
            
            #app.progress_label.configure(text = f'Audio Combine\n{((ci+1)/len(result))*100:.1f}%\n{ci+1}/{len(result)}')
            ci += 1
            rendering_queue.append((vid, tmp_audio_path, i))
        toast_finished("[1/2] Audio combine")

        
        
        path_ending = f'_{SQLAccess.read_letsplay_game_name(lpid)}_final.mp4'
        cnef(VIDEO_FOLDER)
        ci = 0
        for video, audio, index in rendering_queue:
            pbm.increment()
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'
            rie(final_path)
            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )
            reoc(not isfile(final_path),ERROR_007)
            #app.progress_label.configure(text = f'Audio Combine\n{((ci+1)/len(result))*100:.1f}%\n{ci+1}/{len(result)}')
            ci += 1
            SQLAccess.update_episode(lpid, index, final_video_path=final_path)
        toast_finished("[2/2] Audio combine")
    except AutomationError as AE:
        xerr(f'Automation Error\n{AE}')
    
    pbm.reset_task()
