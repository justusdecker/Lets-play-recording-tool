from bin.text_manipulation import err, bold
from bin.constants import COPYRIGHT, header,ERROR_003

def binpi(text : str, inp: str = '') -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input.isdecimal():
        print(text, end='')
        user_input = input(f'{inp}\033[92m\033[3m')
        print('\033[23m\033[39m',end='')
    return int(user_input)

def binps(text : str, inp: str = '') -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input:
        print(text, end='')
        user_input = input(f'{inp}\033[92m\033[3m')
        print('\033[23m\033[39m',end='')
    return user_input
    
def input_episode_range(max_eps:list[int], lp_names: list[str]) -> None | tuple[int, tuple[int, int]]:
    
    if len(max_eps) != len(lp_names):
        err('ValueError')
        return
    # SET LP
    listed_lets_plays = "\n".join([f"({idx}) {lp}" for idx, lp in enumerate(lp_names)])
    
    lp_id = binpi(f"{header('tg',['Set Lets Play'])}{listed_lets_plays}\n")
    
    if lp_id >= len(lp_names):
        err('Input out of range')
        return
    
    
    # SET MODE
    MODE_SET = f"""
{header('tg',['Set MODE'])}
(1) all
(2) in range
(3) one
    """
    RANGE_START = header('tg',['Set RANGE START']) + f'0 - {max_eps[lp_id]-1}\n'
    RANGE_END = header('tg',['Set RANGE END']) + f'0 - {max_eps[lp_id]-1}\n'
    RANGE_ONE = header('tg',['Set Index']) + f'0 - {max_eps[lp_id]-1}\n'
    match binpi(MODE_SET):
        case 1:
            ep_range = (0,max_eps[lp_id])
        case 2:
            _start = binpi(RANGE_START)
            if _start >= max_eps[lp_id]:
                err('Input out of range')
                return
            _end = binpi(RANGE_END + f'\n{_start} - {max_eps[lp_id]-1}\n')
            if _end >= max_eps[lp_id]:
                err('Input out of range')
                return
            if _start > _end:
                err('Input out of range')
                return
            ep_range = (_start, _end+1)
        case 3:
            _index = binpi(RANGE_ONE)
            ep_range = (_index,_index)
        case _:
            err(ERROR_003)
    return lp_id, ep_range