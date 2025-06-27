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
    