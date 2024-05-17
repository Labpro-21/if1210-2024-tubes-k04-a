import time

if __package__ is None or __package__ == "":
    import rng
    import ui
    from monster import atk_result, monster_attribute
    from potion import use_potion
    from utils import clear, is_number, to_lowercase, dict_copy, list_copy
else:
    from . import rng
    from . import ui
    from .monster import atk_result, monster_attribute
    from .potion import use_potion
    from .utils import clear, is_number, to_lowercase, dict_copy, list_copy

def run(GAME_STATE: dict[str, dict[str, str]], enemy_monster: dict[str, str], from_arena: bool = False) -> str:
    
    # Setup data monster lawan
    enemy_monster = dict_copy(enemy_monster)
    enemy_monster = monster_attribute(enemy_monster)
    base_enemy_monster = dict_copy(enemy_monster)
    
    _monster_detail_menu(enemy_monster)

    # Setup data monster user
    my_monster = _choose_monster(GAME_STATE)
    my_monster = monster_attribute(my_monster)
    base_my_monster = dict_copy(my_monster)
    
    result = {"reward": 0, "damage_given": 0, "damage_taken": 0, "hp_healed": 0, "potion_used": 0, "status": ""}
    isRunning = True
    while isRunning:
        clear()
        option = ""
        while not option:
            option = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, "", "Pilih aksi yang ingin kamu lakukan")
            if option == "1" or to_lowercase(option) == "attack": # User memilih untuk menyerang
                damage = atk_result(my_monster, enemy_monster)
                if enemy_monster['hp'] < damage:
                    damage = enemy_monster['hp']
                enemy_monster['hp'] -= damage
                result['damage_given'] += damage
                _ = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, f"Kamu menyerang dengan\n{damage} damage", "", [4, 5])
                time.sleep(3)

                if enemy_monster['hp'] <= 0:
                    result['reward'] = _get_reward(result, enemy_monster['level'])
                    result['status'] = "win"
                    isRunning = False

            elif option == "2" or to_lowercase(option) == "potion": # User memilih untuk menggunakan potion
                potion = ""
                isChoosing = True
                while not potion and isChoosing: # Pilih potion
                    potion = _potion_menu(GAME_STATE['user_item_inventory'])
                    if potion == "1": potion = "strength"
                    elif potion == "2": potion = "resilience"
                    elif potion == "3": potion = "healing"
                    else: potion = to_lowercase(potion)

                    if potion in ["strength", "resilience", "healing"]:
                        for item in GAME_STATE['user_item_inventory']:
                            if item['type'] == potion:
                                if item['quantity']:
                                    item['quantity'] -= 1
                                    break
                        else:
                            _ = ui.enter_to_continue_menu(f"Kamu ga punya {potion} potion!!!", "Kembali")
                            potion = ""
                            option = ""
                            isChoosing = False
                            break
                    else:
                        potion = ""

                if not potion:
                    continue

                # Apply stats baru ke monster setelah menggunakan potion
                my_monster_before_potion = dict_copy(my_monster)
                my_monster = use_potion(potion, my_monster, base_my_monster)
                result['potion_used'] += 1
                if potion == "strength":
                    message = f"Attack power menjadi {my_monster['atk_power']} (dari {my_monster_before_potion['atk_power']})"
                if potion == "resilience":
                    message = f"Defense power menjadi {my_monster['def_power']} (dari {my_monster_before_potion['def_power']})"
                if potion == "healing":
                    message = f"HP monster menjadi {my_monster['hp']} (dari {my_monster_before_potion['hp']})" 


                if potion == "healing":
                    result['hp_healed'] += my_monster['hp'] - my_monster_before_potion['hp']
                _ = ui.enter_to_continue_menu(message, "Lanjut")

            elif option == "3" or to_lowercase(option) == "exit":
                isRunning = False
            else:
                option = ""

        if not isRunning:
            break
        
        # Giliran lawan
        enemy_damage = atk_result(enemy_monster, my_monster)
        if my_monster['hp'] < enemy_damage:
            enemy_damage = my_monster['hp']
        my_monster['hp'] -= enemy_damage
        result['damage_taken'] += enemy_damage

        _ = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, f"Musuh menyerang dengan\n{enemy_damage} damage", "", [3, 6])
        time.sleep(3)

        if my_monster['hp'] <= 0:
            result['status'] = "lose"
            isRunning = False

    if result['status'] == "lose" and from_arena:
        return result

    _stats_menu(result)
    return result

def _choose_monster(GAME_STATE: dict[str, dict[str, str]]):
    isValid = False
    monster_list = list_copy(GAME_STATE['user_monster_inventory'])
    for i, monster in enumerate(monster_list):
        monster_list[i] = monster_attribute(dict_copy(monster))
    while not isValid:
        contents = [
            {"type": "TEXT", "text": "Silahkan pilih salah satu monster yang ingin kamu gunakan", "width": 0, "align": "^", "max_length": 70, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "TABLE", "data": monster_list, "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": [4, 14, 12, 12, 8, 30, 7]},
            ]
        inp = ui.render_menu([], contents, "Masukan id monster yang dipilih")
        if is_number(inp) and inp:
            id = int(inp)
            for monster in GAME_STATE["user_monster_inventory"]:
                if monster['id'] == id:
                    return dict_copy(monster)

def _action_menu(my_monster: dict[str,str], enemy_monster: dict[str, str], base_my_monster: dict[str, str], base_enemy_monster: dict[str, str], message: str, prompt: str, turn: [int, int] = [3, 5]) -> str:
    my_monster_stats = _get_stats_text(my_monster, base_my_monster, 35)
    enemy_monster_stats = _get_stats_text(enemy_monster, base_enemy_monster, 35)
    contents = [
            {"type": "ASCII", "text": f"MONSTER{turn[0]}", "width": 37, "align": ">"},
            {"type": "TEXT", "text": message, "width": 24, "align": "*", "max_length": 24, "inner_align": "^"},
            {"type": "ASCII", "text": f"MONSTER{turn[1]}", "width": 37, "align": "<"},
            {"type": "BUTTON", "text": my_monster_stats, "inner_width": 37, "inner_align": "^", "width": 42, "align": ">", "isNumbered": False},
            {"type": "TEXT", "text": "", "width": 14, "align": "^", "max_length": 14, "inner_align": "^"},

            {"type": "BUTTON", "text": enemy_monster_stats, "inner_width": 37, "inner_align": "^", "width": 42, "align": "<", "isNumbered": False},
            {"type": "NEWLINE"},
            {"type": "BUTTON", "text": "ATTACK", "inner_width": 22, "inner_align": "^", "width": 33, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "USE POTION", "inner_width": 22, "inner_align": "^", "width": 33, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "EXIT", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
    ]

    option = ui.render_menu([], contents, prompt)

    return option

def _potion_menu(item_list: list[dict[str, str]]) -> str:
    s = 0
    r = 0
    h = 0
    for item in item_list:
        if item['type'] == "strength": s = item['quantity']
        elif item['type'] == "resilience": r = item['quantity']
        elif item['type'] == "healing": h = item['quantity']

    contents = [
            {"type": "TEXT", "text": "Kamu punya: ", "width": 98, "align": "^", "max_length": 88, "inner_align": "<"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 32, "align": "^"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 33, "align": "^"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 32, "align": "^"},
            {"type": "TEXT", "text": f"{s} botol strength", "width": 32, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "TEXT", "text": f"{r} botol resilience", "width": 33, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "TEXT", "text": f"{h} botol healing", "width": 32, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "BUTTON", "text": "STRENGTH", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "RESILIENCE", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "HEALING", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
    ]

    option = ui.render_menu([], contents, "Pilih potion yang ingin kamu pakai")

    return option

def _get_stats_text(monster: dict[str, str], base_monster: dict[str, str], width: int) -> str:
    result = ""
    monster_name = f"{monster['type']} (Lvl. {monster['level']})"
    result += " {text: {align}{width}} \n".format(text=monster_name, align="<", width=width - 4)
    leftover_width = (width - 3) // 2 - 6
    atk = "ATK:{text: {align}{width}} ".format(text=monster['atk_power'], align=">", width = leftover_width)
    defe = " DEF:{text: {align}{width}}".format(text=monster['def_power'], align=">", width= leftover_width)
    result += ' ' + atk + '|' + defe + ' \n'
    bar_width = width - 8
    hp_left_width = int(monster['hp'] / base_monster['hp'] * bar_width)
    hp_bar = f"HP: {'█' * hp_left_width + '░' * (bar_width - hp_left_width)}"
    result += " {text: {align}{width}} \n".format(text=hp_bar, align="<", width=width - 4)
    hp_stats = f"({monster['hp']}/{base_monster['hp']})"
    result += " {text: {align}{width}} ".format(text=hp_stats, align=">", width= width - 4)
    return result

def _monster_detail_menu(monster: dict[str, str]):
    detail = ""
    detail += ("\n\nKamu akan melawan\n\n")
    detail += (f"Name        :   {monster['type']}\n")
    detail += (f"Level       :   {monster['level']}\n")
    detail += (f"ATK Power   :   {monster['atk_power']}\n")
    detail += (f"DEF Power   :   {monster['def_power']}\n")
    detail += (f"HP          :   {monster['hp']}\n")
    detail += (f"Description :   {monster['description']}\n")
    contents = [
        {"type": "ASCII", "text": "MONSTER7", "width": 38, "align": "^"},
        {"type": "TEXT", "text": detail, "width": 60, "align": "<", "max_length": 54, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Lawan", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu([], contents, "Tekan Enter untuk melanjutkan")

# Fungsi untuk mendapatkan hadiah berdasarkan level dan hasil
def _get_reward(result: dict[str,int], level: int) -> int:
    reward = int(2 ** (level - 1) * 10)
    bonus = int(reward * (result['damage_taken'] / (result['damage_taken'] + result['damage_given'])) )
    return reward + bonus

def _stats_menu(result: dict[str, int]):

    stats = f"""Statistik pertarungan

    Damage diberikan :   {result['damage_given']}
    Damage diterima  :   {result['damage_taken']}
    HP dipulihkan    :   {result['hp_healed']}
    Potion digunakan :   {result['potion_used']}
    OC didapatkan    :   {result['reward']}
        """
    contents = [
        {"type": "TEXT", "text": "", "width": 10, "align": "^", "max_length": 10, "inner_align": "<"},
        {"type": "TEXT", "text": stats, "width": 88, "align": "<", "max_length": 50, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Keluar", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu(["MENANG" if result['status'] == 'win' else "KALAH", False], contents, "Tekan Enter untuk melanjutkan")


