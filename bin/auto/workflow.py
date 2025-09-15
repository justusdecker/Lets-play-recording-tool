from bin.data_access import SQLAccess
from bin.wintoasty import toast_finished

class GenericWorkFlow:
    """
    This class serves as a base for workflows, 
    ---
    Inheriting from this class will provide you:
    .. rng:: This gives you the effective episode range as a tuple (start, end).
    .. user_workflow:: shows a toast notification
    .. auto_create_folder_path:: You can create this folder with the `cnef` function.
    .. lpid:: Lets Play Index
    .. finished_message:: The message that will be displayed in user_workflow.
    .. lp_name:: The Lets Play Name
    """
    def __init__(self, folder: str, finish_message: str,lpid,epr):

        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.lpid,self.epr = lpid,epr
        self.lp_name = SQLAccess.read_letsplay_name(self.lpid)

    @property
    def rng(self) -> tuple[int,int]:
        """
        Returns the effective episode range as a tuple (start, end).

        The end of the range is inclusive. If the start and end episodes
        in `epr` are the same, the end of the returned range is incremented by 1
        to ensure a valid range for iteration (e.g., (5,5) becomes (5,6)).

        Returns:
            tuple[int, int]: A tuple representing the (start_episode, end_episode)
                             for the workflow.
        """
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
    def user_workflow(self):
        """
        Executes the primary user-facing part of the workflow.

        This method currently triggers a 'toast' notification indicating
        the workflow has finished, using the provided `finish_message`
        """
        toast_finished(self.finish_message)
    
class OverhauledWorkFlow:
    def __init__(self, folder: str, finish_message: str,lpid,epr):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.lpid,self.epr = lpid,epr
        self.lp_name = SQLAccess.read_letsplay_name(self.lpid)
    @property
    def rng(self) -> tuple[int,int]:
        """
        Returns the effective episode range as a tuple (start, end).

        The end of the range is inclusive. If the start and end episodes
        in `epr` are the same, the end of the returned range is incremented by 1
        to ensure a valid range for iteration (e.g., (5,5) becomes (5,6)).

        Returns:
            tuple[int, int]: A tuple representing the (start_episode, end_episode)
                             for the workflow.
        """
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
    def user_workflow(self):
        """
        Executes the primary user-facing part of the workflow.

        This method currently triggers a 'toast' notification indicating
        the workflow has finished, using the provided `finish_message`
        """
        toast_finished(self.finish_message)