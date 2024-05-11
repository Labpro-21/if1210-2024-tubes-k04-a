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

def run(GAME_STATE: dict[str, dict[str, str]], enemy_level: int = rng.get(1, 6)) -> str:
    enemy_monster = dict_copy(GAME_STATE['monster'][rng.get(0, len(GAME_STATE['monster']))])
    enemy_monster['level'] = enemy_level
    
    my_monster = _choose_monster(GAME_STATE)
    print("Monster lawan:", enemy_monster['type'], "(Level 1)")
    print("Stats musuh: ", enemy_monster)
    print("Monster kamu: ", my_monster["type"])
    print("Stats kamu: ", my_monster)
    _ = input("Enter untuk lanjut")

    result = ""
    isRunning = True
    while isRunning:
        clear()
        option = ""
        while not option:
            option = _action_menu(enemy_monster)
            if option == "1" or to_lowercase(option) == "attack":
                damage = atk_result(my_monster['id'], my_monster['level'], enemy_monster['id'], enemy_monster['level'], GAME_STATE['monster'])
                print("Kamu menyerang dengan ", damage, "damage")
                enemy_monster['hp'] -= damage
                print("Monster musuh bersisa", enemy_monster['hp'], "hp")
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
        enemy_damage = atk_result(enemy_monster['id'], enemy_monster['level'], my_monster['id'], my_monster['level'], GAME_STATE['monster'])
        my_monster['hp'] -= enemy_damage
        print("Musuh menyerang dengan ", enemy_damage, "damage")
        print("Monster kamu bersisa", my_monster['hp'], "hp")
        time.sleep(3)
        if my_monster['hp'] <= 0:
            result = "lose"
            isRunning = False

    return result

def _choose_monster(GAME_STATE: dict[str, dict[str, str]]):
    print("Silahkan pilih salah satu monster yang ingin kamu gunakan.")
    for i, monster in enumerate(GAME_STATE["user_monster_inventory"]):
        print(f"{i + 1}. {monster['type']}")

    isValid = False
    while not isValid:
        inp = input("Masukkan nomor monster yang dipilih: ")
        if is_number(inp):
            idx = int(inp) - 1
            if idx >= 0 and idx < len(GAME_STATE["user_monster_inventory"]):
                monster = GAME_STATE["user_monster_inventory"][idx]
                return dict_copy(monster)
        print("Mohon masukkan input yang sesuai!")

def _action_menu(monster: dict[str, str]) -> str:
    contents = [
            {"type": "ASCII", "text": "MONSTER1", "width": 35, "align": "^"},
            {"type": "TEXT", "text": f"Kamu melawan {monster['type']}", "width": 60, "align": "*", "max_length": 0},
            {"type": "BUTTON", "text": "ATTACK", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "USE POTION", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "EXIT", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
    ]

    option = ui.render_menu([], contents, "Pilih aksi yang ingin kamu lakukan: ")

    return option

def _potion_menu(potion_list: list[dict[str, str]]) -> str:
    s = potion_list['strength']
    r = potion_list['resilience']
    h = potion_list['healing']
    message = f"""
    Kamu punya:
    {s} - strength potion
    {r} - resilience potion
    {h} - healing potion
    """
    contents = [
            {"type": "ASCII", "text": "POTION_BOTTLE", "width": 35, "align": "^"},
            {"type": "TEXT", "text": message, "width": 60, "align": "*", "max_length": 0},
            {"type": "BUTTON", "text": "STRENGTH", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "RESILIENCE", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            {"type": "BUTTON", "text": "HEALING", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
    ]

    option = ui.render_menu([], contents, "Pilih potion yang ingin kamu pakai: ")

    return option

