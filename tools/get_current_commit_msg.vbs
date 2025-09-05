'--------------------------------------------------------------------------------------------------
' This script prompts the user for a commit message and saves it to a file.
'
' The user is presented with a dialog box to enter a commit message.
' - If the input is left empty, the string "NULL" is used as the message.
' - The script then creates or overwrites the file "cm.i" in the current directory.
'
' This file serves as a temporary storage for the commit message, to be read
' and used by a separate process (e.g., a Python script).
'--------------------------------------------------------------------------------------------------
commit_msg = InputBox("Leaving it empty will set the commit message to NULL","Your commit Message")
if f = "" Then
    f = "NULL"
End If

' File Interaction
commit_msg_path = "./tools/cm.i"
Set FSO = CreateObject("Scripting.FileSystemObject")
Set objFile = FSO.CreateTextFile(commit_msg_path, True)
objFile.Write commit_msg
objFile.Close