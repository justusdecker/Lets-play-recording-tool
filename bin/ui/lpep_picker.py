from collections.abc import Callable
import tkinter as tk
from bin.constants import ICO_RUN
import tkinter.ttk as ttk
from bin.translation import gtran
from bin.data_access import AsciiImage, SQLAccess
from tools.log import LOG

class LPEPPicker:
    def __init__(self, 
                 parent: tk.Widget,
                 callback: callable,
                 mode: str = 'lp-ep',
                 btn_image: str = ICO_RUN,
                 ch_callback: Callable | None = None):
        """
        .. mode::
            The mode defines the way this class will show the elements of LPEP
            
            The mode syntax is the following: lp-ep-nc-ne
            
            |mode|description|
            |---|---|
            |lp|shows the lets play selecter|
            |ep|shows the episode selector(start,end)|
            |nc|no callback|
            |ne|no end episode selector(one episode selector)|
            |nb|no button|
        """
        
        self.ch_callback = ch_callback
        self.s_lp = 'lp' in mode
        self.s_ep = 'ep' in mode
        self.d_ne = 'ne' in mode
        self.d_nb = 'nb' in mode
            
        self.btn_image = btn_image
        
        self.parent = parent
        self.callback = callback
        self.obj = ttk.LabelFrame(self.parent, text = gtran("bin::ui::lpep_selector_header"))
        self.obj.pack()
        self.values = []
        
        self.v_epstart = tk.IntVar(self.obj,1)
        self.v_epend = tk.IntVar(self.obj,1)
        self.v_epstart.trace_add('write', self.check)
        self.v_epend.trace_add('write', self.check) 
        
        self.v_lp = tk.StringVar(self.obj)
        self.vcmd = self.obj.register(self.val_sp_input)
        self.lp_create_ui()
        self.ep_create_ui()
        self.st_create_ui()
        
    def st_create_ui(self):
        """
        Creates and configures Tkinter UI elements for starting a task.
        """
        if self.d_nb: return
        img = AsciiImage(self.btn_image)
        self.btn_run = ttk.Button(self.obj, image=img.image,command=self.run)
        
        self.btn_run.image = img.image
        if not self.values:
            self.btn_run.state(['disabled'])
        self.btn_run.pack(side='left')
    
    def lp_create_ui(self):
        """
        Creates and configures Tkinter UI elements for selecting a "Let's Play" item.

        This method sets up a label and an option menu (dropdown) for users
        to select from a list of "Let's Play" names. The names are sourced
        from the lprt database.
        When a selection is made, the provided `self.callback` function is executed.
        """
        if not self.s_lp: return
        names = SQLAccess.read_letsplay_names()

        self.lp_label = ttk.Label(self.obj, text ="Lets Play")
        self.options = ttk.OptionMenu(self.obj,self.v_lp,'None' if not self.v_lp.get() else self.v_lp.get(),*names,command=self.lp_changed)
        
        self.lp_label.pack(side='left')
        self.options.pack(side='left')
    
    def ep_create_ui(self):
        """
        Creates and configures Tkinter UI elements for selecting an episode range.

        This method sets up two lab els ("Episode start", "Episode end" <- only if self.both is true!),
        two option menus for selecting start and end episode numbers, and an
        "Run" button. The button is initially disabled(if ft is none <- No data exists) and its state
        can be managed by `self.check`. The `run_callback` is
        executed when the "Run" button is clicked.
        """
        if not self.s_ep: return
        
        self.lbl_start = ttk.Label(self.obj, text = gtran("bin::ui::lpep_selector_start_episode"))

        #self.opm_start = ttk.OptionMenu(self.obj,self.v_epstart,str(self.values[0] if self.values else 'None'),*self.values,command=self.check)
        
        #? New solution
        
        self.opm_start = ttk.Spinbox(
            self.obj, 
            textvariable=self.v_epstart, 
            from_= 1 if self.values else -1,
            to=self.values[-1] if self.values else -1,
            width=4,
            validate='all',
            validatecommand= (self.vcmd, '%P'),
            command=self.check)
        
        
        
        if not self.d_ne: 
            self.lbl_end = ttk.Label(self.obj, text = gtran("bin::ui::lpep_selector_end_episode"))
            self.opm_end = ttk.Spinbox(
                self.obj, 
                textvariable=self.v_epend, 
                from_=self.values[0] if self.values else -1,
                to=self.values[-1] if self.values else -1,
                width=4,
                validate='all',
                validatecommand= (self.vcmd, '%P'),
                command=self.check)
        if self.v_lp.get() == 'None':
            self.opm_start.state(['disabled'])
            if not self.d_ne:
                self.opm_end.state(['disabled'])
        else:
            self.opm_start.state(['!disabled'])
            if not self.d_ne:
                self.opm_end.state(['!disabled'])
        
        self.lbl_start.pack(side='left')
        self.opm_start.pack(side='left')
        if not self.d_ne: 
            self.lbl_end.pack(side='left')
            self.opm_end.pack(side='left')
    
    def val_sp_input(self,P):
        """
        Checks whether the input is a digit or empty.
        The boundary correction takes place in self.check() via the trace/command.
        """
        if P.isdigit() or P == "":
            LOG('Spinbox input "$" is okay',[P])
            return True
        
        LOG('Spinbox input "$" is not okay (non-digit)',[P])
        return False
        
    def check(self,*_):
        """ Checks: b < a. So the start ep cant be greater than the end! """
        
        if self.s_ep:
            self._correct_episode_bounds(self.v_epstart)
            if not self.d_ne:
                self._correct_episode_bounds(self.v_epend)
        
        
        if self.s_ep and not self.d_ne:
            start = LPEPPicker.oro(self.v_epstart)
            end = LPEPPicker.oro(self.v_epend)
            
            self.btn_run.state(['disabled' if end < start else '!disabled'])

        elif self.s_ep and self.d_ne:
            if not self.d_nb and self.values:
                self.btn_run.state(['!disabled'])
            elif not self.d_nb:
                self.btn_run.state(['disabled'])
    
    def reset(self):
        """ resets the ui """
        self.destroy_st()
        self.destroy_lp()
        self.lp_create_ui()
        self.destroy_ep()
        self.ep_create_ui()
        self.st_create_ui()
    
    def destroy_st(self):
        """ destroy the start button """
        if self.d_nb: return
        self.btn_run.destroy()
    
    def destroy_ep(self):
        """ destory the ep selector """
        if not self.s_ep: return
        self.lbl_start.destroy()
        if not self.d_ne: self.lbl_end.destroy()
        self.opm_start.destroy()
        self.opm_end.destroy()
        
    def destroy_lp(self):
        """ destroy the lp selector """
        if not self.s_lp: return
        self.lp_label.destroy()
        self.options.destroy()
        
    def destroy(self):
        """ destory all elements """
        self.obj.destroy()
        self.destroy_lp()
        self.destroy_ep()
        return super().destroy()
    
    @staticmethod
    def oro(var: tk.IntVar):
        """
        'Okay or one' - Attempts to retrieve the value from a tk.IntVar. 
        Returns the value 1 in case of a tk.TclError (e.g., an empty field).
        """
        try: return var.get()
        except tk.TclError: return 1
    
    def _correct_episode_bounds(self, episode_var: tk.IntVar):
        """
        Corrects the value of an episode variable (start or end) 
        so that it lies between 1 and the maximum available episode number.
        """
        max_val = self.values[-1] if self.values else 1
        current_val = LPEPPicker.oro(episode_var)
            
        if current_val > max_val:
            episode_var.set(max_val) # Set to max
        elif current_val < 1:
            episode_var.set(1)       # Set to min
    
    def run(self,*_):
        """ runs the `self.callback` function """
        if self.s_ep:
            if not self.d_ne:
                variables = [self.v_lp.get(),self.v_epstart.get(),self.v_epend.get()]
            else:
                variables = [self.v_lp.get(),self.v_epstart.get()]
        else:
            variables = [self.v_lp.get()]
        LOG('Run - lp: $ eps: $ - $',variables)
        self.callback()
    
    def get_ui(self) -> list[tk.Button]:
        """ Gets all ui elements that need to be blocked """
        _ret = [self.options]
        if not self.d_nb:
            _ret.append(self.btn_run)
        if self.s_ep:
            _ret.append(self.opm_start)
            if not self.d_ne:
                _ret.append(self.opm_end)
        return _ret
    
    def update_ui(self):
        """
        Updates UI elements related to episode range for data deletion.

        Recalculates available episode numbers based on the selected 'Let's Play'
        for the data deletion section.
        """
        lp = self.v_lp.get()
        if lp != 'None':
            self.values = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_names().index(self.v_lp.get())))]
        else:
            self.values = []
    
    def lp_changed(self,*_):
        """
        Callback for changes in the 'Let's Play' selection for data deletion.

        Updates the UI to reflect episode numbers for deletion, re-creates
        episode range selection widgets, and controls the state of the delete button.
        """
        self.update_ui()
        if not self.d_nb:
            LOG("lp changed: i $ myself",['activated' if self.values else 'deactivated'])

            self.btn_run.state(['disabled' if not self.values else '!disabled'])

        
        self.reset()
        if self.ch_callback is not None:
            self.ch_callback()
