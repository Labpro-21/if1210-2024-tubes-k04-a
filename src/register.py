if __name__ == "__main__":
    import encrypt
    import file_io
else:
    from . import encrypt
    from . import file_io

def run() -> dict[str, str]:
    user_list = file_io.read_csv("", "user.csv")
    new_user_list = []
    data = {}
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
        data['username'] = username
        data['password'] = encrypted_password
        print("list: ", user_list)

        new_user_list = _add_new_user_data(username, encrypted_password, user_list)

    if new_user_list:
        return {"status": "success"}
    return {"status": "failed"}

def _get_username(user_list: list[dict[str, str]]) -> str:
    username = ""
    isUsernameValid = False
    while not isUsernameValid:
        username = input("Masukkan username: ")
        if not _is_username_valid(username):
            print("Username hanya boleh berisi alfabet, angka, underscore, dan strip serta panjang maksimal 16 karakter")
            if _is_continue():
                continue
            else:
                username = ""
                break

        if _is_username_used(username, user_list):
            print("Username sudah digunakan!")
            
            if _is_continue():
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
        password = input("Masukkan password: ")
        isPasswordValid = True
        for char in password:
            if not char in encrypt.SEED:
                isPasswordValid = False
                print("Terdapat karakter yang tidak terdefinisi pada password")
                print("Coba password lain.")
                break
        if not isPasswordValid:
            isContinue = _is_continue()
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

def _add_new_user_data(username: str, password: str, user_list: list[dict[str, str]]) -> dict[str, str]:
    user_data = {}
    user_data['id'] = len(user_list) + 1
    user_data['username'] = username
    user_data['password'] = password
    user_data['role'] = "agent"
    user_data['oc'] = 0

    user_list.append(user_data)

    file_io.write_csv("", "user.csv", user_list)
    return user_list

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

if __name__ == "__main__":
    print(run())
