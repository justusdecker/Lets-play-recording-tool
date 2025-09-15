import tkinter as tk
import tkinter.ttk as ttk
from bin.data_access import json_read, file_read, isfile, json_write, file_write
from bin.constants import ROOT, DEFAULT_OBS_SETTINGS
from bin.translation import gtran

class Settings(tk.Frame):
    """
    Manages application settings, particularly for OBS (Open Broadcaster Software) integration.

    Provides UI elements for configuring OBS connection details (IP, Port, Password)
    and allows saving these settings to a JSON file.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        self.menu = parent.master
        
        # Create Headers
        SETTINGS = ttk.LabelFrame(W,text=gtran("bin::ui::settings::obs_header"))
        API_GEMINI_SETTINGS = ttk.LabelFrame(W,text=gtran("bin::ui::settings::gemini_header"))
        
        self.IP = tk.StringVar()
        self.PORT = tk.StringVar()
        self.PW = tk.StringVar()
        self.PW_TOGGLE = tk.IntVar()
        
        obs_ip_label = ttk.Label(SETTINGS,text=gtran("bin::ui::settings::obs_ip"))
        self.obs_ip = ttk.Entry(SETTINGS,textvariable=self.IP)
        
        obs_port_label = ttk.Label(SETTINGS,text=gtran("bin::ui::settings::obs_port"))
        self.obs_port = ttk.Entry(SETTINGS,textvariable=self.PORT)
        
        obs_password_label = ttk.Label(SETTINGS,text=gtran("bin::ui::settings::obs_pw"))
        self.obs_password = ttk.Entry(SETTINGS,show='*',textvariable=self.PW)
        
        self.obs_ip.bind('<KeyPress>',self.something_changed)
        self.obs_port.bind('<KeyPress>',self.something_changed)
        self.obs_password.bind('<KeyPress>',self.something_changed)
        
        self.set_settings_obs_btn = ttk.Button(SETTINGS,text=gtran("bin::ui::settings::obs_save_btn"),command=self.set_obs_settings)
        
        self.show_pw = ttk.Checkbutton(SETTINGS,variable=self.PW_TOGGLE,text=gtran("bin::ui::settings::obs_show_pw"),command=self.toggle_pw_view)
        
        obs_ip_label.grid(row=0,column=0)
        self.obs_ip.grid(row=0,column=1)
        obs_port_label.grid(row=1,column=0)
        self.obs_port.grid(row=1,column=1)
        obs_password_label.grid(row=2,column=0)
        self.obs_password.grid(row=2,column=1)
        self.show_pw.grid(row=2,column=2)
        self.set_settings_obs_btn.grid(row=3,column=0)
        
        if isfile(ROOT+'obs_settings.json'):
            OBS_SETTINGS = json_read(ROOT+'obs_settings.json')
            self.IP.set(OBS_SETTINGS['ip'])
            self.PORT.set(OBS_SETTINGS['port'])
            self.PW.set(OBS_SETTINGS['pw'])
        
        
        self.APIKEY = tk.StringVar()
        self.language = tk.StringVar()
        self.PW_TOGGLE_GAPI = tk.IntVar()
        
        lang = ''
        if isfile('.env'):
            try:
                api_key, lang = file_read('.env').splitlines()
                api_key, lang = api_key.split('=')[1][1:-1], lang.split('=')[1][1:-1]
                self.APIKEY.set(api_key)
                self.language.set(lang)
            except:
                pass
        
        languages = ['german', 'english', 'dutch']
        
        api_key_label = ttk.Label(API_GEMINI_SETTINGS,text=gtran("bin::ui::settings::gemini_key"))
        self.api_key = ttk.Entry(API_GEMINI_SETTINGS,textvariable=self.APIKEY,show='*')
        self.show_pw_gapi = ttk.Checkbutton(API_GEMINI_SETTINGS,variable=self.PW_TOGGLE_GAPI,text=gtran("bin::ui::settings::gemini_show_pw"),command=self.toggle_pw_view)
        language_options = ttk.OptionMenu(API_GEMINI_SETTINGS,self.language,lang,*languages)
        self.set_settings_api_key = ttk.Button(API_GEMINI_SETTINGS,text=gtran("bin::ui::settings::gemini_save_btn"),command=self.set_api_settings)
        self.api_key.bind('<KeyPress>',self.something_changed)
        
        api_key_label.grid(row=0,column=0)
        self.api_key.grid(row=0,column=1)
        self.show_pw_gapi.grid(row=0,column=2)
        language_options.grid(row=1,column=0)
        self.set_settings_api_key.grid(row=1,column=1)
        
        # Packing
        SETTINGS.pack()
        API_GEMINI_SETTINGS.pack()

        W.pack()
        self.something_changed()
        
    def toggle_pw_view(self,*args):
        """ Toggles the visibility of the password in the OBS password entry field. """
        if self.PW_TOGGLE.get():
            self.obs_password.configure(show="")
        else:
            self.obs_password.configure(show="*")
        if self.PW_TOGGLE_GAPI.get():
            self.api_key.configure(show="")
        else:
            self.api_key.configure(show="*")
    
    def something_changed(self,*args):
        """
        Callback for changes in OBS setting input fields.

        Enables or disables the 'Set' button based on whether all OBS
        connection details (IP, Port, Password) are filled.
        """
        if self.PW.get() and self.PORT.get() and self.IP.get():
            self.set_settings_obs_btn.state(['!disabled'])
        else:
            self.set_settings_obs_btn.state(['disabled'])
            
        if self.api_key.get():
            self.set_settings_api_key.state(['!disabled'])
        else:
            self.set_settings_api_key.state(['disabled'])
            
    def set_obs_settings(self,*args):
        """ Saves the current OBS connection settings to a JSON file. """
        
        NEW_OBS_SETTINGS = {key: DEFAULT_OBS_SETTINGS[key] for key in DEFAULT_OBS_SETTINGS}
        NEW_OBS_SETTINGS['ip'] = self.IP.get()
        NEW_OBS_SETTINGS['port'] = self.PORT.get()
        NEW_OBS_SETTINGS['pw'] = self.PW.get()
        json_write(ROOT+'obs_settings.json',NEW_OBS_SETTINGS)
    
    def set_api_settings(self,*args):
        """ Saves the current OBS connection settings to a JSON file. """
        
        file_write('.env',f'GOOGLE_API_KEY=\"{self.APIKEY.get()}\"\nLANG=\"{self.language.get()}\"')
