if __package__ is None or __package__ == "":
    import encrypt
    import file_io
    import ui
else:
    from . import encrypt
    from . import file_io
    from . import ui

def run(GAME_STATE: dict[str, dict[str, str]]) -> list[dict[str, str]]:
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
        username = ui.render_menu(["REGISTER", True], [["RGB_PERRY_R", 30, "^"], ["AYO_BERGABUNG", 68, "<"]], [], "", "Masukkan username: ")
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
        password = ui.render_menu(["REGISTER", True], [["RGB_PERRY_R", 30, "^"], ["AYO_BERGABUNG", 68, "<"]], [], [], "Masukkan password: ")
        isPasswordValid = True
        for char in password:
            if not char in encrypt.SEED:
                isPasswordValid = False
                break
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
    print("Silahkan pilih salah satu monster sebagai monster awalmu.")
    for i, monster in enumerate(GAME_STATE["monster"]):
        print(f"{i + 1}. {monster['type']}")

    isValid = False
    while not isValid:
        inp = input("Masukkan nomor monster yang dipilih: ")
        if _is_number(inp):
            idx = int(inp) - 1
            if idx >= 0 and idx < len(GAME_STATE["monster"]):
                monster = GAME_STATE["monster"][idx]
                new_inventory_data = {"user_id": user["id"], "monster_id": monster["id"], "level": 1}
                GAME_STATE["monster_inventory"].append(new_inventory_data)
                return GAME_STATE["monster_inventory"]
        print("Mohon masukkan input yang sesuai!")


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

    if len(username) > 16:
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
        user_inp = ui.render_menu(['REGISTER', True], [], [["Ulangi", 22, "^", 49, "^", True],["Kembali", 22, "^", 49, "^", True],["Kembali", 22, "^", 49, "^", True]], [message, 0, "*", 0], "Masukkan pilihanmu disini: ")
        if user_inp == 'R':
            isContinue = True
            break
        if user_inp == 'M':
            break

    return isContinue

def _is_number(num: str) -> bool:
    isNumber = True
    
    for char in num:
        if ord(char) > ord('9') or ord(char) < ord('0'):
            isNumber = False

    return isNumber

if __name__ == "__main__":
    print(run())
