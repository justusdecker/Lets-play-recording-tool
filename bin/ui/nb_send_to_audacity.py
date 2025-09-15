from bin.ui.automation_frame import AutomationFrame
from bin.automations import SendToAudacityWF

class Send2Audacity(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = SendToAudacityWF