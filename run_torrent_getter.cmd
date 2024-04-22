@echo off

rem Activate virtual environment
call D:\UDEMY_Workspace\GITHUB\python-1337x-torrent-downloader\.venv\Scripts\activate.bat

rem Run Python script with command-line argument
python D:\UDEMY_Workspace\GITHUB\python-1337x-torrent-downloader\main.py %1

rem Deactivate virtual environment (optional)
deactivate
