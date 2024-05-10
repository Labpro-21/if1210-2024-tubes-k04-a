if __package__ is None or __package__ == "":
    import file_io
    import encrypt
else:
    from . import file_io
    from . import encrypt

def run(user_list: list[dict[str, str]]) -> dict[str, str]:
    user_data = {}
    
    isRunning = True

    while isRunning:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")

        user_data = _search_user(username, password, user_list)

        if user_data['id'] == "not_exist":
            print("Username yang anda masukkan tidak ada!")
        elif user_data['id'] == "wrong_password":
            print("Password yang anda masukkan salah!")
        else:
            break
        
        if _is_continue():
            continue
        else:
            user_data = {}
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

def _is_continue() -> bool:
    isContinue = False
    while True:
        user_inp = input("(R untuk mengisi kembali / M untuk kembali ke menu)")
        if user_inp == 'R':
            isContinue = True
            break
        if user_inp == 'M':
            break

    return isContinue
