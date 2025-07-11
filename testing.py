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

    l = len(data)
    return {i: (data[i] , data[i+1]) for i in range(0,l,2)}
        
    #! Will not see the last one when odd
    
def convert_to_tc(t:float):
    h, m, s = t // 60 // 60,t // 60, t % 60

    h = f'0{h}' if h < 10 else str(h)
    m = f'0{m}' if m < 10 else str(m)
    m = f'0{m}' if m < 10 else str(m)
    return f'{h}:{m}:{s}'
path = "C:\\Users\\Justus\\jri_data\\audio\\1_schedule_one_track_mic.aac"
result = get_silence(path)
print(result)
for key in result:
    print(convert_to_tc(result[key][0]),convert_to_tc(result[key][1]))
    ffmpeg_run(FFPLAY_PLAY_AUDIO,{'__IN__': path,'__SS__': result[key][0],'__TO__': result[key][1]})
    #TODO SOX Command

