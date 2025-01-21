from internal_libs.import_libs import *
x_min, x_max = -1000, 1000
y_min, y_max = -1000, 1000
image_path = 'internal_libs/worldmap.png'
image = plt.imread(image_path)
height, width = image.shape[:2]
x_scale = width / (x_max - x_min)
y_scale = height / (y_max - y_min)
def to_image_coordinates(x_world, y_world):
    x_img = (x_world - x_min) * x_scale
    y_img = (y_max - y_world) * y_scale
    return int(x_img), int(y_img)
def parse_logfile(log_path):
    print(f"Now parsing the info...")
    with open(log_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    guild_data = []
    current_guild = {}
    base_keys = set()
    total_bases = 0
    level_55_count = 0
    for line in lines:
        if line.startswith('Guild:'):
            if current_guild:
                guild_data.append(current_guild)
                current_guild = {}
            guild_info = line.strip().split('|')
            current_guild['Guild'] = guild_info[0].split(': ')[1].strip()
            current_guild['Guild Leader'] = guild_info[1].split(': ')[1].strip()
        if line.startswith('Base ') and line.split(':')[0].strip() in ['Base 1', 'Base 2', 'Base 3', 'Base 4', 'Base 5', 'Base 6', 'Base 7', 'Base 8', 'Base 9', 'Base 10']:
            base_info = line.strip().split('|')
            base_key = base_info[0].split(':')[0].strip()
            new_coords = next(
                (part.split('New:')[1].strip() for part in base_info if part.strip().startswith("New:")),
                None
            )
            if new_coords:
                current_guild[base_key] = new_coords
                base_keys.add(base_key)
                total_bases += 1
        if "Level: 55" in line:
            level_55_count += 1
    if current_guild:
        guild_data.append(current_guild)
    return guild_data, sorted(base_keys)
def write_csv(guild_data, base_keys, output_file):
    print(f"Now writing the info into csv...")
    fieldnames = ['Guild', 'Guild Leader'] + base_keys
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for guild in guild_data:
            row = {field: guild.get(field, '') for field in fieldnames}
            writer.writerow(row)
Image.MAX_IMAGE_PIXELS = None
def sanitize_text(text):
    try:
        return text.encode('utf-8', 'ignore').decode('utf-8')
    except UnicodeEncodeError:
        return text.replace('\uFFFD', '?')
def extract_info_from_log():
    print(f"Now extracting the info from log...")
    try:
        with open('fix_save.log', 'r', encoding='utf-8') as file:
            log_content = file.read()
    except UnicodeDecodeError:
        raise ValueError("Failed to read log file with utf-8 encoding.")
    stats = {
        'Total Players': 'N/A',
        'Total Caught Pals': 'N/A',
        'Total Overall Pals': 'N/A',
        'Total Owned Pals': 'N/A',
        'Total Worker/Dropped Pals': 'N/A',
        'Total Initial Guilds': 'N/A',
        'Total Inactive Guilds': 'N/A',
        'Total Active Guilds': 'N/A',
        'Total Bases': 'N/A'
    }
    for key in stats.keys():
        match = re.search(rf"{key}: (\d+)", log_content)
        if match:
            stats[key] = match.group(1)
    for key, value in stats.items():
        print(f"{key}: {value}")
    return stats
def create_world_map():
    image = Image.open('internal_libs/worldmap.png').convert('RGBA')
    marker = Image.open('internal_libs/baseicon.png').convert('RGBA')
    font_path = 'internal_libs/NotoSans-Regular.ttf'
    pil_font = ImageFont.truetype(font_path, 24)
    df = pd.read_csv('bases.csv')
    marker_size = (64, 64)
    marker_resized = marker.resize(marker_size, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    base_cols = [col for col in df.columns if col.startswith('Base ')]
    for _, row in df.iterrows():
        for col in base_cols:
            if pd.notna(row[col]):
                x, y = map(int, row[col].split(' | ')[0].split(', '))
                x_img, y_img = to_image_coordinates(x, y)
                circle_radius = 35
                circle_x = x_img
                circle_y = y_img
                draw.ellipse(
                    (circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius),
                    outline='red', width=4
                )
                marker_x = x_img - marker_size[0] // 2
                marker_y = y_img - marker_size[1] // 2
                image.paste(marker_resized, (marker_x, marker_y), marker_resized)
                text_x = x_img
                text_y = marker_y + marker_size[1] + 10
                guild = row.get('Guild', 'Unknown')
                leader = row.get('Guild Leader', 'Unknown')
                text = f"{guild} ({leader})"
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    draw.text((text_x + dx, text_y + dy), text, fill='black', font=pil_font, anchor='mm')
                draw.text((text_x, text_y), text, fill='red', font=pil_font, anchor='mm')
    stats = extract_info_from_log()
    stats_text = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
    text_bbox = draw.textbbox((0, 0), stats_text, font=pil_font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    image_width, image_height = image.size
    text_position = (image_width - text_width - 50, image_height - text_height - 50)
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.multiline_text((text_position[0] + dx, text_position[1] + dy), stats_text, fill='black', font=pil_font, align='right')
    draw.multiline_text(text_position, stats_text, fill='red', font=pil_font, align='right')
    print(f"Now populating the info for world map...")
    print(f"Now creating the world map...")
    high_dpi_image = image.resize((8000, 8000), Image.Resampling.LANCZOS)
    high_dpi_image.save('updated_worldmap.png', format='PNG', dpi=(100, 100), optimize=True)
    os.remove('bases.csv')
if __name__ == "__main__":
    start_time = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_dir = os.path.dirname(script_dir)
    log_file_path = os.path.join(main_dir, 'fix_save.log')
    try:
        guild_data, base_keys = parse_logfile(log_file_path)
        write_csv(guild_data, base_keys, 'bases.csv')
        create_world_map()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    end_time = time.time()
    duration = end_time - start_time
    print(f"Done in {duration:.2f} seconds")