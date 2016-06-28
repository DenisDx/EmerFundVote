rem follow https://kivy.org/docs/guide/packaging-windows.html

rem 1.
rem del EmerFundVoteApp.spec
rem python -m PyInstaller --name EmerFundVoteApp --icon icon.ico main.py
rem python -m PyInstaller --onefile --name EmerFundVoteApp main.py
rem from kivy.deps import sdl2, glew

rem check pyinstaller --onefile file_script.py

rem 2.
rem echo final build...
rem python -m PyInstaller EmerFundVoteApp.spec
rem python -m PyInstaller --onefile EmerFundVoteApp.spec



rem  ==========ONE-FILE
rem 1. python -m PyInstaller --onefile --name EmerFundVoteApp main.py
rem 2. change EmerFundVoteApp.spec
rem 3. python -m PyInstaller EmerFundVoteApp.spec

rem =================
rem del dist /S/Q/F
rem del build /S/Q/F
rd dist /Q/S
rd build /Q/S
del EmerFundVoteApp.spec
rem copy EmerFundVoteApp_win.spec EmerFundVoteApp.spec
copy EmerFundVoteApp_single_exe.spec EmerFundVoteApp.spec
python -m PyInstaller EmerFundVoteApp.spec