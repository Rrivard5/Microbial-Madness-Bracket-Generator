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

    all_pairs = []
    leftovers = []

    # Shuffle and pair within each group
    for group in type_groups.values():
        random.shuffle(group)
        while len(group) >= 2:
            all_pairs.append((group.pop(), group.pop()))
        if group:
            leftovers.append(group.pop())

    # Try to match leftover students with BYEs first
    for leftover in leftovers:
        bye_found = False
        for i, (m1, m2) in enumerate(all_pairs):
            if m2['name'] == 'BYE':
                all_pairs[i] = (m1, leftover)
                bye_found = True
                break
        if not bye_found:
            all_pairs.append((leftover, {"name": "BYE", "type": "", "student": ""}))

    # Add any unmatched BYEs in pairs if even number
    byes = [m for m1, m2 in all_pairs for m in (m1, m2) if m['name'] == 'BYE']
    unmatched_byes = [b for b in byes if all_pairs.count((b, {"name": "BYE", "type": "", "student": ""})) == 0]
    if len(unmatched_byes) % 2 == 0:
        for i in range(0, len(unmatched_byes), 2):
            all_pairs.append((unmatched_byes[i], unmatched_byes[i+1]))

    # Create rounds
    rounds = [all_pairs]
    current = flatten_matchups(all_pairs)
    while len(current) > 1:
        new_round = []
        random.shuffle(current)
        while len(current) >= 2:
            new_round.append((current.pop(), current.pop()))
        if current:
            new_round.append((current.pop(), {"name": "BYE", "type": "", "student": ""}))
        rounds.append(new_round)
        current = flatten_matchups(new_round)
    return rounds

def flatten_matchups(matchups):
    return [m1 for m1, m2 in matchups if m1['name'] != 'BYE'] + [m2 for m1, m2 in matchups if m2['name'] != 'BYE']

def generate_bracket_image(rounds):
    width = 200 * len(rounds)
    height = max(len(r) for r in rounds) * 100
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, 14)
    except:
        font = ImageFont.load_default()

    pos_dict = {}  # track center positions for lines

    for i, round_matches in enumerate(rounds):
        x = i * 200 + 20
        for j, (m1, m2) in enumerate(round_matches):
            y = j * 100 + 40
            name1 = f"{m1['name']} ({m1['student']})" if m1['name'] != "BYE" else "BYE"
            name2 = f"{m2['name']} ({m2['student']})" if m2['name'] != "BYE" else "BYE"

            draw.text((x, y), name1, fill="black", font=font)
            draw.text((x, y + 20), "vs", fill="gray", font=font)
            draw.text((x, y + 40), name2, fill="black", font=font)

            center_y = y + 20
            pos_dict[(i, j)] = (x, center_y)

            # draw connector from previous round
            if i > 0:
                prev_x = (i - 1) * 200 + 20 + 130
                prev_y = int(((j * 2) * 100 + 40 + ((j * 2 + 1) * 100 + 40)) / 2) + 20
                draw.line([(prev_x, prev_y), (x, center_y)], fill="gray", width=2)
    return img
