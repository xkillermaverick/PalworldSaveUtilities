from convert import *
import zipfile
import glob
import shutil
def delete_converted_save_backups(root_dir, partial_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if partial_name in dirname:
                full_path = os.path.join(dirpath, dirname)
                print(f"Deleting: {full_path}")
                shutil.rmtree(full_path)
def xbox_save_zip(directory, partial_name, extract_to):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip') and partial_name in file:
                zip_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                print(f"Extracted {zip_path} to {extract_to}")
def move_and_rename_level_files(file_path, new_name):
    directory = os.path.dirname(file_path)
    parent_directory = os.path.dirname(directory)
    new_file_path = os.path.join(parent_directory, new_name)
    print("Moving file from '{file_path}' to '{new_file_path}'")
    shutil.move(file_path, new_file_path)
def main():
    xbox_save_zip(".", "palworld", "GamePassSave")
    delete_converted_save_backups("GamePassSave", "Slot")
    level_file_paths = glob.glob("GamePassSave/**/01.sav", recursive=True)
    for specific_level_file in level_file_paths:
        level_json_output_path = specific_level_file.replace(".sav", ".json")
        convert_sav_to_json(specific_level_file, level_json_output_path)
    converted_level_file_paths = glob.glob("GamePassSave/**/01.json", recursive=True)
    for specific_converted_level_file in converted_level_file_paths:
        level_sav_output_path = specific_converted_level_file.replace("01.json", "Converted.sav")
        convert_json_to_sav(specific_converted_level_file, level_sav_output_path)
        move_and_rename_level_files(level_sav_output_path, "Level.sav")
if __name__ == "__main__":
    main()