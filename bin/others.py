__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.117"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

def convert_to_tc(t:float):
    h, m, s = t // 60 // 60,t // 60, t % 60
    h, m, s = int(h), int(m), int(s)
    h = f'0{h}' if h < 10 else str(h)
    m = f'0{m}' if m < 10 else str(m)
    s = f'0{s}' if s < 10 else str(s)
    return f'{h}:{m}:{s}'