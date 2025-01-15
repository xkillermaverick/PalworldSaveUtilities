from convert import *
def search_for_players_folders(search_name, root_path):
    found_folders = []
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            if dir_name == search_name:
                found_folders.append(os.path.join(root, dir_name))
    return found_folders
def main():
    convertion_type = sys.argv[1]
    players_folders = search_for_players_folders("Players", ".")
    if len(players_folders) == 0:
        print("Players folder not found.")
        exit(1)
    for specific_player_folder in players_folders:
        if convertion_type == "sav":
            for root, dirs, player_files in os.walk(specific_player_folder):
                if len(player_files) == 0:
                    print("Players folder empty.")
                    exit(1)
                for specific_player_file in player_files:
                    if specific_player_file.endswith(".json"):
                        player_location = os.path.join(root, specific_player_file)
                        player_sav_output_path = player_location.replace(".json", ".sav")
                        convert_json_to_sav(player_location, player_sav_output_path)
                    else:
                        print("No json Files found.")
                        exit(1)
        if convertion_type == "json":
            for root, dirs, player_files in os.walk(specific_player_folder):
                if len(player_files) == 0:
                    print("Players folder empty.")
                    exit(1)
                for specific_player_file in player_files:
                    if specific_player_file.endswith(".sav"):
                        player_location = os.path.join(root, specific_player_file)
                        player_json_output_path = player_location.replace(".sav", ".json")
                        convert_sav_to_json(player_location, player_json_output_path)
                    else:
                        print("No sav Files found.")
                        exit(1)
if __name__ == "__main__":
    main()