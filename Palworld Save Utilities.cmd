:: Hide Command and Set Scope
@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: Customize Window
title Palworld Save Utilities
echo Setting up your environment!

:: Create the LocalWorldSave folder
if not exist "LocalWorldSave" (
	mkdir "LocalWorldSave"
	mkdir "LocalWorldSave/Players"
	echo LocalWorldSave folder and its subdirectories have been created.
)

:: Create the DedicatedServerSave folder
if not exist "DedicatedServerSave" (
	mkdir "DedicatedServerSave"
	mkdir "DedicatedServerSave/Players"
	echo DedicatedServerSave folder and its subdirectories have been created.
)

:: Create the GamePassSave folder
if not exist "GamePassSave" (
	mkdir "GamePassSave"
	echo GamePassSave folder has been created.
)

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Menu Name
set strName[1]=Convert Level.sav file to Level.json
set strName[2]=Convert Level.json file back to Level.sav
set strName[3]=Convert Player files to the json file format
set strName[4]=Convert Player files back to sav file format
set strName[5]=Convert Game Pass Save to Steam Save
set strName[6]=Convert Steam Save to Game Pass Save
set strName[7]=Modify your Palworld Save file
set strName[8]=Scan/Repair Save file
set strName[9]=Generate a Image of your Palworld World Save
set strName[10]=Fix Host Save (Convert host save to regular save and vice versa)
set strName[11]=Transfer Character(Server to Server)
set strName[12]=Convert Steam ID to two different Save IDs
set strName[13]=Convert coordinates from in-game to the system in .sav files and vice versa
set strName[14]=Delete Inactive Players Saves
set strName[15]=Delete NoSteam Player Saves
set strName[16]=Delete Steam Player Savess
set strName[17]=Delete Players by Pals amount
set strName[18]=Generate Palguard killnearestbase Commands (Server Required)
set strName[19]=Clean up generated files
set strName[20]=Palworld Save Utilities Package Manager
set strName[21]=Update Palworld Save Utilities
set strName[22]=About Palworld Save Utilities
set strName[23]=Exit Palworld Save Utilities

:: Menu Options
set "strRequest[1]=%strName[1]%"
set "strRequest[2]=%strName[2]%"
set "strRequest[3]=%strName[3]%"
set "strRequest[4]=%strName[4]%"
set "strRequest[5]=%strName[5]%"
set "strRequest[6]=%strName[6]%"
set "strRequest[7]=%strName[7]%"
set "strRequest[8]=%strName[8]%"
set "strRequest[9]=%strName[9]%"
set "strRequest[10]=%strName[10]%"
set "strRequest[11]=%strName[11]%"
set "strRequest[12]=%strName[12]%"
set "strRequest[13]=%strName[13]%"
set "strRequest[14]=%strName[14]%"
set "strRequest[15]=%strName[15]%" 
set "strRequest[16]=%strName[16]%"
set "strRequest[17]=%strName[17]%"
set "strRequest[18]=%strName[18]%"
set "strRequest[19]=%strName[19]%"
set "strRequest[20]=%strName[20]%"
set "strRequest[21]=%strName[21]%"
set "strRequest[22]=%strName[22]%"
set "strRequest[23]=%strName[23]%"

:: Display the Menu
set "Message="
:objMenu
title Palworld Save Utilities
cls
echo.%Message%
echo.
echo.  Palworld Save Utilities Version 1.1.3 (Working as of v0.4.13 Patch) 
echo.       WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!
echo.
set "intMenuCounter=0"
:objMenuLoop
if %intMenuCounter% == 0 (
	echo ==================================================================================
	echo   Save Converting Tools
	echo ==================================================================================
)
set /a "intMenuCounter+=1"
if defined strRequest[%intMenuCounter%] (
    call echo   %intMenuCounter%. %%strRequest[%intMenuCounter%]%%
	if %intMenuCounter% == 6 (
		echo ==================================================================================
		echo   Save Managment Tools
		echo ==================================================================================
	)
		if %intMenuCounter% == 13 (
		echo ==================================================================================
		echo   Save Cleaning Tools
		echo ==================================================================================
	)
		if %intMenuCounter% == 18 (
		echo ==================================================================================
		echo   Program Managment
		echo ==================================================================================
	)
    goto objMenuLoop
)
echo.

:: objPrompt User for Choice
:objPrompt
set "strInput="
set /p "strInput=Select what you want to do:"

:: objValidate strInput [Remove Special Characters]
if not defined strInput goto objPrompt
set "strInput=%strInput:"=%"
set "strInput=%strInput:^=%"
set "strInput=%strInput:<=%"
set "strInput=%strInput:>=%"
set "strInput=%strInput:&=%"
set "strInput=%strInput:|=%"
set "strInput=%strInput:(=%"
set "strInput=%strInput:)=%"

:: Equals are not allowed in variable names
set "strInput=%strInput:^==%"
call :objValidate %strInput%

:: objProcess strInput
call :objProcess %strInput%
goto End


:objValidate
set "objNext=%2"
if not defined strRequest[%1] (
    set "Message=Invalid Input: %1"
    goto objMenu
)
if defined objNext shift & goto objValidate
goto :eof


:objProcess
set "objNext=%2"
call set "strRequest=%%strRequest[%1]%%"

:: Run Commands
if "%strRequest%" EQU "%strName[1]%" (
    title Loading Pylar's Convert Save Tool - Modified by xKillerMaverick...
	cls
    :: Run the convert_level_location_finder.py script
	python convert_level_location_finder.py sav
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[2]%" (
    title Loading Pylar's Convert Save Tool - Modified by xKillerMaverick...
	cls
    :: Run the convert_level_location_finder.py script
	python convert_level_location_finder.py json
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[3]%" (
    title Loading Pylar's Convert Save Tool - Modified by xKillerMaverick...
	cls
    :: Run the convert_players_location_finder.py script to convert sav to json
	python convert_players_location_finder.py sav
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[4]%" (
    title Loading Pylar's Convert Save Tool - Modified by xKillerMaverick...
	cls
    :: Run the convert_players_location_finder.py script to convert json to sav
	python convert_players_location_finder.py json
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[5]%" (
	title Loading xKillerMaverick's Game Pass Save Convert Tool - Based on Pylar's/Z1ni Scripts...
	cls
    :: Run the game_pass_save_fix.py script
	python game_pass_save_fix.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[6]%" (
	title Loading Fr33dan's Game Pass Save Converter...
	cls
	:: Run the GPSaveConverter.py script
	python GPSaveConverter.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[7]%" (
	title Loading oMaN-Rod's Save Editor...
	cls
	:: Run the PSP.py script
	python PSP.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[8]%" (
    title Loading Pylar's Save Tool - Modified by xKillerMaverick...
	cls
    :: Delete old files from previous runs
	if exist "fix_save.log" del "fix_save.log"
	if exist "players.log" del "players.log"
	if exist "sort_players.log" del "sort_players.log"
	if exist "Pal Logger" rmdir /s /q "Pal Logger"
	if exist "import_lock.txt" del "import_lock.txt"
	:: Run the fix_save.py with Level.sav
	python fix_save_location_finder.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[9]%" (
    title Loading Pylar's Map Maker Tool...
	cls
    :: Run the internal_libs.base.py
	python -m internal_libs.bases
	:: Open the image file
	if exist "updated_worldmap.png" (
		echo Opening updated_worldmap.png...
		start updated_worldmap.png
	) else (
		echo updated_worldmap.png not found.
	)
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[10]%" (
    title Loading Pylar's Save Tool...
	cls
    :: Run the fix_host_save.py with LocalWorldSave
	python fix_host_save.py LocalWorldSave
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[11]%" (
	title Loading Pylar's Save Tool...
	cls
	:: Run the char-export.py script
	python char-export.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[12]%" (
    title Loading Pylar's Save Tool...
	cls
    :: Run the convertids.py script
	python convertids.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[13]%" (
    title Loading Pylar's Coordinate Converter Tool..
	cls
    :: Run the Coordinate_Converter.py script
	python Coordinate_Converter.py
	pause
    goto objMenu
)
if "%strRequest%" EQU "%strName[14]%" (
    title Loading Pylar's Save Tool...
	cls
	:: Execute sort_players.py using the Python from the virtual environment
	python sort_players.py players.log
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[15]%" (
    title Loading Pylar's Save Tool...
	cls
    :: Run the AutoDeleteNoSteamSaves.py script
	python AutoDeleteNoSteamSaves.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[16]%" (
    title Loading Pylar's Save Tool...
	cls
    :: Run the AutoDeleteNoXboxSaves.py script
	python AutoDeleteNoXboxSaves.py
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[17]%" (
    title  Loading Pylar's Save Tool - Modified by xKillerMaverick...
	cls
	:: Execute delete_pals_save.py using the Python from the virtual environment
	python delete_pals_save.py players.log
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[18]%" (
    title Loading Pylar's Save Tool...
	cls
    :: Run the AutoCheckBases.py script
	python AutoCheckBases.py
	pause
)
if "%strRequest%" EQU "%strName[19]%" (
    title Cleaning Palworld Save Utilities Directory...
	cls
	:: Clean up all .log files
	del /q *.log >nul 2>&1
	echo All logs have been deleted.
	:: Delete the Pal Logger folder and its contents
	if exist "Pal Logger" rmdir /s /q "Pal Logger" >nul 2>&1
	echo Pal Logger folder and all contents within have been deleted.
	:: Delete the Players folder and its contents
	if exist "Players" rmdir /s /q "Players" >nul 2>&1
	echo Players folder and all contents within have been deleted.
	:: Delete everything in external_libs except for palworld_save_tools and palworld_coord
	if exist "external_libs" (
		pushd "external_libs"
		for /d %%D in (*) do (
			if /i not "%%~nxD"=="palworld_save_tools" if /i not "%%~nxD"=="palworld_coord" (
				rmdir /s /q "%%D" >nul 2>&1
			)
		)
		for %%F in (*) do (
			if /i not "%%~nxF"=="palworld_save_tools" if /i not "%%~nxF"=="palworld_coord" (
				del /q "%%F" >nul 2>&1
			)
		)
		popd
		echo All contents except palworld_save_tools and palworld_coord have been deleted from external_libs.
	)
	:: Delete the LocalWorldSave folder and its contents
	if exist "LocalWorldSave" rmdir /s /q "LocalWorldSave" >nul 2>&1
	echo LocalWorldSave folder and all contents within have been deleted.
	:: Recreate the LocalWorldSave folder
	mkdir "LocalWorldSave"
	echo New LocalWorldSave folder has been created.
	:: Delete the DedicatedServerSave folder and its contents
	if exist "DedicatedServerSave" rmdir /s /q "DedicatedServerSave" >nul 2>&1
	echo DedicatedServerSave folder and all contents within have been deleted.
	:: Recreate the DedicatedServerSave folder
	mkdir "DedicatedServerSave"
	echo New DedicatedServerSave folder has been created.
	:: Delete the GamePassSave folder and its contents
	if exist "GamePassSave" rmdir /s /q "GamePassSave" >nul 2>&1
	echo GamePassSave folder and all contents within have been deleted.
	:: Recreate the GamePassSave folder
	mkdir "GamePassSave"
	echo New GamePassSave folder has been created.
	:: Create a new Players folder
	mkdir "DedicatedServerSave/Players"
	mkdir "LocalWorldSave/Players"
	echo New Players folders has been created.
	:: Delete all .sav files
	del /q *.sav >nul 2>&1
	echo All .sav files have been deleted.
	:: Delete all .json files except for games.json
	for %%i in (*.json) do if not "%%i"=="games.json" del /q "%%i"
	echo All .json files have been deleted.
	:: Delete all .csv files
	del /q *.csv >nul 2>&1
	echo All .csv files have been deleted.
	:: Delete all .png files
	del /q *.png >nul 2>&1
	echo All .png files have been deleted.
	:: Delete all .zip files
	del /q *.zip >nul 2>&1
	echo All .zip files have been deleted.
	:: Detect and delete all __pycache__ folders recursively
	for /r %%D in (__pycache__) do (
		if exist "%%D" rmdir /s /q "%%D" >nul 2>&1
	)
	echo All __pycache__ folders has been deleted.
	:: Delete import_lock.txt
	if exist "import_lock.txt" del "import_lock.txt"
	echo Everything's all cleaned.
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[20]%" (
	title Palworld Save Utilities Package Manager
	cls
	echo To Delete all Downloaded files Press any button to continue else close the Command Prompt
	pause
	:: Delete GPSaveConverter.exe
	if exist "GPSaveConverter.exe" del "GPSaveConverter.exe"
	:: Delete the psp_windows folder and its contents
	if exist "psp_windows" rmdir /s /q "psp_windows" >nul 2>&1
	echo All Downloaded files have been removed.
	echo To list all Python Package Press any button to continue else close the Command Prompt
	pause
    pip list
	echo To Uninstall Press any button to continue else close the Command Prompt
	pause
	:: Uninstall all packages listed in requirements.txt
	pip uninstall -r requirements.txt -y
	echo Uninstallation complete.
	pip list
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[21]%" (
    title Updating Palworld Save Utilities...
	cls
	:: Ensures pip is installed after checking python is installed already.
	python -m ensurepip --upgrade >nul 2>&1
    git init >nul 2>&1
    git remote remove origin >nul 2>&1
    git remote add origin https://github.com/xkillermaverick/PalworldSaveUtilities.git
    echo Replacing all files in the current directory with the latest from GitHub...
    git fetch --all
    git reset --hard origin/main
    git clean -fdx
    echo Update complete. All files have been replaced.
    pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[22]%" (
    title About Palworld Save Utilities
	cls
	echo The UI was made by xKillerMaverick with plety of research in programing languages i dont fully know but work on this in hopes it help anyone that needs these tools
	echo Converting and Repairing Palworld Save file is only possable due to Pylar's and his team's hard work
	echo Xbox Game Pass Save Extraction is only possable due to Z1ni's and his team's hard work
	echo Steam to Game Pass Convertion is only possable due to Fr33dan's and his team's hard work
	echo Palworld Save Editing is only possable due to oMaN-Rod's and his team's hard work
	pause
	goto objMenu
)
if "%strRequest%" EQU "%strName[23]%" (
    title Closing Palworld Save Utilities...
    exit
)

:: Prevent the command from being processed twice if listed twice.
set "strRequest[%1]="
if defined objNext shift & goto objProcess
goto :eof

:End
endlocal
pause >nul

