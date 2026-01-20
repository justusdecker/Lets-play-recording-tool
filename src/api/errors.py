class AutomationError(Exception):
	"""
	If this error is thrown. The user has done some bullshit, in most cases:
    The user forgot to do a earlier automation or deleted some files.
    In rare cases the programmer has done something wrong here!
    This Exception should be catched, so the user can get a simple error message,
    without throwing too much code in between the automations that makes it nearly unreadable.
 	"""
  
def reoc(cond: bool,msg: str) -> None:
    """ raise_error_on_condition """
    if cond: raise AutomationError(msg)