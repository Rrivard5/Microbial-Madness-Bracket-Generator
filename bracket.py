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

    # Try to match leftovers with BYEs if possible
    for leftover in leftovers:
        paired = False
        for i, (m1, m2) in enumerate(all_pairs):
            if m2['name'] == 'BYE':
                all_pairs[i] = (m1, leftover)
                paired = True
                break
        if not paired:
            all_pairs.append((leftover, {'name': 'BYE', 'type': '', 'student': ''}))

    # Ensure any leftover BYEs are paired together
    bye_microbes = [m for m1, m2 in all_pairs for m in (m1, m2) if m['name'] == 'BYE']
    used_byes = set()
    bye_pairs = []
    for i in range(len(bye_microbes)):
        for j in range(i + 1, len(bye_microbes)):
            if i not in used_byes and j not in used_byes:
                bye_pairs.append((bye_microbes[i], bye_microbes[j]))
                used_byes.add(i)
                used_byes.add(j)

    for pair in bye_pairs:
        all_pairs.append(pair)

    # Begin rounds
    rounds = [all_pairs]
    current_round = [winner_from_match(m1, m2) for m1, m2 in all_pairs if winner_from_match(m1, m2) is not None]

    while len(current_round) > 1:
        next_round = []
        random.shuffle(current_round)
        while len(current_round) >= 2:
            next_round.append((current_round.pop(), current_round.pop()))
        if current_round:
            next_round.append((current_round.pop(), {'name': 'BYE', 'type': '', 'student': ''}))
        rounds.append(next_round)
        current_round = [winner_from_match(m1, m2) for m1, m2 in next_round if winner_from_match(m1, m2) is not None]

    return rounds

def winner_from_match(m1, m2):
    if m1['name'] == 'BYE' and m2['name'] == 'BYE':
        return None
    elif m1['name'] == 'BYE':
        return m2
    elif m2['name'] == 'BYE':
        return m1
    else:
        # Arbitrarily pick one — could add user input later
        return random.choice([m1, m2])

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
