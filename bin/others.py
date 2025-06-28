from bin.text_manipulation import err, bold
from bin.constants import COPYRIGHT, header, USER_INPUT_NUM_UNMATCHED

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
    
def input_episode_range(max_eps:list[int], lp_names: list[str]):
    # SET LP
    listed_lets_plays = "\n".join([f"({idx}) {lp}" for idx, lp in enumerate(lp_names)])
    
    lp_id = binpi(f"{header('tg',['Set Lets Play'])}{listed_lets_plays}")
    
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
    RANGE_START = header('tg',['Set RANGE START']) + f'{max_eps[lp_id]}'
    RANGE_END = header('tg',['Set RANGE END']) + f'{max_eps[lp_id]}'
    RANGE_END = header('tg',['Set Index']) + f'{max_eps[lp_id]}'
    match binpi(MODE_SET):
        case 1:
            ep_range = (0,max_eps[lp_id]-1)
        case 2:
            _start = binpi(RANGE_START)
            _end = binpi(RANGE_END + f'\nMust be greater or equal {_start}')
            if _start > _end:
                err('Input out of range')
                return
            ep_range = (_start, _end)
        case 3:
            _index = binpi(RANGE_START)
            ep_range = (_index,_index)
        case _:
            err(USER_INPUT_NUM_UNMATCHED)
    return lp_id, ep_range