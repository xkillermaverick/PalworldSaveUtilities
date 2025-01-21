from convert import *
def get_number_in_range(min_value, max_value):
  while True:
    try:
      number = int(input(f"Enter a number between {min_value} and {max_value}: "))
      if min_value <= number <= max_value:
        return number
      else:
        print("Number is out of range. Try again.")
    except ValueError:
      print("Invalid input. Please enter an integer.")
def get_directory_from_user():
    while True:
        directory_path = input("Please enter a directory path: ")
        if os.path.isdir(directory_path):
            return directory_path
        else:
            print("Invalid directory path. Please try again.")
def search_for_players_folders(search_name, root_path):
    found_folders = []
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            if dir_name == search_name:
                found_folders.append(os.path.join(root, dir_name))
    return found_folders
def main():
    file_type = sys.argv[1]
    print("1. Look for Players Folder Automatically")
    print("2. LocalWorldSave/Players")
    print("3. DedicatedServerSave/Players")
    print("4. I want to input the directory path manually")
    intUserChoice = get_number_in_range(1, 4)
    if intUserChoice == 1:
        players_folders = search_for_players_folders("Players", ".")
    if intUserChoice == 2:
        players_folder = "LocalWorldSave/Players"
    if intUserChoice == 3:
        players_folder = "DedicatedServerSave/Players"
    if intUserChoice == 4:
        players_folder = get_directory_from_user()
    if len(players_folders) == 0:
        print("Players folder not found.")
        exit(1)
    for specific_player_folder in players_folders:
        for root, dirs, player_files in os.walk(specific_player_folder):
            if len(player_files) == 0:
                print("Players folder empty.")
                exit(1)
            if file_type == "sav":
                for specific_player_file in player_files:
                    if specific_player_file.endswith(".sav"):
                        player_location = os.path.join(root, specific_player_file)
                        player_json_output_path = player_location.replace(".sav", ".json")
                        convert_sav_to_json(player_location, player_json_output_path)
                    else:
                        print("No json Files found.")
                        exit(1)
            if file_type == "json":
                for specific_player_file in player_files:
                    if specific_player_file.endswith(".json"):
                        player_location = os.path.join(root, specific_player_file)
                        player_sav_output_path = player_location.replace(".json", ".sav")
                        convert_json_to_sav(player_location, player_sav_output_path)
                    else:
                        print("No sav Files found.")
                        exit(1)
if __name__ == "__main__":
    main()