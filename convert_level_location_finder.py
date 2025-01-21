from convert import *
import fnmatch
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
def search_file(pattern, directory):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                matching_files.append(os.path.join(root, file))
    return matching_files
def main():
    file_type = sys.argv[1]
    dirname = os.path.dirname(__file__)
    print("1. Look for Level File Automatically")
    print("2. LocalWorldSave")
    print("3. DedicatedServerSave")
    print("4. I want to input the directory path manually")
    intUserChoice = get_number_in_range(1, 4)
    if intUserChoice == 1:
        if file_type == "sav":
            level_files = search_file("Level.sav", ".")
        if file_type == "json":
            level_files = search_file("Level.json", ".")
    if intUserChoice == 2:
        if file_type == "sav":
            level_files = search_file("Level.sav", "LocalWorldSave")
        if file_type == "json":
            level_files = search_file("Level.json", "LocalWorldSave")
    if intUserChoice == 3:
        if file_type == "sav":
            level_files = search_file("Level.sav", "DedicatedServerSave")
        if file_type == "json":
            level_files = search_file("Level.json", "DedicatedServerSave")
    if intUserChoice == 4:
        level_folder = get_directory_from_user()
        if file_type == "sav":
            level_files = search_file("Level.sav", level_folder)
        if file_type == "json":
            level_files = search_file("Level.json", level_folder)
    if level_files:
        print("File found:", level_files)
    else:
        print("File not found.")
        exit(1)
    for specific_level_file in level_files:
        if specific_level_file.endswith(".sav"):
            level_location = os.path.join(dirname, specific_level_file)
            level_json_output_path = level_location.replace(".sav", ".json")
            convert_sav_to_json(level_location, level_json_output_path)
        if specific_level_file.endswith(".json"):
            level_location = os.path.join(dirname, specific_level_file)
            level_sav_output_path = level_location.replace(".json", ".sav")
            convert_json_to_sav(level_location, level_sav_output_path)
if __name__ == "__main__":
    main()