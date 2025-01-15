from convert import *
import glob
def search_file(pattern, directory):
    for filename in glob.glob(f"{directory}/**/{pattern}", recursive=True):
        return filename
    return None
def main():
    convertion_type = sys.argv[1]
    if convertion_type == "sav":
        level_files = search_file("Level.json", ".")
    if convertion_type == "json":
        level_files = search_file("Level.sav", ".")
    if level_files:
        print("File found:", level_files)
    else:
        print("File not found.")
        exit(1)
    for specific_level_file in level_files:
        if convertion_type == "sav":
            if specific_level_file.endswith(".json"):
                level_location = os.path.join(root, specific_level_file)
                level_sav_output_path = level_location.replace(".json", ".sav")
                convert_json_to_sav(level_location, level_sav_output_path)
            else:
                print("No sav Files found.")
                exit(1)
        if convertion_type == "json":
            if specific_level_file.endswith(".sav"):
                level_location = os.path.join(root, specific_level_file)
                level_json_output_path = level_location.replace(".sav", ".json")
                convert_sav_to_json(level_location, level_json_output_path)
            else:
                print("No json Files found.")
                exit(1)
if __name__ == "__main__":
    main()