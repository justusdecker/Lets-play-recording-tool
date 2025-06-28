from bin.text_manipulation import err, bold
from bin.constants import COPYRIGHT, header

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
    HEADER = f"""
{COPYRIGHT}    
    
{bold(f'Main > Automation > Thumbnail Generator > Select LP')}

Select your Option:
    """
    
    listed_lets_plays = "\n".join([f"({idx}) {lp}" for idx, lp in enumerate(lp_names)])
    lp_id = binpi(f'Select Lets Play ID: \n {listed_lets_plays}')
    if lp_id < len(lp_names):
        err('Input out of range')
        return
    f"""
    Select Option:
    """
    binpi()
    lp_id = binpi(f'Select Lets Play ID: \n {listed_lets_plays}')