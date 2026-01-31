set dest=%USERPROFILE%\.vscode\extensions\lprtscript\
mkdir %dest%
mkdir %dest%\syntaxes\
copy .\src\api\syntax\lprtscript.json %dest%\syntaxes\schema.tmLanguage.json
copy .\src\api\syntax\package.json %dest%\package.json
