import os

if __package__ is None or __package__ == "":
    import file_io
    import ui
    from utils import to_lowercase
else:
    from . import file_io
    from . import ui
    from .utils import to_lowercase

def save(GAME_STATE: dict[str, dict[str, str]]) -> bool:
    folder = GAME_STATE['save_folder']
    isOverwrite = False
    if GAME_STATE['save_folder'] != "default_folder":
        isOverwrite = ui.confirm_menu("Apakah kamu ingin melakukan overwrite terhadap save sebelumnya?")
    
    saved_folders = file_io.get_folders(os.getcwd() + "/data")
    while not isOverwrite:

        content = [
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {"type": "TEXT", "text": "Masukkan nama save folder yang ingin dibuat", "width": 0, "align": "*", "max_length": 90, "inner_align": "^"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},

        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 37, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False},
                ]
        folder = ui.render_menu([], content, "Nama folder")

        if folder == 'exit':
            return True

        isValid, message = _is_valid_directory_name(folder, saved_folders)
        if isValid:
            break
        else:
            ui.enter_to_continue_menu(message, "Ulangi")
    

    confirm = ui.confirm_menu(f"Apakah kamu yakin ingin membuat save baru di folder {folder} ?")

    if not confirm:
        return False

    if not folder in saved_folders:
        os.mkdir(f'{file_io.DIR_PATH}/data/{folder}')

    for user_item in GAME_STATE['user_item_inventory']:
        for item in GAME_STATE['item_inventory']:
            if item['user_id'] == GAME_STATE['user']['id'] and item['type'] == user_item['type']:
                item['quantity'] = user_item['quantity']

    for user in GAME_STATE['user_list']:
        if user['id'] == GAME_STATE['user']['id']:
            user['oc'] = GAME_STATE['user']['oc']

    file_names = ["monster_inventory",
                  "item_inventory",
                  "monster_shop",
                  "item_shop",
                  "user_list",
                  "monster",
                  ]
    keys = [key for key in GAME_STATE]

    for file in file_names:
        if not file in keys:
            return False
    
    for file in file_names:
        key = file
        if file == "user_list":
            file = "user"

        file_io.write_csv(folder, f"{file}.csv", GAME_STATE[key])
    
    GAME_STATE['save_folder'] = folder
    ui.enter_to_continue_menu("SAVE TELAH BERHASIL", "Kembali")
    return True

def _is_valid_directory_name(dir_name, saved_folders):
    # Karakter yang dilarang untuk semua OS
    forbidden_chars = {'<', '>', ':', '"', '/', '\\', '|', '?', '*'}
    
    # Tambahan larangan untuk windows
    reserved_names = {
        "con", "prn", "aux", "nul",
        "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
        "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"
    }
   
    # Cek kalau nama folder kosong
    if not dir_name:
        return False, "Nama folder tidak boleh kosong."

    # Cek kalau nama folder mengandung huruf kapital
    if to_lowercase(dir_name) != dir_name:
        return False, f"Nama folder tidak boleh mengandung huruf kapital!" # Untuk menghindari nama file yang sama
    
    # Cek apabila terdapat karakter yang dilarang
    for char in forbidden_chars:
        if char in dir_name:
            return False, f"Nama folder mengandung karakter terlarang: {forbidden_chars}"

    # Cek apabila nama folder merupakan reserved folders windows
    if os.name == 'nt' and to_lowercase(dir_name) in reserved_names:
        return False, f"Nama folder merupakan folder bawaan windows: {reserved_names}"

    # Cek apabila folder sudah ada
    if dir_name in saved_folders:
        return False, "Nama folder sudah ada!\nGunakan nama yang lain!"

    # Cek apabila ada spasi di awal dan di akhir
    if dir_name[0] == ' ' or dir_name[len(dir_name) - 1] == ' ':
        return False, "Nama folder tidak boleh mengandung spasi di awal atau di akhir"

    # Jika semua cek berhasil dilewati
    return True, ""
    


if __name__ == "__main__":
    print("test")
