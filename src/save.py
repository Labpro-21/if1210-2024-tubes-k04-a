import os

if __package__ is None or __package__ == "":
    import file_io
    import ui
else:
    from . import file_io
    from . import ui

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

        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 98, "align": ">", "isNumbered": False},
                ]
        folder = ui.render_menu([], content, "Nama folder")

        if folder == 'exit':
            return True
    
        if folder in saved_folders:
            ui.enter_to_continue_menu("Nama folder sudah ada!\nGunakan nama yang lain!", "Ulangi")
        else:
            break

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
    


if __name__ == "__main__":
    print("test")
