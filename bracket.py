from PIL import Image, ImageDraw, ImageFont
import random
import math
import io

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def create_matchups(microbes):
    # Group microbes by type
    type_groups = {}
    for m in microbes:
        type_groups.setdefault(m['type'], []).append(m)

    # Shuffle and pair within each group
    all_pairs = []
    for group in type_groups.values():
        random.shuffle(group)
        while len(group) > 1:
            all_pairs.append((group.pop(), group.pop()))
if len(group) == 1:
    leftover = group.pop()
    if [m for m1, m2 in all_pairs for m in (m1, m2) if m['name'] == 'BYE']:
        # Find a BYE match already inserted and pair this one with it
        for idx, (m1, m2) in enumerate(all_pairs):
            if m2['name'] == 'BYE':
                all_pairs[idx] = (m1, leftover)
                break
    else:
        all_pairs.append((leftover, {\"name\": \"BYE\", \"type\": \"\", \"student\": \"\"}))

    # Create rounds by pairing winners
    rounds = [all_pairs]
    while len(rounds[-1]) > 1:
        prev_round = rounds[-1]
        new_round = []
        temp = [m1 if m2['name'] == "BYE" else m1 for m1, m2 in prev_round]
        random.shuffle(temp)
        while len(temp) > 1:
            new_round.append((temp.pop(), temp.pop()))
        if temp:
            new_round.append((temp.pop(), {"name": "BYE", "type": "", "student": ""}))
        rounds.append(new_round)
    return rounds

def generate_bracket_image(rounds):
    width = 1200
    round_height = 60
    spacing = 30
    height = len(rounds[0]) * (round_height + spacing)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, 16)
    except:
        font = ImageFont.load_default()

    col_width = width // len(rounds)
    for i, round_matches in enumerate(rounds):
        for j, (m1, m2) in enumerate(round_matches):
            y = j * (round_height + spacing)
            x = i * col_width
            name1 = f"{m1['name']} ({m1['student']})" if m1['name'] != "BYE" else "BYE"
            name2 = f"{m2['name']} ({m2['student']})" if m2['name'] != "BYE" else "BYE"
            draw.text((x + 10, y), name1, fill="black", font=font)
            draw.text((x + 10, y + 20), "vs", fill="gray", font=font)
            draw.text((x + 10, y + 40), name2, fill="black", font=font)
    return img
