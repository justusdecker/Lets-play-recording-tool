from pygame import Color

LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARNING = 2
LOG_ERROR = 3
        
def __gvc(id):
    return [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ][id]
    
def __grgb(col,text):
    """ Taste the rainbow """
    col = Color(col)
    return f'\033[38;2;{col.r};{col.g};{col.b}m{text}\033[0m'

def LOG(message: str, variables: list[any] | None = None, logtype: int = 0):
    """
    The pretty way to log your things
    """
    logtype_str = ('DEB','INF','WAR','ERR')[logtype]
    logcolor = ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[logtype]
    output = ''
    var_step = 0
    if variables is not None:
        for idx,word in enumerate(message):
            if word == '$' and var_step <= len(variables) - 1:
                if variables[var_step] is not None:
                    color_picker = [isinstance(variables[var_step], typ) for typ in [int, str, bool, float, dict, tuple, list, bytes]].index(True)
                else:
                    color_picker = 2
                if color_picker == 1:
                    if variables[var_step].startswith('#') and variables[var_step].__len__() == 7:

                        word = __grgb(variables[var_step],variables[var_step])
                        _ = ''
                    else:
                        word = __grgb(__gvc(color_picker),variables[var_step])
                        _ = ''
                else:
                    word = __grgb(__gvc(color_picker),variables[var_step])
                var_step += 1
            elif var_step > len(variables) - 1 and word == '$':
                word = '[NULL]'
            
            output += word
    else:
        output = message

    print(f'[{logcolor}{logtype_str}\033[0m] {output}\033[0m')