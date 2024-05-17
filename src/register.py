if __package__ is None or __package__ == "":
    import encrypt
    import file_io
    import ui
    from utils import is_number
else:
    from . import encrypt
    from . import file_io
    from . import ui
    from .utils import is_number

def run(GAME_STATE: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    ui.transition('SCENE_1', 3,3,1)
    ui.transition('SCENE_2', 3,1,1)
    ui.transition('SCENE_3', 3,1,1)
    ui.transition('SCENE_4', 3,1,1)
    ui.transition('SCENE_5', 3,1,1)
    ui.transition('SCENE_6', 3,1,1)
    ui.transition('SCENE_7', 3,1,3)
    user_list = GAME_STATE["user_list"]
    new_user_data = {}
    username = ""
    password = ""

    isRunning = True
    while isRunning:
        username = _get_username(user_list)
        
        if not username:
            break
        
        password = _get_password()
        
        if not password:
            break
                        
        isRunning = False
    
    if password:
        encrypted_password = encrypt.encrypt(password)    

        new_user_data = _generate_new_user_data(username, encrypted_password, user_list)

    if new_user_data:
        GAME_STATE["user_list"].append(new_user_data)
        GAME_STATE["monster_inventory"] = _choose_one_monster(GAME_STATE, new_user_data)
        return GAME_STATE

    return {"user_list": [{"id": "failed"}]}

def _get_username(user_list: list[dict[str, str]]) -> str:
    username = ""
    isUsernameValid = False
    while not isUsernameValid:
        message = "\n" * 8 + "Ayo bergabung bersamaku\nDan kita kalahkan Dr. Asep Spakbor bersama-sama!!!"
        contents = [
        {"type": "TEXT", "text": message, "width": 58, "align": ">", "max_length": 54, "inner_align": "^"},
        {"type": "ASCII", "text": "PERRY", "width": 40, "align": "^"},
        ]
        username = ui.render_menu(["REGISTER", True], contents, "Masukkan username")
        if not _is_username_valid(username):
            if _is_continue("Username hanya boleh berisi alfabet, angka, underscore, dan strip serta panjang maksimal 16 karakter"):
                continue
            else:
                username = ""
                break

        if _is_username_used(username, user_list):
            
            if _is_continue("Username sudah digunakan!"):
                continue
            else:
                username = ""
                break

        isUsernameValid = True

    return username

def _get_password() -> str:
    password = ""
    isPasswordValid = False
    while not isPasswordValid:
        message = "\n" * 8 + "Ayo bergabung bersamaku\nDan kita kalahkan Dr. Asep Spakbor bersama-sama!!!"
        contents = [
        {"type": "TEXT", "text": message, "width": 58, "align": ">", "max_length": 54, "inner_align": "^"},
        {"type": "ASCII", "text": "PERRY", "width": 40, "align": "^"},
        ]

        password = ui.render_menu(["REGISTER", True], contents, "Masukkan password")
        isPasswordValid = True
        for char in password: # -------------------------------------

            if not char in encrypt.SEED:
                isPasswordValid = False
                break
        
        if not password:
            continue

        if not isPasswordValid:
            isContinue = _is_continue("Terdapat karakter yang tidak terdefinisi pada password\nCoba password lain.")
            if isContinue:
                continue
            else:
                password = ""
                break
    return password

def _is_username_used(username: str, user_list: list[dict[str, str]]) -> bool:
    isUsed = False
    for user in user_list:
        if user['username'] == username:
            isUsed = True

    return isUsed

def _choose_one_monster(GAME_STATE: dict[str, dict[str, str]], user: dict[str, str]) -> list[dict[str, str]]:
    
    isValid = False
    while not isValid:

        contents = [
            {"type": "TEXT", "text": "Silahkan pilih salah satu monster sebagai monster pertama kamu", "width": 0, "align": "^", "max_length": 70, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "TABLE", "data": GAME_STATE["monster"], "width": 98, "align": "^", "inner_width": 85, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
            ]
        inp = ui.render_menu(["REGISTER", True], contents, "Masukan id monster yang dipilih")
        if is_number(inp) and inp:
            idx = int(inp) - 1
            if idx >= 0 and idx < len(GAME_STATE["monster"]):
                monster = GAME_STATE["monster"][idx]
                new_inventory_data = {"user_id": user["id"], "monster_id": monster["id"], "level": 1}
                GAME_STATE["monster_inventory"].append(new_inventory_data)
                return GAME_STATE["monster_inventory"]
        contents = [
            {"type": "TEXT", "text": "Mohon masukkan id monster yang sesuai dengan tabel!", "width": 0, "align": "*", "max_length": 60, "inner_align": "^"},
            {"type": "NEWLINE"},
            {"type": "BUTTON", "text": "Ulangi", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
                ]
        inp = ui.render_menu(["REGISTER", True], contents, "Tekan enter untuk mengisi ulang")


def _generate_new_user_data(username: str, password: str, user_list: list[dict[str, str]]) -> dict[str, str]:
    user_data = {}
    user_data['id'] = len(user_list) + 1
    user_data['username'] = username
    user_data['password'] = password
    user_data['role'] = "agent"
    user_data['oc'] = 0

    return user_data

def _is_username_valid(username: str) -> bool:
    allowed_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"

    isValid = True

    if len(username) > 16 or username == "":
        isValid = False
    else:
        for char in username:
            if not char in allowed_char:
                isValid = False
                break

    return isValid

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

if __name__ == "__main__":
    print("halo dunia")
