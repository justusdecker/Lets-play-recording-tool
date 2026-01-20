import win32gui
import win32con
import win32api
import uuid
class ToastIcon:
    ERROR = win32gui.NIIF_ERROR
    INFO = win32gui.NIIF_INFO
    WARNING = win32gui.NIIF_WARNING

class ToastMessager:
    """
    Use this by instanciate this once!
    
    After that use the show method:
        It used the title, message & from the ToastIcon Class the Icon.
    """
    def __init__(self):
        self.class_name = f"LPRTToast_{uuid.uuid4().hex}"
        
        wc = win32gui.WNDCLASS()
        self.hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self.class_name
        
        wc.lpfnWndProc = self.__wnd_proc 
        
        try:
            self.class_atom = win32gui.RegisterClass(wc)
        except Exception as e:
            print(f"Class registration failed: {e}")

    def __wnd_proc(self, hwnd, msg, wparam, lparam) -> int:
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0  # LRESULT Success
        # Failed Messages must be send to DefWindowProc
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def show(self, title: str, message: str, icon: int = ToastIcon.INFO):
        hwnd = win32gui.CreateWindow(
            self.class_name, 
            "ToastWindow", 
            win32con.WS_OVERLAPPED,
            0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0, self.hinst, None
        )
        
        win32gui.UpdateWindow(hwnd)
        
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO
        nid = (
            hwnd,                          # Window Handle
            0,                             # ID
            flags,                         # Configuration-Flags
            win32con.WM_USER + 20,         # Callback Message
            hicon,                         # Icon Handle
            "Python Tooltip",              # Hover-Text
            message,                       # Textcontent
            10,                            # Timeout
            title,                         # Title
            icon                           # Icon-Type (Info)
        )
        
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)