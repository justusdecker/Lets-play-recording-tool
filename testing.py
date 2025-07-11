from bin.constants import *

def get_silence(filepath: str,silence: int = -36, duration: float = 0.5) -> list[str]:
    

    result = ffmpeg_run(FFMPEG_GET_SILENCE,{'__IN__':filepath, '__DUR__': duration, '__SIL__': silence})
    data = []
    for idx,line in enumerate(str(result.stderr).split('\n')):
        line: str     
        if line.startswith('[silencedetect'):
            args = line.split(']')[1].split(' ')
            if idx % 2 == 0:
                data.append(float(args[2]))

            else:
                data.append(float(args[2]))
            #print(data[-1])
    l = len(data)
    return {i: (data[i] , data[i+1]) for i in range(0,l,2)}
        
    #! Will not see the last one when odd
path = "C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_track_mic.aac"
result = get_silence(path)
print(result)
for key in result:
    
    ffmpeg_run(FFPLAY_PLAY_AUDIO,{'__IN__': path,'__SS__': result['start'],'__TO__': result['end']})
    #TODO SOX Command

