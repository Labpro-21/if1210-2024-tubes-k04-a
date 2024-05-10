if __package__ is None or __package__ == "":
    import file_io
    import encrypt
    import ui
else:
    from . import file_io
    from . import encrypt
    from . import ui

def run(user_list: list[dict[str, str]]) -> dict[str, str]:
    user_data = {}
    
    isRunning = True

    while isRunning:
        contents = [
        {"type": "ASCII", "text": "HALO_AGENT", "width": 60, "align": ">"},
        {"type": "ASCII", "text": "RGB_PERRY", "width": 38, "align": "^"},
        ]

        username = ui.render_menu(["LOGIN", True], contents, "Masukkan username: ")

        password = ui.render_menu(["LOGIN", True], contents, "Masukkan password: ")

        user_data = _search_user(username, password, user_list)

        if user_data['id'] == "not_exist":
            if _is_continue("Username yang anda masukkan tidak ada!"):
                continue
            else:
                user_data = {}
                break
        elif user_data['id'] == "wrong_password":
            if _is_continue("Password yang anda masukkan salah!"):
                continue
            else:
                user_data = {}
                break
        else:
            break
        
    return user_data

def _search_user(username: str, password: str, user_list: list[dict[str, str]]) -> dict[str, str]:
    for user in user_list:
        if user['username'] == username:
            if user['password'] == encrypt.encrypt(password):
                return user
            else:
                return {"id": "wrong_password"}
    return {"id": "not_exist"} 

def _is_continue(message: str) -> bool:
    isContinue = False
    while True:
        contents = [
        {"type": "TEXT", "text": message, "width": 0, "align": "*", "max_length": 0},
        {"type": "BUTTON", "text": "Ulangi", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Kembali", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        ]

        user_inp = ui.render_menu(['REGISTER', True], contents, "Masukkan pilihanmu disini: ")
        if user_inp == '1':
            isContinue = True
            break
        if user_inp == '2':
            break

    return isContinue


