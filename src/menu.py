from src import register, login, save, ui, battle, help, rng, arena, lab, shop
from src.utils import dict_copy, clear
import os
import time

def start_menu(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    # tampilan masih sementara yang penting jadi dulu wkwjkwk

    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "REGISTER", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LOGIN", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "HELP", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "EXIT", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        ]
        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka")
        if option == "1":
            new_game_state = register.run(GAME_STATE)
            if new_game_state["user_list"][0]["id"] != "failed":
                GAME_STATE = new_game_state
        elif option == "2":
            login.run(GAME_STATE)
            if GAME_STATE["user"]:
                return
        elif option == "3":
            _help_menu(GAME_STATE)
        elif option == "4":
            clear()
            return 
        option = ""

def start_menu_already_login(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "START GAME", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LOGOUT", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        ]
        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka")
        if option == "1":
            GAME_STATE["isPlaying"] = True
            return
        elif option == "2":
            GAME_STATE["user"] = {}
            GAME_STATE['user_monster_inventory'] = []
            GAME_STATE['user_item_inventory'] = {}
            GAME_STATE["isLogin"] = False
            return
        else:
            option = ""

def main_menu(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "BATTLE", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "ARENA", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "SHOP", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LABORATORY", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "INVENTORY", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "SAVE", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "HELP", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "EXIT", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        ]

        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka")
        if option == "1":
            enemy_monster = dict_copy(GAME_STATE['monster'][rng.get(0, len(GAME_STATE['monster']))])
            enemy_monster['level'] = rng.get(1, 6)
            battle_result = battle.run(GAME_STATE, enemy_monster)
            if battle_result['status'] == "": # exited
                return 
            elif battle_result['status'] == "win":
                GAME_STATE['user']['oc'] += battle_result['reward']
                return 
            elif battle_result['status'] == "lose":
                return 
        elif option == "2":
            arena_result = arena.run(GAME_STATE)
            GAME_STATE['user']['oc'] += arena_result['total_reward']
            return
        elif option == "3":
            shop.manage_shop(GAME_STATE)
        elif option == "4":
            lab.upgrade_monster(GAME_STATE)
            return
        elif option == "6":
            while True:
                if save.save(GAME_STATE):
                    break
        elif option == "7":
            _help_menu(GAME_STATE)
        elif option == "8":
            GAME_STATE["isPlaying"] = False
            return 
        elif option == "debug":
            _debug(GAME_STATE)
            _ = input("enter untuk lanjut")
            return
        else:
            option = ""

def alert_menu(message: str) -> bool:
    isOk = False
    content = f"""-----PERHATIAN-----

{message}
    """
    inp = ui.confirm_menu(content)
    clear()
    return inp
         

def _help_menu(GAME_STATE: dict[dict[str, str]]):
    if GAME_STATE['isLogin']:
        if GAME_STATE['user']['role'] == 'admin':
            message = help.help_login_admin(GAME_STATE['user']['username'])
        else:
            message = help.help_login(GAME_STATE['user']['username'])
    else:
        message = help.help_not_login()

    contents = [
        {"type": "TEXT", "text": message, "width": 0, "align": "^", "max_length": 94, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Kembali ke menu", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu(['HELP', True], contents, "Tekan Enter untuk kembali")

    return

def _debug(GAME_STATE: dict[str, dict[str, str]]):
    for key in GAME_STATE:
        print(f"    {key}: {GAME_STATE[key]}")
        print()