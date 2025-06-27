def binpi(text : str, inp: str = '') -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input.isdecimal():
        print(text)
        user_input = input(f'{inp}\033[92m\033[3m')
        print('\033[23m\033[39m',end='')
    return int(user_input)
    