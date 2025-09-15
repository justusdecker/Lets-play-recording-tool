import tkinter as tk
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import tkinter.messagebox as msgbox

#! NOT FINISHED

class TBO:
    """
    A helper class for creating and managing Tkinter UI elements (Tkinter Binding Object).

    This class simplifies the creation of various Tkinter widgets (Buttons, LabeledScales,
    Entries, Checkbuttons) and binds them to Tkinter variables. It includes validation
    logic based on specified conditions (e.g., numeric ranges, non-null strings).
    """
    def __init__(self,
                 master,
                 key: str,
                 type: tk.IntVar | tk.StringVar | tk.DoubleVar, 
                 uie: ttk.Button | ttk.LabeledScale | ttk.Entry | ttk.Checkbutton, 
                 cond: str, 
                 command:bool=askopenfilename):
        self.command = command
        # cond: <62::>51 if int or double
        # cond: notnull if str
        self.master = master
        self.key: str = key
        self.type: tk.IntVar | tk.StringVar | tk.DoubleVar = type
        
        self.uie: ttk.Button | ttk.Spinbox | ttk.Entry | ttk.Checkbutton = uie

        self.var: tk.IntVar | tk.StringVar | tk.DoubleVar = self.type()
        self.cond = cond
        self.create_ui()
    
    def create_ui(self):
        """
        Creates the Tkinter UI element based on the `uie` type and packs it.

        Also binds validation checks for Entry widgets.
        """
        f = tk.Frame(self.master)
        if self.uie is ttk.Spinbox:
            ttk.Label(f,text='-'.join(self.key.split('::')[1:])).grid(column=0, sticky='w')
            
            self.ui = self.uie(f,from_=self.condition[0][1:],to=self.condition[1][1:],textvariable=self.var,width=8,increment=0.1 if self.type is tk.DoubleVar else 1.0)
        elif self.uie is ttk.Entry:
            ttk.Label(f,text=f'{self.name}:').grid(column=0, sticky='w')
            self.ui = self.uie(f,textvariable=self.var)
            self.ui.bind('<KeyRelease>',self.check)
        elif self.uie is ttk.Checkbutton:
            self.ui = self.uie(f,variable=self.var,text=self.name)
        elif self.uie is ttk.Button:
            self.ui = self.uie(f,text=self.name,command=self.btn_cb)
        self.ui.grid(column=1,row=0, sticky='w')
        f.pack()
    
    @property
    def name(self) -> str:
        """ Extracts and returns the display name for the UI element from its key. """
        return self.key.split('::')[-1]
    
    @property
    def condition(self) -> tuple[str,str]:
        """
        Parses and returns the validation conditions.

        Raises:
            ValueError: If the condition string syntax is invalid for the variable type.
        """
        if self.type is tk.IntVar or self.type is tk.DoubleVar:
            cond = self.cond.split('::')
            if len(cond) != 2:
                raise ValueError(f'Length must be 2! {cond}')
            if (not cond[0].startswith('>') and not cond[0].startswith('<')) or (not cond[1].startswith('>') and not cond[1].startswith('<')):
                raise ValueError(f'Wrong Syntax! Should be < or > at the start! {cond}')
        elif self.type is tk.StringVar:
            cond = self.cond
            if cond != '' and cond != 'notnull':
                raise ValueError(f'Wrong condition should be empty or notnull. Not {cond}')
        return cond
    
    def btn_cb(self,*args):
        """
        Callback for button clicks, executing the assigned command.

        Updates the associated Tkinter variable with the command's result and
        then performs a validation check.
        """
        if self.command is askopenfilename:
            self.var.set(self.command())
        elif self.command is askcolor:
            self.var.set(self.command()[1])
        self.check()
        print(self.var.get())
        
    def _check_numeric(self,cond) -> bool:
        """
        Internal helper to check numeric values against a condition.
        """
        if cond.startswith('<'):
            return float(cond[1:]) <= self.get_value()
        elif cond.startswith('>'):
            return float(cond[1:]) >= self.get_value()
        
    def _check_text(self,cond) -> bool:
        """ Internal helper to check string values against a condition. """
        if cond == 'notnull':
            if not self.get_value():
                msgbox.showwarning('WARN','This input is flagged as notnull!')
            return not self.get_value()
        
    def get_value(self):
        """ Safely retrieves the current value from the associated Tkinter variable.

        Handles potential `ValueError` during initial retrieval for numeric types
        by setting a default. """
        try:
            return self.var.get()
        except:
            self.var.set(self.condition[0][1:])
            return self.var.get()
    
    def check(self,*args):
        """
        Performs validation checks on the UI element's value based on its type and conditions.
        Adjusts the variable's value if it falls outside the specified numeric range.
        """
        if self.type is tk.IntVar or self.type is tk.DoubleVar:
            if self._check_numeric(self.condition[0]):
                self.var.set(self.condition[0][1:])
            elif self._check_numeric(self.condition[1]):
                self.var.set(self.condition[1][1:])
        else:
            self._check_text(self.condition)
                
    def set_name(self,name: str):
        """
        Sets the display name of the UI element.

        Args:
            name (str): The new display name.
        """
        self.name = name
 
class TadEditor(tk.Frame):
    """
    Provides a graphical user interface for editing Thumbnail Automation Data (TAD) files.

    This editor allows users to configure various aspects of thumbnail generation,
    including background properties, logo placement and scaling, and text appearance.
    It integrates with 'Let's Play' selection and allows saving configurations
    and previewing generated thumbnails.
    """
    names = [
            {
                "pos": ['x','y'],
                "r_pos": [['x-from','x-to'],['y-from','y-to']],
                "r_scale": ['from','to'],
                "r_rot": ['from','to'],
                "center": None,
                "scale": None,
                "rot": None
            },
            {
                "path": None,
                "scale": None,
                "rot": None,
                "pos": ['x','y'],
                "center": None
            },
            {
                "path": None,
                "scale": None,
                "rot": None,
                "color": ['R','G','B','A'],
                "ol_color": ['R','G','B','A'],
                "size": None,
                "pos": ['x','y'],
                "center": None
            }

        ]
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        self.tg = ThumbnailGenerator()
        
        #W = ttk.Frame(self)
        W = tk.Frame(parent)
        self.menu = parent.master
        
        # Create Headers
        TAD_EDITOR = ttk.Frame(W)
        tad_editor_header = ttk.Label(W,text='TAD Editor',font=Font(W,size=16))
        
        OPTIONS = tk.Frame(W)
        OPTIONS.pack()
        LETSPLAY = ttk.LabelFrame(OPTIONS,text='Lets Play')
        
        BACKGROUND = ttk.LabelFrame(OPTIONS,text='Background')
        
        LOGO = ttk.LabelFrame(OPTIONS,text='Logo')

        TEXT = ttk.LabelFrame(OPTIONS,text='Text')
        
        SAVE = ttk.LabelFrame(OPTIONS,text='Save')
        
        PREVIEW = ttk.LabelFrame(W,text='Preview')
        PREVIEW.pack()
        self.tw = ThumbnailPreview(PREVIEW)
        self.lpep_picker = LPEPPicker(LETSPLAY,None,'lp-nb',ch_callback=self.lp_changed)
        
        self.tbos = []
        self.ui_elements = []
        for cheader, HEADER in zip(['bg','logo','text'],[BACKGROUND,LOGO,TEXT]):
            
            self.ui_elements.extend([TBO(HEADER,tbo,*FDS_TBO[inps]) for inps, tbo in zip(FDS_TBO,DEFAULT_TAD) if cheader == tbo.split('::')[0]])
        
        change_states([ui.ui for ui in self.ui_elements],'disabled')
        # Vartype | UIE | (from, to) or None

        # Packing
        #tad_editor_header.grid(row=0,column=1,pady=10,sticky='N')
        #TAD_EDITOR.grid(row=1,column=0,sticky='N')
        
        LETSPLAY.grid(row=0,column=0,sticky='N')
        
        BACKGROUND.grid(row=0,column=1,sticky='N')
        
        LOGO.grid(row=0,column=2,sticky='N')
        
        TEXT.grid(row=0,column=3,sticky='N')
        
        self.save_btn = ttk.Button(SAVE,text='save',command=self.save_tad)
        self.save_btn.grid(row=0,column=5)
        
        SAVE.grid(row=0,column=4,sticky='N')
        self.save_btn.state(['disabled'])
        
        W.pack()

    def set_logo_path(self,*args):
        """
        Opens a file dialog for selecting a logo image file (.png).

        Validates the selected file type and updates the corresponding
        Tkinter variable for the logo path. Shows error messages for
        invalid selections.
        """
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.png'):
            self.get_strings()[0].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
        
    def set_font_path(self,*args):
        """
        Opens a file dialog for selecting a font file (.ttf or .otf).

        Validates the selected file type and updates the corresponding
        Tkinter variable for the font path. Shows error messages for
        invalid selections.
        """
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.ttf') or filepath.endswith('.otf'):
            self.get_strings()[1].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
    
    def lp_changed(self,*args):
        """
        Callback for changes in the 'Let's Play' selection in the editor.

        Enables/disables UI elements, loads existing TAD data for the selected
        'Let's Play' (if available), or sets default values.
        """
        if self.lpep_picker.v_lp.get() != 'None':
            self.save_btn.state(['!disabled'])
            change_states([ui.ui for ui in self.ui_elements],'!disabled')
            lpid = SQLAccess.read_letsplay_by_option_var(self)
            filepath = SQLAccess.read_tad_path(lpid)
            
            #! No JSONDecodError catch
            #! No wrong type catch[case: only if user change the data outside of lprt!]
            if filepath is None:
                [ui.var.set(DEFAULT_TAD[entry]) for entry, ui in zip(DEFAULT_TAD,self.ui_elements)]
                return
            if isfile(filepath):
                DATA = json_read(filepath)
                [ui.var.set(DATA[entry]) for entry, ui in zip(DATA,self.ui_elements)]
            else:
                [ui.var.set(DEFAULT_TAD[entry]) for entry, ui in zip(DEFAULT_TAD,self.ui_elements)]
            
    def save_tad(self,*args):
        """
        Saves the current TAD settings to a JSON file and generates a preview thumbnail.

        Gathers data from UI elements, writes it to a `.json` file in the TAD_FOLDER,
        updates the database with the TAD file path, and generates a preview image
        which is then displayed in a `ThumbnailPreview` window.
        """
        #- Check final
        #- Write TAD File into TAD_FOLDER/lp_name.json
        DATA = {key: ui.var.get() for ui, key in zip(self.ui_elements, DEFAULT_TAD)}
        lpid = SQLAccess.read_letsplay_by_option_var(self)
        lpname = SQLAccess.read_letsplay_name(lpid)
        filepath = f'{lpname}.json'
        json_write(f'{TAD_FOLDER}{filepath}',DATA)
        print(DATA)
        #- Update Database
        SQLAccess.update_tadpath(lpid, filepath)
        
        self.tg.generate(
            '123',
            None,
            SQLAccess.read_tad_path(lpid),
            f'{TEMP_FOLDER}preview.png'
        )
        
        self.tw.update_image(f'{TEMP_FOLDER}preview.png',None)
