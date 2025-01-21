from fix_save import *
import fnmatch
def search_file(pattern, directory):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                matching_files.append(os.path.join(root, file))
    return matching_files
def get_directory_from_user():
    while True:
        directory_path = input("Please enter a directory path of your players folder: ")
        if os.path.isdir(directory_path):
            return directory_path
        else:
            print("Invalid directory path. Please try again.")
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
def repair_save(level_file):
    print(f"Now starting the tool...")
    global output_file, output_path, args, gui, playerMapping
    if not os.path.exists(level_file):
        logging.info(f"{level_file} does not exist.")
        exit(1)
    if not os.path.isfile(level_file):
        logging.info(f"{level_file} is not a file.")
        exit(1)
    t1 = time.time()
    try:
        input_file_size = os.path.getsize(level_file)
        logging.info(f"Size Level.sav: {input_file_size} bytes")
        LoadFile(level_file)
    except Exception as e:
        logging.info("Corrupted Save File", exc_info=True)
        sys.exit(0)
    try:
        logging.info(f"Now checking the data...")
        ShowPlayers()
        logging.info("Data has been fully checked...\n")
    except KeyError as e:
        traceback.print_exception(e)
        logging.info("Corrupted Save File", exc_info=True)
        sys.exit(0)
    print("Total time taken: %.2fs" % (time.time() - t1))
    print("\n")
    output_path = level_file
    return None
def main():
    print("1. LocalWorldSave")
    print("2. DedicatedServerSave")
    print("3. I want to input the directory path manually")
    intUserChoice = get_number_in_range(1, 3)
    if intUserChoice == 1:
        level_files = search_file("Level.sav", "LocalWorldSave")
    if intUserChoice == 2:
        level_files = search_file("Level.sav", "DedicatedServerSave")
    if intUserChoice == 3:
        level_folder = get_directory_from_user()
        level_files = search_file("Level.sav", level_folder)
    if level_files:
        print("File found:", level_files)
    else:
        print("File not found.")
        exit(1)
    for specific_level_file in level_files:
        if specific_level_file.endswith(".sav"):
            repair_save(specific_level_file)
if __name__ == "__main__":
    main()