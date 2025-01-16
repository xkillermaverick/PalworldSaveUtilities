# PalWorldSaveTools: Working as of v0.4.13 Patch

- **Author:** MagicBear and cheahjs  
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin  
- **Testers/Helpers:** Lethe  

---

## Prerequisites

### 1. **Updated Saves**
- Ensure your saves were updated on/after the current patch.

### 2. **[Python Installation](https://www.python.org/downloads)**
- Download Python from the official website.  
- Before clicking **Install Now**, **CHECK** the box at the bottom that says:  
  **"Add Python to PATH"** 🟩  
  (*This ensures Python is accessible from the command line!*)  
  ![Add Python to PATH checkbox](https://i.imgur.com/SCJEkdJ.png)

### 3. **[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)**
- Download and install Visual Studio Build Tools.  
- During installation, **CHECK** the box that says:  
  **"Desktop development with C++"** 🟩  
  (*This allows the `cityhash` library to install!*)  
  ![CityHash Screenshot](https://i.imgur.com/RZGZ9So.png)

---

## Features

- **Fast parsing/reading** tool—one of the quickest available.  
- Lists all players/guilds.  
- Lists all pals and their details.  
- Displays last online time for players.  
- Logs players and their data into `players.log`.  
- Sorts and deletes players based on level and inactivity.  
- Logs and sorts players by the number of pals owned.  
- Deletes players with fewer than a specified number of pals.  
- Includes double-click functionality for file save versions.  
- Provides a **base map view** via `bases.cmd`.  
- Transfers saves between dedicated servers and single/coop worlds.  
- Includes Steam ID conversion with `convertids`.  

---

## Transferring Between Servers/Worlds (Single/Coop)

- Ensure you disable private locks on the "source" chests before transferring saves.

---

## Gamepass Saves

If you're playing Palworld through Xbox Game Pass, you must extract and convert your save files using the **XGP-save-extractor** and **PalWorldSaveTools**. Follow these steps:

---

### XGP-save-extractor

- [XGP-save-extractor GitHub Repository](https://github.com/Z1ni/XGP-save-extractor)

---

### Steps

1. **Extract the Save Files**  
   - Download and unzip the **XGP-save-extractor**.  
   - Run the program, follow the prompts in the command prompt, and it will output a ZIP file containing your Xbox Game Pass Palworld save files.

2. **Locate the Save File**  
   - Unzip the exported file.  
   - Navigate to the nested folder named `Level` and locate the file named `01.sav`.

3. **Rename the Save File**  
   - Rename `01.sav` to `Level.sav`.

4. **Prepare the Save Tools**  
   - Unzip the **PalWorldSaveTools** folder.

5. **Move the Save File**  
   - Move the renamed `Level.sav` file into the **PalWorldSaveTools** folder.

6. **Convert Save to JSON**  
   - Drag `Level.sav` onto the `convert-sav-to-json.cmd` file.  
   - A new file named `Level.sav.json` will be created in the same folder.

7. **Delete the Original Save**  
   - Delete the `Level.sav` file you moved earlier.

8. **Convert JSON Back to Save**  
   - Drag `Level.sav.json` onto the `convert-json-to-sav.cmd` file.  
   - You should now have a newly converted `Level.sav` file ready to use.

---

## Automatically Delete Player Saves Based on Inactivity

Follow these steps to delete inactive players based on your criteria (e.g., inactivity, level, or number of pals):

1. Copy all files from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) to the same location within the tool (`PalworldSaveTools\`).  
2. Run `fix_save.cmd`.  
3. Run `sort_players.cmd` and/or `delete_pals_save.cmd`.  
4. Copy the `Players` folder from the tool.  
5. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).  
6. Paste the copied `Players` folder into the server folder.  
7. Restart the server:  
   - Reboot once to clear the player from `Level.sav`.  
   - Reboot a second time to clear the player from RAM.  
8. Profit?  

---

## Additional Notes

- **Days:** Deletes players inactive for a specified number of days (e.g., 30 days).  
- **Level:** Deletes players below a specified level (e.g., level 30 or lower).  
- **Pals:** Deletes players with fewer than a specified number of pals (e.g., 10 or fewer).  