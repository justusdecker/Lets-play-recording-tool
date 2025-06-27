def binpi(text : str) -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input.isdecimal():
        print(text)
        user_input = input('\033[90m\033[3m')
        print('\033[23m\033[39m',end='')
    return int(user_input)
    