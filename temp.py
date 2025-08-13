import tkinter as tk
from tkinter import ttk
from threading import Thread
# Annahme: Deine AutomationFrame-Klasse und Hilfsfunktionen wie
# get_menu, get_lets_play, get_episode_range, SQLAccess, change_states
# sind bereits definiert.

# Deine AutomationFrame-Klasse
# class AutomationFrame(tk.Frame):
#     ...

class FixAudio(AutomationFrame):
    def __init__(self, parent, controller):

        # --- UI-Elemente für die Audiofilter ---
        audio_filters_frame = ttk.Frame(self.THUMBNAIL_AUTOMATION)
        audio_filters_frame.pack(pady=10)

        # Highpass Filter
        hp_frame = ttk.LabelFrame(audio_filters_frame, text="High-Pass Filter")
        hp_frame.pack(fill='x', padx=5, pady=5)
        
        self.hp_enabled = tk.BooleanVar(value=False)
        self.hp_freq = tk.DoubleVar(value=175.0)
        
        ttk.Checkbutton(hp_frame, text="Aktivieren", variable=self.hp_enabled).grid(row=0, column=0, sticky='w')
        ttk.Label(hp_frame, text="Frequenz (Hz):").grid(row=0, column=1, sticky='w')
        ttk.Spinbox(
            hp_frame,
            from_=20.0,
            to=5000.0,
            increment=1.0,
            textvariable=self.hp_freq,
            width=8
        ).grid(row=0, column=2, sticky='w')

        # Lowpass Filter
        lp_frame = ttk.LabelFrame(audio_filters_frame, text="Low-Pass Filter")
        lp_frame.pack(fill='x', padx=5, pady=5)
        
        self.lp_enabled = tk.BooleanVar(value=False)
        self.lp_freq = tk.DoubleVar(value=13000.0)
        
        ttk.Checkbutton(lp_frame, text="Aktivieren", variable=self.lp_enabled).grid(row=0, column=0, sticky='w')
        ttk.Label(lp_frame, text="Frequenz (Hz):").grid(row=0, column=1, sticky='w')
        ttk.Spinbox(
            lp_frame,
            from_=500.0,
            to=20000.0,
            increment=100.0,
            textvariable=self.lp_freq,
            width=8
        ).grid(row=0, column=2, sticky='w')

        # Loudness Normalization
        ln_frame = ttk.LabelFrame(audio_filters_frame, text="Loudness Normalization")
        ln_frame.pack(fill='x', padx=5, pady=5)
        
        self.ln_enabled = tk.BooleanVar(value=True)
        self.ln_i = tk.DoubleVar(value=-15.0)
        self.ln_tp = tk.DoubleVar(value=-1.5)
        self.ln_lra = tk.DoubleVar(value=11.0)
        
        ttk.Checkbutton(ln_frame, text="Aktivieren", variable=self.ln_enabled).grid(row=0, column=0, sticky='w', columnspan=2)
        
        ttk.Label(ln_frame, text="Integrated (LUFS):").grid(row=1, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=-24.0,
            to=-10.0,
            increment=0.5,
            textvariable=self.ln_i,
            width=6
        ).grid(row=1, column=1, sticky='w')

        ttk.Label(ln_frame, text="True Peak (dBTP):").grid(row=2, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=-6.0,
            to=0.0,
            increment=0.1,
            textvariable=self.ln_tp,
            width=6
        ).grid(row=2, column=1, sticky='w')

        ttk.Label(ln_frame, text="Loudness Range (LU):").grid(row=3, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=1.0,
            to=20.0,
            increment=1.0,
            textvariable=self.ln_lra,
            width=6
        ).grid(row=3, column=1, sticky='w')

    def get_ffmpeg_audio_filter_string(self):
        """Erstellt den FFmpeg-Audiofilter-String basierend auf den UI-Einstellungen."""
        filters = []
        
        # Highpass Filter
        if self.hp_enabled.get():
            filters.append(f"highpass=f={self.hp_freq.get()}")
            
        # Lowpass Filter
        if self.lp_enabled.get():
            filters.append(f"lowpass=f={self.lp_freq.get()}")

        # Loudness Normalization
        if self.ln_enabled.get():
            filters.append(f"loudnorm=I={self.ln_i.get()}:TP={self.ln_tp.get()}:LRA={self.ln_lra.get()}")
            
        print(",".join(filters))