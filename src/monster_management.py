if __package__ is None or __package__ == '':
    import ui
    from utils import to_lowercase, is_number
else:
    from . import ui
    from .utils import to_lowercase, is_number

def monster_admin(GAME_STATE: dict[str, dict[str, str]]):
    while True:
        contents = [
        {"type": "ASCII", "text": "MANAGE", "width": 98, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih aksi yang ingin kamu lakukan", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "BUTTON", "text": "Lihat", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Tambah", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Ubah", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Hapus", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Keluar", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu([], contents, "Masukkan pilihanmu")
        choice = to_lowercase(choice)

        if choice == '1' or choice == "lihat":
            _see_monsters(GAME_STATE)
        elif choice == '2' or choice == "tambah":
            _add_monster(GAME_STATE)
        elif choice == '3' or choice == "ubah":
            _edit_monster(GAME_STATE)
        elif choice == '4' or choice == "hapus":
            _delete_monster(GAME_STATE)
        elif choice == '5' or choice == "keluar" or choice == 'exit':
            break
        else:
            continue

def _see_monsters(GAME_STATE: dict[str, dict[str, str]]):
    contents = [
        {"type": "TABLE", "data": GAME_STATE["monster"], "width": 98, "align": "^", "inner_width": 85, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
        {"type": "BUTTON", "text": "Kembali", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]
    inp = ui.render_menu([], contents, "Tekan enter untuk kembali")
    return

def _add_monster(GAME_STATE: dict[str, dict[str, str]]):
    name, atk, defe, hp, desc = None, None, None, None, None

    contents = _get_monster_detail_content(name, atk, defe, hp, desc, True)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan nama monster")
        if user_inp:
            name = user_inp
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc, True)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan attack power monster")
        if is_number(user_inp) and user_inp:
            atk = int(user_inp)
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc, True)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan defend power monster")
        if is_number(user_inp) and user_inp:
            defe = int(user_inp)
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc, True)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan hp monster")
        if is_number(user_inp) and user_inp:
            hp = int(user_inp)
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc, True)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan deskripsi monster")
        if user_inp:
            desc = user_inp
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")
    
    isDone = ui.confirm_menu(f"Apakah kamu yakin ingin menambahkan {name} ke database monster?")
    
    if isDone:
        max_id = -1
        for monster_data in GAME_STATE['monster']:
            max_id = monster_data['id'] if monster_data['id'] > max_id else monster_data['id']
        new_monster_data = {'id': max_id + 1, 'type': name, 'atk_power': atk, 'def_power': defe, 'hp': hp, 'description': desc}
        GAME_STATE['monster'].append(new_monster_data)
        ui.enter_to_continue_menu(f"{name} berhasil ditambahkan ke database monster\nMohon segera lakukan save agar perubahan dapat tersimpan", "Kembali")
        return
    else:
        return

def _edit_monster(GAME_STATE: dict[str, dict[str, str]]):
    monster = {}
    contents = [
        {"type": "TABLE", "data": GAME_STATE["monster"], "width": 98, "align": "^", "inner_width": 85, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
        ]
    while not monster:
        inp = ui.render_menu([], contents, "Mohon pilih id dari monster yang ingin diubah")
        for monster_data in GAME_STATE['monster']:
            if str(monster_data['id']) == inp:
                monster = monster_data
                break
        if not monster:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")
            continue

    name, atk, defe, hp, desc = monster['type'], monster['atk_power'], monster['def_power'], monster['hp'], monster['description']

    contents = _get_monster_detail_content(name, atk, defe, hp, desc)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan nama monster")
        if user_inp:
            name = user_inp
            break
        elif user_inp == 'tetap':
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan attack power monster")
        if is_number(user_inp) and user_inp:
            atk = int(user_inp)
            break
        elif user_inp == 'tetap':
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan defend power monster")
        if is_number(user_inp) and user_inp:
            defe = int(user_inp)
            break
        elif user_inp == 'tetap':
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan hp monster")
        if is_number(user_inp) and user_inp:
            hp = int(user_inp)
            break
        elif user_inp == 'tetap':
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

    contents = _get_monster_detail_content(name, atk, defe, hp, desc)

    while True:
        user_inp = ui.render_menu([], contents, "Masukkan deskripsi monster")
        if user_inp:
            desc = user_inp
            break
        elif user_inp == 'tetap':
            break
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")
    
    isDone = ui.confirm_menu(f"Apakah kamu yakin ingin menambahkan {name} ke database monster?")
    
    if isDone:
        monster['type'], monster['atk_power'], monster['def_power'], monster['hp'], monster['description'] = name, atk, defe, hp, desc 
        for old_monster in GAME_STATE['user_monster_inventory']:
            if old_monster['id'] == monster['id']:
                old_monster['type'] = monster['type']
                old_monster['atk_power'] = monster['atk_power']
                old_monster['def_power'] = monster['def_power']
                old_monster['hp'] = monster['hp']
                old_monster['description'] = monster['description']
        ui.enter_to_continue_menu(f"Data {name} berhasil diubah ke database monster\nMohon segera lakukan save agar perubahan dapat tersimpan", "Kembali")
        return
    else:
        return

def _delete_monster(GAME_STATE: dict[str, dict[str, str]]):
    monster = {}
    contents = [
        {"type": "TABLE", "data": GAME_STATE["monster"], "width": 98, "align": "^", "inner_width": 85, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False},
        ]
    while not monster:
        inp = ui.render_menu([], contents, "Mohon pilih id dari monster yang ingin diubah")
        if inp == 'exit':
            return

        for monster_data in GAME_STATE['monster']:
            if str(monster_data['id']) == inp:
                monster = monster_data
                break
        if not monster:
            ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")
            continue

    isConfirm = ui.confirm_menu(f"Apakah kamu yakin ingin menghapus {monster['type']} dari database?\n\nCatatan: Data monster ini pada inventory setiap user yang memilikinya akan hilang dan juga item ini akan hilang dari shop.")

    if isConfirm:
        id = monster['id']
        name = monster['type']
        temp_monster = []
        for monster_data in GAME_STATE['monster']:
            if monster_data['id'] != id:
                temp_monster.append(monster_data)

        GAME_STATE['monster'] = temp_monster

        temp_monster_inventory = []
        for monster_data in GAME_STATE['monster_inventory']:
            if monster_data['monster_id'] != id:
                temp_monster_inventory.append(monster_data)
        GAME_STATE['monster_inventory'] == temp_monster_inventory

        temp_user_monster_inventory = []
        for monster_data in GAME_STATE['user_monster_inventory']:
            if monster_data['id'] != id:
                temp_user_monster_inventory.append(monster_data)
        GAME_STATE['user_monster_inventory'] = temp_user_monster_inventory

        temp_monster_shop = []
        for monster_data in GAME_STATE['monster_shop']:
            if monster_data['monster_id'] != id:
                temp_monster_shop.append(monster_data)
        GAME_STATE['monster_shop'] = temp_monster_shop

        ui.enter_to_continue_menu(f"{name} telah berhasil dihapus dari database!\nMohon segera save agar perubahan dapat tersimpan", "Kembali")
        return
    else:
        return

def _get_monster_detail_content(name: str, atk: int, defe:int, hp:int, desc: str, isNew = False) -> list[dict[str, str]]:
    detail = "\n\n"
    detail += (f"Name       : {name}\n")
    detail += (f"ATK Power  : {atk}\n")
    detail += (f"DEF Power  : {defe}\n")
    detail += (f"HP         : {hp}\n")
    detail += (f"Description: {desc}\n")

    contents = [
        {"type": "ASCII", "text": "MONSTER7", "width": 38, "align": "^"},
        {"type": "TEXT", "text": detail, "width": 60, "align": "<", "max_length": 54, "inner_align": "<"},
        {"type": "NEWLINE"},
        ]

    if not isNew:
        contents.append({"type": "BUTTON", "text": "Ketik 'tetap' untuk menggunakan data sebelumnya", "inner_width": 51, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False})

    return contents



    
