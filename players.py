from convert import *
def main():
    convertion_type = sys.argv[1]
    players_folder = "Players"
    players = os.listdir(players_folder) 
    if not os.path.exists(players_folder):
        print(f"Players folder '{players_folder}' not found.")
        exit(1)
    if len(players) == 0:
        print(f"Players folder '{players_folder}' is empty.")
        exit(1)
    if convertion_type == "sav":
        for root, dirs, player_files in os.walk(players_folder):
            for specific_player_file in player_files:
                if specific_player_file.endswith(".sav"):
                    player_location = os.path.join(root, specific_player_file)
                    player_sav_output_path = player_location.replace(".json", ".sav")
                    convert_json_to_sav(player_location, player_sav_output_path)
    if convertion_type == "json":
        for root, dirs, player_files in os.walk(players_folder):
            for specific_player_file in player_files:
                if specific_player_file.endswith(".sav"):
                    player_location = os.path.join(root, specific_player_file)
                    player_json_output_path = player_location.replace(".sav", ".json")
                    convert_sav_to_json(player_location, player_json_output_path)
if __name__ == "__main__":
    main()