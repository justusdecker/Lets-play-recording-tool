:: Takes the main.spec file & compiles the project into onefile
:: Upside: Simple to use
:: Downside: The Windows Defender nukes the zip! 
pyinstaller main.spec
python zipit.py
pause 2>NUL