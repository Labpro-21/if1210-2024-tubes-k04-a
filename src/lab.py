if __package__ is None or __package__ == "":
    from utils import list_copy, dict_copy, is_number
    from monster import _monster_attribute
    import ui
else:
    from .utils import list_copy, dict_copy, is_number
    from .monster import _monster_attribute
    from . import ui


def upgrade_monster(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, str]:
    isValid = False
    while not isValid:
        choosen_monster_id = _user_monster_to_upgrade(GAME_STATE)
        if is_number(choosen_monster_id) and choosen_monster_id:
            id = int(choosen_monster_id)
            for monster in GAME_STATE["user_monster_inventory"]:
                if monster['id'] == id:
                    upgrade_price = monster['level'] ** 2 * 100
                    if monster['level'] == 5:
                        ui.enter_to_continue_menu("Level monster sudah maksimal!", "Kembali")
                    elif GAME_STATE['user']['oc'] < upgrade_price:
                        ui.enter_to_continue_menu("O.W.C.A. Coin kamu tidak cukup!", "Kembali")
                    else:
                        isConfirm = ui.confirm_menu(f"Apakah kamu yakin ingin mengupgrade {monster['type']}\nseharga {upgrade_price} O.W.C.A. Coin ???")
                        if isConfirm:
                            monster['level'] += 1
                            GAME_STATE['user']['oc'] -= upgrade_price
                            ui.enter_to_continue_menu(f"{monster['type']} berhasil diupgrade\nLevel {monster['level'] - 1} -> {monster['level']}", "Kembali")
                    break
        elif choosen_monster_id == 'exit':
            isValid = True
        else:
            ui.enter_to_continue_menu("Mohon masukkan id monster yang sesuai dengan tabel!", "Ulangi")
    return

def get_monster_type(monster_id: int, monster_types: list[dict[int, str]]) -> int:
    for monster_type in monster_types:
        if monster_type['id'] == monster_id:
            return monster_type['type']
    return "Unknown"

def lab_detail(user_id: int, monsters: list[dict[int, int, int]], monster_types: list[dict[int, str]]) -> None:
    user_monsters = [monster for monster in monsters if monster['user_id'] == str(user_id)]

    print("User's Monsters Inventory:")
    for monster in user_monsters:
        monster_type = get_monster_type(monster['monster_id'], monster_types)
        print(f"{monster['monster_id']} Type: {monster_type}, Level: {monster['level']}")

    print("\nPrice List:")
    for level in range(1, 6):
        needed_currency = 100 * level ** 2
        print(f"Level {level} -> {level + 1 if level < 5 else level}: {needed_currency} coins")

def _user_monster_to_upgrade(GAME_STATE: dict[str, dict[str, str]]) -> str:

    # Abaikan saja, cuma manipulasi data untuk menampilkan perubahan stats jika monster akan diupgrade
    user_monsters_with_price = list_copy(GAME_STATE['user_monster_inventory'])
    if not user_monsters_with_price:
        ui.enter_to_continue_menu("Kamu ga punya monster!", "Balik ke menu")
        return "exit"
    for i, monster in enumerate(user_monsters_with_price):
        temp = {} 
        monster_attr = _monster_attribute(dict_copy(monster))
        for key in monster:
            if key != "description":
                temp[key] = monster[key]
        temp = _monster_attribute(temp)
        if temp['level'] == 5:
            temp['price'] = "Max lvl"
        else:
            temp['level'] += 1
            temp = _monster_attribute(temp)
            temp['price'] = 100 * (temp['level'] - 1) ** 2
            temp['atk_power'] = f"{monster_attr['atk_power']} -> {temp['atk_power']}"
            temp['def_power'] = f"{monster_attr['def_power']} -> {temp['def_power']}"
            temp['hp'] = f"{monster_attr['hp']} -> {temp['hp']}"
            temp['level'] = f"{temp['level'] - 1} -> {temp['level']}"
        user_monsters_with_price[i] = temp

    owca_left_text = " O.W.C.A. Coin Kamu: {text: {align}{width}}".format(text=GAME_STATE['user']['oc'], align=">", width=18)
    contents = [
        {"type": "ASCII", "text": "LAB", "width": 60, "align": ">"},
        {"type": "ASCII", "text": "MICROSCOPE", "width": 38, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih salah satu monster yang ingin kamu upgrade", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "TABLE", "data": user_monsters_with_price, "width": 98, "align": "^", "inner_width": 78, "inner_align": "<", "size": [4, 14, 14, 12, 16, 9, 9]},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": owca_left_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
            ]
    inp = ui.render_menu([], contents, "Masukkan id monster yang dipilih: ")
    
    return inp







