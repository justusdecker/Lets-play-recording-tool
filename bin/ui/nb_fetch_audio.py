from bin.ui.automation_frame import AutomationFrame
from bin.auto.wf_fetch_audio import ExtractAudioWF
 
class FetchAudio(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = ExtractAudioWF
