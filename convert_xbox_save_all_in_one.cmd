@echo off
title Pylar's Auto Convert Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt


setlocal
:PROMPT
SET /P RunXGP=Do you want to run XGP Extractor (Y/N)?
IF /I "%RunXGP%" NEQ "Y" GOTO END

:: Run the main.py script
python xgp_save_extractor.py

:END
endlocal

:: Run the game_pass_converter.py script
python game_pass_save_fix.py

pause