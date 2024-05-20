if __package__ is None or __package__ == "":
    import file_io
    import encrypt
    import ui
    from utils import dict_copy, list_copy
else:
    from . import file_io
    from . import encrypt
    from . import ui
    from .utils import dict_copy, list_copy

def run(GAME_STATE: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    user_data = {}
    isRunning = True

    while isRunning:
        contents = [
        {"type": "ASCII", "text": "HALO_AGENT", "width": 60, "align": ">"},
        {"type": "ASCII", "text": "PERRY", "width": 38, "align": "^"},
        ]

        username = ui.render_menu(["LOGIN", True], contents, "Masukkan username")

        password = ui.render_menu(["LOGIN", True], contents, "Masukkan password")

        GAME_STATE['user'] = _search_user(username, password, GAME_STATE["user_list"])

        if GAME_STATE['user']['id'] == "not_exist":
            if _is_continue("Username yang anda masukkan tidak ada!"):
                continue
            else:
                GAME_STATE['user'] = {}
                break
        elif GAME_STATE['user']['id'] == "wrong_password":
            if _is_continue("Password yang anda masukkan salah!"):
                continue
            else:
                GAME_STATE['user'] = {}
                break
        else:
            GAME_STATE['isLogin'] = True
            GAME_STATE['user_monster_inventory'] = _get_user_monster_inventory(GAME_STATE)
            GAME_STATE['user_item_inventory'] = _get_user_item_inventory(GAME_STATE)
            break
        
    return GAME_STATE

def _search_user(username: str, password: str, user_list: list[dict[str, str]]) -> dict[str, str]:
    for user in user_list:
        if user['username'] == username:
            if str(user['password']) == encrypt.encrypt(password):
                return dict_copy(user)
            else:
                return {"id": "wrong_password"}
    return {"id": "not_exist"} 

def _get_user_item_inventory(GAME_STATE: list[dict[str, str]]) -> dict[str,str]:
    result = []
    for data in GAME_STATE['item_inventory']:
        if data['user_id'] == GAME_STATE['user']['id']:
            user_item = {} 
            for item in GAME_STATE['item_shop']:
                if data['type'] == item['type']:
                    for key in item:
                        if key != 'stock':
                            user_item[key] = item[key]
                    break
            user_item['quantity'] = data['quantity']
            result.append(user_item)
                     
    return result


def _get_user_monster_inventory(GAME_STATE: list[dict[str, str]]) -> list[dict[str,str]]:
    result = []
    for data in GAME_STATE['monster_inventory']:
        if data['user_id'] == GAME_STATE["user"]["id"]:
            user_monster = {}
            for monster in GAME_STATE['monster']:
                if data['monster_id'] == monster['id']:
                    monster_copy = dict_copy(monster)
                    monster_copy['level'] = data['level']
                    user_monster = monster_copy
                    break
            result.append(user_monster)

    return result

def _is_continue(message: str) -> bool:
    isContinue = False
    while True:
        contents = [
        {"type": "TEXT", "text": message, "width": 0, "align": "*", "max_length": 60, "inner_align": "^"},
        {"type": "BUTTON", "text": "Ulangi", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Kembali", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        ]

        user_inp = ui.render_menu(['REGISTER', True], contents, "Masukkan pilihanmu disini")
        if user_inp == '1':
            isContinue = True
            break
        if user_inp == '2':
            break

    return isContinue


