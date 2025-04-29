@echo off

:: CHANGE TO THE FOLDER WHERE YOUR SCRIPT LIVES
cd /d "C:\MyProject\SummaryTranslate"

:: SETUP FILE LOCATIONS
echo Running transcription script...
python transcribe1.py ^
  --audio "[Where your audio is]" ^
  --vault "[Where you want .md uploaded]" ^
  --ffmpeg "[where this specific software is installed]"