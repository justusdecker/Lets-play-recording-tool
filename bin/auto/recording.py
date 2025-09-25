from bin.data_access import SQLAccess
from bin.api.obs import OBSObserver
from time import sleep
from tools.log import LOG, LOG_ERROR
from bin.translation import gtran
def obs_rec_label_set(OBSO, el,reset:bool = False):
    """
    Sets the recording label color
    """
    if reset:
        el.recording_information_label.configure(foreground='black')
        return
    epl = SQLAccess.read_episode_length(SQLAccess.read_letsplay_names().index(el.lpep_picker.v_lp.get()))
    
    if epl is None:
        el.recording_information_label.configure(foreground='black')
        return
    
    if OBSO.time_in_seconds >= epl:
        el.recording_information_label.configure(foreground='red')
        return
    elif OBSO.time_in_seconds + 30 >= epl:
        el.recording_information_label.configure(foreground='orange')
        return
    else:
        el.recording_information_label.configure(foreground='green')

def obs_connect(el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up. See issue #244
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        obs_rec_label_set(OBSO,el, True)
        el.btn_connect.configure(text= gtran("bin::auto::recording::settings_not_exist"))
        return
    if not OBSO.isconnected:
        obs_rec_label_set(OBSO,el, True)
        el.btn_connect.configure(text= gtran("bin::auto::recording::no_connection"))
        return
    el.btn_connect.configure(text= gtran("bin::auto::recording::disconnect"))
    el.btn_connect.state(["!disabled"])
    while OBSO.isconnected:
        if el.close_connection:
            OBSO.client.disconnect()
            el.btn_connect.configure(text= gtran("bin::auto::recording::connection_closed"))
            return
        try:
            id = SQLAccess.read_letsplay_names().index(el.lpep_picker.v_lp.get())
            if OBSO.time_in_seconds:
                el.recording_information_label.configure(text= f'{gtran("bin::auto::recording::recording_text")} - {SQLAccess.read_episode_ammount(id)} {gtran("bin::auto::recording::episodes_text")}\n{OBSO.timecode.split(".")[0]}')
                obs_rec_label_set(OBSO,el)
            else:
                obs_rec_label_set(OBSO,el, True)
                el.recording_information_label.configure(text= f'{gtran("bin::auto::recording::waiting_text")} - {SQLAccess.read_episode_ammount(id)} {gtran("bin::auto::recording::episodes_text")}')
            OBSO.update(id)
        except Exception as E:
            obs_rec_label_set(OBSO,el, True)
            el.btn_connect.configure(text= gtran("bin::auto::recording::unexpected_error"))
            LOG(f'Unexpected Error happened [{E}]',logtype=LOG_ERROR)
        sleep(0.3)