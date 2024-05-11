import time

if __package__ is None or __package__ == "":
    import rng
    import ui
    from monster import atk_result
    from utils import clear, is_number
else:
    from . import rng
    from . import ui
    from .monster import atk_result
    from .utils import clear, is_number

def run(GAME_STATE: dict[str, dict[str, str]]) -> str:
    monster = GAME_STATE['monster'][rng.get(0, len(GAME_STATE['monster']))]
        
    my_monster = _choose_monster(GAME_STATE)
    print("Monster lawan:", monster['type'], "(Level 1)")
    print("Stats musuh: ", monster)
    print("Monster kamu: ", my_monster["type"])
    print("Stats kamu: ", my_monster)
    time.sleep(3)

    result = ""
    isRunning = True
    while isRunning:
        clear()
        option = ""
        while not option:
            contents = [
                {"type": "ASCII", "text": "MONSTER1", "width": 35, "align": "^"},
                {"type": "TEXT", "text": f"Kamu melawan {monster['type']}", "width": 60, "align": "*", "max_length": 0},
                {"type": "BUTTON", "text": "ATTACK", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
                {"type": "BUTTON", "text": "USE POTION", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
                {"type": "BUTTON", "text": "EXIT", "inner_width": 22, "inner_align": "^", "width": 32, "align": "^", "isNumbered": True},
            ]

            option = ui.render_menu([], contents, "Pilih aksi yang ingin kamu lakukan: ")
            if option == "1":
                damage = atk_result(my_monster['id'], my_monster['level'], monster['id'], 1, GAME_STATE['monster'])
                print("Kamu menyerang dengan ", damage, "damage")
                monster['hp'] -= damage
                print("Monster musuh bersisa", monster['hp'], "hp")
                time.sleep(3)
                if monster['hp'] <= 0:
                    result = "win"
                    isRunning = False
                    break
            elif option == "3":
                isRunning = False
                break
            else:
                option = ""

        if not isRunning:
            break
        
        enemy_damage = atk_result(monster['id'], 1, my_monster['id'], my_monster['level'], GAME_STATE['monster'])
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
                return monster
        print("Mohon masukkan input yang sesuai!")
