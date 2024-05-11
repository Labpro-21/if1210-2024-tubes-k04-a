import time

if __package__ is None or __package__ == "":
    import rng
    import ui
    from monster import atk_result
    from potion import use_potion
    from utils import clear, is_number, to_lowercase, dict_copy, list_copy
else:
    from . import rng
    from . import ui
    from .monster import atk_result
    from .potion import use_potion
    from .utils import clear, is_number, to_lowercase, dict_copy, list_copy

def run(GAME_STATE: dict[str, dict[str, str]], enemy_level: int = rng.get(1, 6), from_arena: bool = False) -> str:
    enemy_monster = dict_copy(GAME_STATE['monster'][rng.get(0, len(GAME_STATE['monster']))])
    enemy_monster['level'] = enemy_level
    enemy_monster = _monster_attribute(enemy_monster)
    base_enemy_monster = dict_copy(enemy_monster)
    
    my_monster = _choose_monster(GAME_STATE)
    my_monster = _monster_attribute(my_monster)
    base_my_monster = dict_copy(my_monster)
    
    result = ""
    isRunning = True
    while isRunning:
        clear()
        option = ""
        while not option:
            option = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, "", "Pilih aksi yang ingin kamu lakukan: ")
            if option == "1" or to_lowercase(option) == "attack":
                damage = atk_result(my_monster, enemy_monster)
                enemy_monster['hp'] -= damage
                if enemy_monster['hp'] < 0: enemy_monster['hp'] = 0
                _ = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, f"Kamu menyerang dengan\n{damage} damage", "")
                time.sleep(3)
                if enemy_monster['hp'] <= 0:
                    result = "win"
                    isRunning = False

            elif option == "2" or to_lowercase(option) == "potion":
                potion = ""
                while not potion:
                    potion = _potion_menu(GAME_STATE['user_item_inventory'])
                    if potion == "1": potion = "strength"
                    elif potion == "2": potion = "resilience"
                    elif potion == "3": potion = "healing"
                    else: potion = to_lowercase(potion)

                    if potion in ["strength", "resilience", "healing"]:
                        if GAME_STATE['user_item_inventory'][potion]:
                            GAME_STATE['user_item_inventory'][potion] -= 1
                            break
                        print(f"Kamu ga punya {potion} potion!!!")
                        potion = ""
                        option = ""
                        time.sleep(3)
                        break
                    else:
                        potion = ""

                if not potion:
                    continue
                my_monster_before_potion = dict_copy(my_monster)
                my_monster = use_potion(potion, my_monster, GAME_STATE['monster'])
                message = f"""
                Attack power menjadi  - {my_monster['atk_power']} (dari {my_monster_before_potion['atk_power']})
                Defense power menjadi - {my_monster['def_power']} (dari {my_monster_before_potion['def_power']})
                HP monster menjadi    - {my_monster['hp']} (dari {my_monster_before_potion['hp']})
                """
                print(message)
                _ = input("Enter untuk lanjut")

            elif option == "3" or to_lowercase(option) == "exit":
                isRunning = False
            else:
                option = ""

        if not isRunning:
            break
        
        # Enemy turn
        enemy_damage = atk_result(enemy_monster, my_monster)
        my_monster['hp'] -= enemy_damage
        if my_monster['hp'] < 0: my_monster['hp'] = 0
        _ = _action_menu(my_monster, enemy_monster, base_my_monster, base_enemy_monster, f"Musuh menyerang dengan\n{enemy_damage} damage", "")
        time.sleep(3)
        if my_monster['hp'] <= 0:
            result = "lose"
            isRunning = False

    return result

def _choose_monster(GAME_STATE: dict[str, dict[str, str]]):
    isValid = False
    while not isValid:
        contents = [
            {"type": "TEXT", "text": "Silahkan pilih salah satu monster yang ingin kamu gunakan", "width": 0, "align": "^", "max_length": 70, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "TABLE", "data": GAME_STATE["user_monster_inventory"], "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": [4, 14, 12, 12, 8, 30, 7]},
            ]
        inp = ui.render_menu(["REGISTER", True], contents, "Masukan id monster yang dipilih: ")
        if is_number(inp) and inp:
            id = int(inp)
            for monster in GAME_STATE["user_monster_inventory"]:
                if monster['id'] == id:
                    return dict_copy(monster)
        print("Mohon masukkan input yang sesuai!")

def _action_menu(my_monster: dict[str,str], enemy_monster: dict[str, str], base_my_monster: dict[str, str], base_enemy_monster: dict[str, str], message: str, prompt: str) -> str:
    my_monster_stats = _get_stats_text(my_monster, base_my_monster, 35)
    enemy_monster_stats = _get_stats_text(enemy_monster, base_enemy_monster, 35)
    contents = [
            {"type": "ASCII", "text": "MONSTER2", "width": 37, "align": ">"},
            {"type": "TEXT", "text": message, "width": 24, "align": "*", "max_length": 24, "inner_align": "^"},
            {"type": "ASCII", "text": "MONSTER1", "width": 37, "align": "<"},
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

def _potion_menu(potion_list: list[dict[str, str]]) -> str:
    s = potion_list['strength']
    r = potion_list['resilience']
    h = potion_list['healing']
    contents = [
            {"type": "TEXT", "text": "Kamu punya: ", "width": 98, "align": "^", "max_length": 88, "inner_align": "<"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 32, "align": "^"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 33, "align": "^"},
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 32, "align": "^"},
            {"type": "TEXT", "text": f"{s} botol strength", "width": 32, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "TEXT", "text": f"{r} botol resilience", "width": 33, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "TEXT", "text": f"{h} boto healing", "width": 32, "align": "^", "max_length": 32, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "BUTTON", "text": "STRENGTH", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "RESILIENCE", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "HEALING", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
    ]

    option = ui.render_menu([], contents, "Pilih potion yang ingin kamu pakai: ")

    return option

def _get_stats_text(monster: dict[str, str], base_monster: dict[str, str], width: int) -> str:
    result = ""
    monster_name = f"{monster['type']} (Lvl. {monster['level']})"
    result += " {text: {align}{width}} \n".format(text=monster_name, align="<", width=width - 4)
    leftover_width = (width - 3) // 2 - 6
    atk = "ATK:{text: {align}{width}} ".format(text=monster['atk_power'], align=">", width = leftover_width)
    defe = " DEF:{text: {align}{width}}".format(text=monster['def_power'], align=">", width= leftover_width)
    result += ' ' + atk + '│' + defe + ' \n'
    bar_width = width - 8
    hp_left_width = int(monster['hp'] / base_monster['hp'] * bar_width)
    hp_bar = f"HP: {'█' * hp_left_width + '░' * (bar_width - hp_left_width)}"
    result += " {text: {align}{width}} \n".format(text=hp_bar, align="<", width=width - 4)
    hp_stats = f"({monster['hp']}/{base_monster['hp']})"
    result += " {text: {align}{width}} ".format(text=hp_stats, align=">", width= width - 4)
    return result

def _monster_attribute(monster: dict[str, str]) -> dict[str, str]: 
    """
    Mengkalkulasikan atribut monster sesuai levelnya
    """
    
    monster['atk_power'] = int(int(monster['atk_power'])+((((monster['level'] - 1) * 10)/100)*int(monster['atk_power'])))
    monster['def_power'] = int(int(monster['def_power'])+((((monster['level'] - 1) * 10)/100)*int(monster['def_power'])))
    if int(monster['def_power']) > 50:
        monster['def_power'] = 50
    monster['hp'] = int(int(monster['hp'])+((((monster['level'] - 1) * 10)/100)*int(monster['hp'])))

    return monster


