from bin.ui.automation_frame import AutomationFrame
from bin.automations import ExtractAudioWF
 
class FetchAudio(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = ExtractAudioWF
