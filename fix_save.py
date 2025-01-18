from internal_libs.import_libs import *
def set_console_title(title):
    try:
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        elif platform.system() == "Darwin":
            raise PermissionError("Setting console title is not supported on macOS.")
        else:
            os.system(f"echo -ne '\033]0;{title}\007'")
    except Exception as e:
        pass
batch_title = f"Pylar's Save Tool"
set_console_title(batch_title)
log_folder = "Pal Logger"
os.makedirs(log_folder, exist_ok=True)
log_file = "fix_save.log"
logging.basicConfig(level=logging.INFO, format='%(message)s',
                    handlers=[
                        logging.FileHandler(log_file, encoding='utf-8'), 
                        logging.StreamHandler(sys.stdout)])
player_log_file = "players.log"
player_logger = logging.getLogger('playerLogger')
player_logger.setLevel(logging.INFO)
player_logger.propagate = False
player_file_handler = logging.FileHandler(player_log_file, encoding='utf-8')
player_file_handler.setFormatter(logging.Formatter('%(message)s'))
player_logger.addHandler(player_file_handler)
wsd: Optional[dict] = None
output_file = None
gvas_file = None
backup_gvas_file = None
backup_wsd = None
backup_file_path = None
playerMapping = None
output_path = None
args = None
player = None
filetime = -1
gui = None
backup_path: Optional[str] = None
delete_files = []
loadingStatistics = {}
MappingCache: MappingCacheObject = None
loadingTitle = ""
class skip_loading_progress(threading.Thread):
    def __init__(self, reader, size):
        super().__init__()
        self.reader = reader
        self.size = size
    def run(self) -> None:
        try:
            while not self.reader.progress_eof():
                if sys.platform in ['linux', 'darwin']:
                    print("\033]0;%s - %3.1f%%\a" % (loadingTitle, 100 * self.reader.progress() / self.size), end="",
                          flush=True)
                print("%3.0f%%" % (100 * self.reader.progress() / self.size), end="\b\b\b\b", flush=True)
                if gui is not None:
                    gui.set_progress(100 * self.reader.progress() / self.size)
        except ValueError:
            pass
        if gui is not None:
            gui.set_progress(100)
class ProgressGvasFile(GvasFile):
    @staticmethod
    def read(
            data: bytes,
            type_hints: dict[str, str] = {},
            custom_properties: dict[str, tuple[Callable, Callable]] = {},
            allow_nan: bool = True,
    ) -> "ProgressGvasFile":
        gvas_file = GvasFile()
        with FProgressArchiveReader(
                data,
                type_hints=type_hints,
                custom_properties=custom_properties,
                allow_nan=allow_nan,
                reduce_memory=getattr(args, "reduce_memory", False),
                check_err=getattr(args, "check_file", False),
        ) as reader:
            skip_loading_progress(reader, len(data)).start()
            gvas_file.header = GvasHeader.read(reader)
            gvas_file.properties = reader.properties_until_end()
            gvas_file.trailer = reader.read_to_end()
            if gvas_file.trailer != b"\x00\x00\x00\x00":
                print(f"{len(gvas_file.trailer)} bytes of trailer data, file may not have fully parsed")
        return gvas_file
def parse_item(properties, skip_path):
    if isinstance(properties, dict):
        if 'skip_type' in properties:
            properties_parsed = parse_skiped_item(properties, skip_path, None, True)
            for k in properties_parsed:
                properties[k] = properties_parsed[k]
        else:
            for key in properties:
                call_skip_path = skip_path + "." + key[0].upper() + key[1:]
                properties[key] = parse_item(properties[key], call_skip_path)
    elif isinstance(properties, list):
        top_skip_path = ".".join(skip_path.split(".")[:-1])
        for idx, item in enumerate(properties):
            properties[idx] = parse_item(item, top_skip_path)
    return properties
def load_skipped_decode(_worldSaveData, skip_paths, recursive=True):
    BatchParseItem(_worldSaveData, skip_paths, recursive=recursive,
                   progress=lambda reader, size: skip_loading_progress(reader, size).start(),
                   use_mp=not getattr(args, "reduce_memory", False))
def main_editor():
    print(f"Now starting the tool...")
    global output_file, output_path, args, gui, playerMapping
    parser = argparse.ArgumentParser(prog="palworld-save-editor", description="Editor for the Level.sav")
    parser.add_argument("filename")
    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.filename):
        logging.info(f"{args.filename} does not exist.")
        exit(1)
    if not os.path.isfile(args.filename):
        logging.info(f"{args.filename} is not a file.")
        exit(1)
    t1 = time.time()
    try:
        input_file_size = os.path.getsize(args.filename)
        logging.info(f"Size Level.sav: {input_file_size} bytes")
        LoadFile(args.filename)
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
    output_path = args.filename
    return None
def LoadFile(filename):
    global filetime, gvas_file, wsd, MappingCache, backup_path, players_path
    print(f"Loading {filename}...", end="", flush=True)
    filetime = os.stat(filename).st_mtime
    backup_path = os.path.join(os.path.dirname(os.path.abspath(filename)), "backup/%s" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    players_path = os.path.join(os.path.dirname(filename), "Players")
    with open(filename, "rb") as f:
        start_time = time.time()
        data = f.read()
        raw_gvas, save_type, cnk_header = decompress_sav_to_gvas(data)
        print("Done in %.2fs." % (time.time() - start_time))
        print(f"Parsing {filename}...", end="", flush=True)
        start_time = time.time()
        gvas_file = ProgressGvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, SKP_PALWORLD_CUSTOM_PROPERTIES)
        print("Done in %.2fs." % (time.time() - start_time))
        print("\n")
    wsd = gvas_file.properties['worldSaveData']['value']
    MappingCache = MappingCacheObject.get(wsd, use_mp=not getattr(args, "reduce_memory", False))
def extract_value(data, key, default_value=''):
    value = data.get(key, default_value)
    if isinstance(value, dict):
        value = value.get('value', default_value)
        if isinstance(value, dict):
            value = value.get('value', default_value)
    return value
def count_pals_found(data, player_pals_count):
    from collections import defaultdict
    owner_pals_info = defaultdict(list)
    non_owner_pals_info = []
    non_owner_pals_info_with_base = []
    owner_nicknames = {}
    base_id_groups = defaultdict(list)    
    base_count = defaultdict(int)
    for key, value in data.items():
        if key == "CharacterSaveParameterMap":
            raw_data_value_list = value.get("value", [])
            for raw_data_value_item in raw_data_value_list:
                raw_data_value_key = raw_data_value_item.get("key", {})
                raw_data_value_value = raw_data_value_item.get("value", {}).get("RawData", {})
                is_player = False
                try:
                    if ("custom_type" in raw_data_value_value and
                        raw_data_value_value["custom_type"] == ".worldSaveData.CharacterSaveParameterMap.Value.RawData" and
                        "IsPlayer" in raw_data_value_value["value"]["object"]["SaveParameter"]["value"]):
                        player_uid = raw_data_value_key.get("PlayerUId", {}).get("value") if isinstance(raw_data_value_key, dict) else None
                        nickname = raw_data_value_value["value"]["object"]["SaveParameter"]["value"].get("NickName", {}).get("value", "Unknown")
                        if player_uid:
                            owner_nicknames[player_uid] = nickname
                except KeyError as e:
                    print(f"KeyError: {e}")  
    character_save_param_map = data.get("CharacterSaveParameterMap", {}).get("value", [])
    for item in character_save_param_map:
        raw_data = item.get("value", {}).get("RawData", {}).get("value", {}).get("object", {}).get("SaveParameter", {}).get("value", {})
        if not isinstance(raw_data, dict):
            continue      
        player_uid = raw_data.get("OwnerPlayerUId", {}).get("value")
        character_id = raw_data.get("CharacterID", {}).get("value")
        level = extract_value(raw_data, "Level", 1)
        rank = extract_value(raw_data, "Rank", 1)
        base = raw_data.get("SlotID", {}).get("value", {}).get("ContainerId", {}).get("value", {}).get("ID", {}).get("value")        
        gender_value = raw_data.get("Gender", {}).get("value", {}).get("value", "")
        gender_info = {
            "EPalGenderType::Male": "Male",
            "EPalGenderType::Female": "Female"
        }.get(gender_value, "Unknown")
        passive_skills = [
            PAL_PASSIVES.get(skill_id, {}).get("Name", skill_id)
            for skill_id in raw_data.get("PassiveSkillList", {}).get("value", {}).get("values", [])
        ]
        passive_skills_str = ", Skills: " + ", ".join(passive_skills) if passive_skills else ""
        rank_hp = int(extract_value(raw_data, "Rank_HP", 0)) * 3
        rank_attack = int(extract_value(raw_data, "Rank_Attack", 0)) * 3
        rank_defense = int(extract_value(raw_data, "Rank_Defence", 0)) * 3
        rank_craft_speed = int(extract_value(raw_data, "Rank_CraftSpeed", 0)) * 3
        talents_str = (
            f"HP IV: {extract_value(raw_data, 'Talent_HP', '0')}({rank_hp}%), "
            f"ATK IV: {extract_value(raw_data, 'Talent_Shot', '0')}({rank_attack}%), "
            f"DEF IV: {extract_value(raw_data, 'Talent_Defense', '0')}({rank_defense}%), "
            f"Work Speed: ({rank_craft_speed}%)"
        )
        pal_name = PAL_NAMES.get(character_id, character_id)
        if pal_name and pal_name.lower().startswith("boss_"):
            base_name = PAL_NAMES.get(pal_name[5:], pal_name[5:])
            pal_name = f"Alpha {base_name.capitalize()}"
        pal_nickname = raw_data.get("NickName", {}).get("value", "Unknown")
        nickname_str = f", {pal_nickname}" if pal_nickname != "Unknown" else ""
        pal_info = (
            f"{pal_name}{nickname_str}, Level: {level}, Rank: {rank}, Gender: {gender_info}, "
            f"{talents_str}{passive_skills_str}, ID: {base}"  
        )        
        base_count[base] += 1
        if not player_uid:
            pal_name = pal_info.split(",")[0].strip()        
            if pal_name != "None":
                non_owner_pals_info.append(pal_info)
                non_owner_pals_info_with_base.append(f"{pal_info} (ID: {base})")
                base_id_groups[base].append(pal_info) 
                continue       
        owner_pals_info[player_uid].append(pal_info)
        player_pals_count[player_uid] = player_pals_count.get(player_uid, 0) + 1     
    if non_owner_pals_info:
        filtered_non_owner_pals = non_owner_pals_info_with_base
        total_non_owner_pals = len(filtered_non_owner_pals) 
        non_owner_log_file = os.path.join(log_folder, "non_owner_pals.log")
        with open(non_owner_log_file, 'w', encoding='utf-8') as non_owner_file:
            non_owner_file.write(f"{total_non_owner_pals} Non-Owner Pals\n")
            non_owner_file.write("-" * (len(str(total_non_owner_pals)) + len(" Non-Owner Pals")) + "\n")
            for base_id, pals in base_id_groups.items():
                count = len(pals)
                non_owner_file.write(f"ID: {base_id} (Count: {count})\n")
                non_owner_file.write("----------------")
                non_owner_file.write("-" * (len(f"ID: {base_id} (Count: {count})")) + "\n")
                non_owner_file.write("\n".join(pals) + "\n\n")              
    for player_uid, pals_list in owner_pals_info.items():
        pals_by_base_id = defaultdict(list)
        for pal in pals_list:
            if "ID:" in pal and "None" not in pal:
                base_id = pal.split("ID:")[1].strip()
                pals_by_base_id[base_id].append(pal)
        player_name = owner_nicknames.get(player_uid, 'Unknown')
        if player_name == 'Unknown':
            print(f"No nickname found for {player_uid}")
        sanitized_player_name = sanitize_filename(player_name)
        log_file = os.path.join(log_folder, f"({sanitized_player_name})({player_uid}).log")
        logger_name = ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in f"logger_{player_uid}")
        owner_logger = logging.getLogger(logger_name)
        owner_logger.setLevel(logging.INFO)
        owner_logger.propagate = False       
        if not owner_logger.hasHandlers():
            owner_file_handler = logging.FileHandler(log_file, encoding='utf-8')
            owner_file_handler.setFormatter(logging.Formatter('%(message)s'))
            owner_logger.addHandler(owner_file_handler)
        pals_count = sum(len(pals) for pals in pals_by_base_id.values())
        owner_logger.info(f"{player_name}'s {pals_count} Pals")
        owner_logger.info("-" * (len(player_name) + len(f"'s {pals_count} Pals")))
        for base_id, pals in pals_by_base_id.items():
            owner_logger.info(f"ID: {base_id}")
            owner_logger.info("----------------")
            owner_logger.info("\n".join(sorted(pals)))
            owner_logger.info("----------------")
def ShowPlayers():
    data_source = wsd
    base_locations = {}
    srcGuildMapping = MappingCacheObject.get(data_source, use_mp=not getattr(args, "reduce_memory", False))
    initial_guild_count = len(srcGuildMapping.GuildSaveDataMap)
    start_time = time.time()
    total_items = len(data_source['CharacterSaveParameterMap']['value'])
    playerMapping = {}
    for i, item in enumerate(data_source['CharacterSaveParameterMap']['value']):
        if item['value']['RawData']['value']['object']['SaveParameter']['struct_type'] == 'PalIndividualCharacterSaveParameter' and 'IsPlayer' in item['value']['RawData']['value']['object']['SaveParameter']['value'] and item['value']['RawData']['value']['object']['SaveParameter']['value']['IsPlayer']['value']:
            player_key = str(item['key']['PlayerUId']['value'])
            playerMapping[player_key] = {
                **{k: v['value'] for k, v in item['value']['RawData']['value']['object']['SaveParameter']['value'].items()},
                'InstanceId': item['key']['InstanceId']['value']}
        progress = (i + 1) * 100 // total_items
        print(f"\rNow mapping the players... {progress}%", end="")
    elapsed_time = time.time() - start_time
    print(f"\rNow mapping the players...Done in {elapsed_time:.2f}s.")
    guild_data = {}
    guild_player_count = {}
    player_data = {}
    player_pals_count = {}
    total_bases = 0
    total_pals = 0
    total_players = 0
    instance_counts = {}
    deleted_pals = []
    total_pals_count = [0]
    player_pal_caught_count = {}
    player_pal_caught_unique = {}
    player_pal_encounter_count = {}
    processed_uids = set()
    deleted_guilds_count = 0
    to_delete = []
    def process_player_file(player_uid, nickname, players_folder):
        if player_uid in processed_uids:
            print(f"{nickname}({player_uid}) already processed")
            return        
        def get_paltotalcount_from_sav(sav_file):
            print(f"Now processing... {nickname}({os.path.basename(sav_file)})")
            try:
                with open(sav_file, "rb") as file:
                    data = file.read()
                    raw_gvas, _, cnk_header = decompress_sav_to_gvas(data)
                gvas_file = ProgressGvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, SKP_PALWORLD_CUSTOM_PROPERTIES)
                json_data = json.loads(json.dumps(gvas_file.dump(), cls=CustomEncoder))
                pal_capture_count_list = json_data.get('properties', {}).get('SaveData', {}).get('value', {}).get('RecordData', {}).get('value', {}).get('PalCaptureCount', {}).get('value', [])
                unique_captured = len(pal_capture_count_list) if pal_capture_count_list else 0
                total_captured = sum(entry.get('value', 0) for entry in pal_capture_count_list) if pal_capture_count_list else 0
                pal_deck_unlock_flag_list = json_data.get('properties', {}).get('SaveData', {}).get('value', {}).get('RecordData', {}).get('value', {}).get('PaldeckUnlockFlag', {}).get('value', [])
                pal_deck_unlocked = len(pal_deck_unlock_flag_list) if pal_deck_unlock_flag_list else 0
                pal_deck_unlocked = unique_captured if unique_captured > pal_deck_unlocked else pal_deck_unlocked
                return unique_captured, total_captured, pal_deck_unlocked
            except Exception as e:
                print(f"Error processing .sav file for {nickname}({os.path.basename(sav_file)}): Save not found...")
                return 0, 0, 0   
        clean_uid = str(player_uid).replace("-", "")
        sav_files = [f for f in os.listdir(players_folder) if f.lower() == f"{clean_uid}.sav".lower()]
        if sav_files:
            sav_file_path = os.path.join(players_folder, sav_files[0])
            unique_captured, total_captured, pal_deck_unlocked = get_paltotalcount_from_sav(sav_file_path)
            player_pal_caught_unique[player_uid] = unique_captured
            player_pal_caught_count[player_uid] = total_captured
            player_pal_encounter_count[player_uid] = pal_deck_unlocked
            processed_uids.add(player_uid)
        else:
            print(f"Save file for {nickname}({player_uid}) not found.")
    start_time = time.time()
    print(f"Now processing the players saves...")
    for key, value in data_source.items():
        if key == "CharacterSaveParameterMap":
            raw_data = value
            raw_data_value = raw_data.get("value", [])
            updated_values = []
            for raw_data_value_list in raw_data_value:
                raw_data_value_key = raw_data_value_list.get("key", {})
                raw_data_value_value = raw_data_value_list.get("value", {}).get("RawData", {})
                is_player = False
                try:
                    if ("custom_type" in raw_data_value_value and
                        raw_data_value_value["custom_type"] == ".worldSaveData.CharacterSaveParameterMap.Value.RawData" and
                        "IsPlayer" in raw_data_value_value["value"]["object"]["SaveParameter"]["value"]):
                        player_uid = raw_data_value_key.get("PlayerUId", {}).get("value") if isinstance(raw_data_value_key, dict) else None
                        instance_id = raw_data_value_key.get("InstanceId", {}).get("value") if isinstance(raw_data_value_key, dict) else None
                        nickname = raw_data_value_value["value"]["object"]["SaveParameter"]["value"].get("NickName", {}).get("value")
                        player_level = extract_value(raw_data_value_value["value"]["object"]["SaveParameter"]["value"], "Level", 0)
                        playerPalCount = player_pals_count.get(player_uid, 0)
                        playerPalCaughtCount = player_pal_caught_count.get(player_uid, 0)
                        process_player_file(player_uid, nickname, players_path)
                        player_data[player_uid] = {
                            "name": nickname,
                            "Level": player_level,
                            "uid": player_uid,
                            "instanceid": instance_id,
                            "PalCount": playerPalCount,
                            "PalCaughtCount": player_pal_caught_count.get(player_uid, 0),
                            "PalCaughtUnique": player_pal_caught_unique.get(player_uid, 0),
                            "PalEncounterCount": player_pal_encounter_count.get(player_uid, 0),
                            "LastOnline": ""}
                        updated_values.append(raw_data_value_list)
                        is_player = True
                        total_players += 1
                except Exception as e:
                    print(f"Error processing CharacterSaveParameterMap: {e}")
                    continue
                finally:
                    if "custom_type" in raw_data_value_value and raw_data_value_value["custom_type"] == ".worldSaveData.CharacterSaveParameterMap.Value.RawData":
                        if isinstance(raw_data_value_key, dict):
                            instance_id = raw_data_value_key.get("InstanceId", {}).get("value")
                        else:
                            instance_id = None
                        if not is_player:
                            if instance_counts.get(instance_id, 0) == 0:
                                deleted_pals.append(instance_id)
                                total_pals_count[0] += 1
    print("Processing the players saves done in %.2fs." % (time.time() - start_time))
    start_time = time.time()
    logging.info(f"Now counting pals...")
    count_pals_found(data_source, player_pals_count)
    print("Counting pals done in %.2fs." % (time.time() - start_time))
    start_time = time.time()
    logging.info(f"Now populating the information...")
    for playerUId in playerMapping:
        playerMeta = playerMapping[playerUId]
        try:
            level_value = extract_value(playerMeta, 'Level', 0)
            level = max(int(level_value), 1)
            last_online = "Unknown"
            for guild in guild_data.values():
                for player in guild['players']:
                    if playerUId == player['player_uid']:
                        last_online = player['player_info'].get('last_online_real_time', 'Unknown')
                        break
                if last_online != 'Unknown':
                    break
            if last_online != 'Unknown':
                try:
                    last_online_local = TickToLocal(last_online)
                    last_online_human = TickToHuman(last_online) + " ago"
                except Exception as e:
                    logging.error(f"Error converting Last Online info: {e}")
                    last_online_local = 'Unknown'
                    last_online_human = 'Unknown'
            else:
                last_online_local = 'Unknown'
                last_online_human = 'Unknown'
            player_data[playerUId] = {
                "name": playerMeta.get('NickName', 'Unknown'),
                "Level": level,
                "uid": playerUId,
                "instanceid": playerMeta.get('InstanceId', 'Unknown'),
                "PalCount": player_pals_count.get(playerUId, 0),
                "LastOnlineLocal": last_online_local,
                "LastOnlineHuman": last_online_human}
            total_pals += player_pals_count.get(playerUId, 0)
        except Exception as e:
            logging.error(f"Error processing player data: {e}")
    for group_id, group_data in list(srcGuildMapping.GuildSaveDataMap.items()):
        item = group_data['value']['RawData']['value']
        mapObjectMeta = {m_k: item[m_k] for m_k in item}
        admin_uid = str(mapObjectMeta['admin_player_uid'])
        guild_leader_name = playerMapping.get(admin_uid, {}).get('NickName', admin_uid)
        guild_players = [player for player in mapObjectMeta.get('players', []) if player['player_uid'] in playerMapping]        
        if guild_players:
            guild_data[group_id] = {
                'name': mapObjectMeta.get('guild_name', 'Unnamed Guild'),
                'admin_uid': admin_uid,
                'admin_name': guild_leader_name,
                'group_id': str(mapObjectMeta['group_id']),
                'base_camp_level': item.get('base_camp_level', 'Unknown'),
                'character_count': len(mapObjectMeta.get('individual_character_handle_ids', [])),
                'base_camps': [(base_id, srcGuildMapping.BaseCampMapping.get(toUUID(base_id))) for base_id in item.get('base_ids', [])],
                'map_object_instance_ids_base_camp_points': item.get('map_object_instance_ids_base_camp_points', []),
                'players': guild_players}
            total_bases += len(guild_data[group_id]['base_camps'])
            guild_player_count[group_id] = len(guild_players)            
            for base_id in item.get('base_ids', []):
                basecamp = srcGuildMapping.BaseCampMapping.get(toUUID(base_id))
                if basecamp:
                    offset = basecamp['value']['RawData']['value']['transform']['translation']
                    old_coords = palworld_coord.sav_to_map(offset['x'], offset['y'], new=False)
                    new_coords = palworld_coord.sav_to_map(offset['x'], offset['y'], new=True)
                    base_locations[base_id] = (
                        f"Old: {old_coords[0]}, {old_coords[1]} | "
                        f"New: {new_coords[0]}, {new_coords[1]} | "
                        f"RawData: {offset['x']}, {offset['y']}, {offset['z']}")
                else:
                    base_locations[base_id] = "Unknown, Unknown"
        else:
            logging.info(f"Inactive Guild: {mapObjectMeta.get('guild_name', 'Unnamed Guild')} | Guild ID: {group_id} | Reason: No players found.")
            to_delete.append(group_id)
            deleted_guilds_count += 1
    for group_id in to_delete:
        del srcGuildMapping.GuildSaveDataMap[group_id]
    for group_id, guild in sorted(guild_data.items(), key=lambda x: x[1]['name']):
        if 'name' not in guild or not guild['name']:
            guild['name'] = 'Unnamed Guild'
        if guild['players']:
            base_locations_count = len(guild['base_camps'])
            base_locations_str = "\n".join([f"Base {i + 1}: {base_locations.get(base_id, 'Unknown, Unknown')}" for i, (base_id, _) in enumerate(guild['base_camps'])])
            if base_locations_count > 0:
                logging.info(
                    f"\nGuild: {guild['name']} | Guild Leader: {guild['admin_name']} | Guild ID: {guild['group_id']}\n"
                    f"Base Locations: {base_locations_count}\n{base_locations_str}\n"
                    f"Guild Players: {guild_player_count[group_id]}")
            else:
                logging.info(
                    f"\nGuild: {guild['name']} | Guild Leader: {guild['admin_name']} | Guild ID: {guild['group_id']}\n"
                    f"Base Locations: {base_locations_count}\n"
                    f"Guild Players: {guild_player_count[group_id]}")
            for player in guild['players']:
                player_data = playerMapping.get(player['player_uid'])
                if player_data:
                    nickname = player_data.get('NickName', 'Unknown')
                    player_uid = player['player_uid']
                    level = extract_value(player_data, 'Level', 0)
                    pal_count = player_pals_count.get(player_uid, 0)
                    pal_caught_count = player_pal_caught_count.get(player_uid, 0)
                    pal_caught_unique = player_pal_caught_unique.get(player_uid, 0)
                    pal_encounter_count = player_pal_encounter_count.get(player_uid, 0)
                    message = f"Player: {nickname} | UID: {player_uid} | Level: {level} | Caught: {pal_caught_count} | Owned: {pal_count} | Encounters: {pal_encounter_count} | Uniques: {pal_caught_unique} | Last Online: {TickToLocal(player['player_info']['last_online_real_time'])} ({TickToHuman(player['player_info']['last_online_real_time'])} ago)"
                    logging.info(message)
                    player_logger.info(message)
    print("Populating information done in %.2fs." % (time.time() - start_time))
    total_caught_pals = sum(player_pal_caught_count.values())
    logging.info(f"\n")
    total_worker_dropped_pals = total_pals_count[0] - total_pals
    total_pals_count = total_pals_count[0]
    total_guilds = len(guild_data)
    header_line = (
        f"Total Players: {total_players} | "
        f"Total Caught Pals: {total_caught_pals} | "
        f"Total Overall Pals: {total_pals_count} | "
        f"Total Owned Pals: {total_pals} | "
        f"Total Worker/Dropped Pals: {total_worker_dropped_pals} | "
        f"Total Initial Guilds: {initial_guild_count} | "        
        f"Total Inactive Guilds: {deleted_guilds_count} | "
        f"Total Active Guilds: {total_guilds} | "
        f"Total Bases: {total_bases} \n")
    resort_player_log('players.log', header_line)
    header_line = (
        f"Total Players: {total_players} \n"
        f"Total Caught Pals: {total_caught_pals} \n"
        f"Total Overall Pals: {total_pals_count} \n"
        f"Total Owned Pals: {total_pals} \n"
        f"Total Worker/Dropped Pals: {total_worker_dropped_pals} \n"
        f"Total Initial Guilds: {initial_guild_count} \n"        
        f"Total Inactive Guilds: {deleted_guilds_count} \n"
        f"Total Active Guilds: {total_guilds} \n"
        f"Total Bases: {total_bases} \n")
    logging.info(header_line)
def resort_player_log(file_path, header_line):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(header_line)
        file.writelines(lines)
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
def TickToHuman(tick):
    seconds = (wsd['GameTimeSaveData']['value']['RealDateTimeTicks']['value'] - tick) / 1e7
    s = ""
    if seconds > 86400:
        s += "%dd:" % (seconds // 86400)
        seconds %= 86400
    if seconds > 3600:
        s += "%dh:" % (seconds // 3600)
        seconds %= 3600
    if seconds > 60:
        s += "%dm:" % (seconds // 60)
        seconds %= 60
    s += "%ds" % seconds
    return s
def TickToLocal(tick):
    ts = filetime + (tick - wsd['GameTimeSaveData']['value']['RealDateTimeTicks']['value']) / 1e7
    t = datetime.datetime.fromtimestamp(ts)
    return t.strftime("%Y-%m-%d %H:%M:%S")
def backup_file(source_file):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(os.path.dirname(source_file), "Backup")
    os.makedirs(backup_folder, exist_ok=True)
    backup_filename = f"Level_{timestamp}.sav"
    backup_path = os.path.join(backup_folder, backup_filename)
    print(f"\nCreating backup file: {backup_path}", end="", flush=True)
    shutil.copy2(source_file, backup_path)
    print("\nDone")
def Save(exit_now=True):
    print("Processing GVAS to Sav file...", end="", flush=True)
    if "Pal.PalWorldSaveGame" in gvas_file.header.save_game_class_name or "Pal.PalLocalWorldSaveGame" in gvas_file.header.save_game_class_name:
        save_type = 0x32
    else:
        save_type = 0x31
    fixed_folder = os.path.join(os.path.dirname(output_path), "Fixed")
    os.makedirs(fixed_folder, exist_ok=True)
    fixed_output_path = os.path.join(fixed_folder, os.path.basename(output_path))
    backup_file(output_path)
    sav_file = compress_gvas_to_sav(gvas_file.write(SKP_PALWORLD_CUSTOM_PROPERTIES), save_type)
    print("Done")
    print("Saving Sav file...", end="", flush=True)
    with open(fixed_output_path, "wb") as f:
        f.write(sav_file)
    print("Done")
    print(f"File saved to {fixed_output_path}")
    for del_file in delete_files:
        try:
            os.unlink(del_file)
        except FileNotFoundError:
            pass
    if exit_now:
        sys.exit(0)
if __name__ == "__main__":
    main_editor()