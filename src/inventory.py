import os

if __package__ is None or __package__ == "":
    from monster import monster_attribute
    import ui
    from utils import dict_copy, is_number
else:
    from .monster import monster_attribute
    from . import ui
    from .utils import dict_copy, is_number

def inventory(GAME_STATE: dict[str, dict[str, str]]) -> None:
    """
    Menampilkan fitur inventory agent dengan id yang diinput ketika memilih opsi 'Inventory' pada menu help.
    """
    while True:
        
        item_type = _inventory_main_menu()
        if item_type == "exit": return


        inventory_list = []
        if item_type == "monster":
            for monster in GAME_STATE['user_monster_inventory']:
                item_copy = {}
                monster_copy = monster_attribute(dict_copy(monster))
                for key in monster_copy:
                    if key != "description":
                        item_copy[key] = monster_copy[key]
                inventory_list.append(item_copy)

        if item_type == "item":
            for item in GAME_STATE['user_item_inventory']:
                item_copy = {}
                for key in item:
                    if key == "type" or key == "quantity":
                        item_copy[key] = item[key]
                inventory_list.append(item_copy)

        
        item_id = _choose_item_menu(inventory_list, item_type, GAME_STATE['user']['oc'])

        
        if item_id == 'exit': # keluar dari inventory
            break
        if item_id == 'continue':
            continue
        
        detail = ""
        if item_type == 'monster': # menampilkan detail monster
            item = {}
            for monster in GAME_STATE['user_monster_inventory']:
                if str(monster['id']) == item_id:
                    item = monster_attribute(dict_copy(monster))
            detail += ("\nMonster\n")
            detail += (f"Name       : {item['type']}\n")
            detail += (f"ATK Power  : {item['atk_power']}\n")
            detail += (f"DEF Power  : {item['def_power']}\n")
            detail += (f"HP         : {item['hp']}\n")
            detail += (f"Level      : {item['level']}\n")
            detail += (f"Description: {item['description']}\n")
        elif item_type == 'item': # menampilkan detail item
            item_detail = {}
            for item in GAME_STATE['user_item_inventory']:
                if item['type'] == item_id:
                    item_detail = item
            detail += ("\nPotion\n")
            detail += (f"Type       : {item_detail['type']}\n")
            detail += (f"Quantity   : {item_detail['quantity']}\n")
            detail += (f"Description: {item_detail['description']}\n")

        _detail_menu(detail, item_type)
        
        
def _inventory_main_menu() -> str:
    while True:
        contents = [
        {"type": "ASCII", "text": "INVENTORY", "width": 98, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih menu yang ingin kamu buka", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Monster", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Item", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Keluar", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu([], contents, "Masukkan pilihanmu")
        if choice == "1": choice = "monster"
        if choice == "2": choice = "item"
        if choice == "3": choice = "exit"

        if choice in  ['monster', 'item', 'exit']:
            return choice

def _choose_item_menu(item_list: list[dict[str, str]], kind: str, oc: int) -> str:
    if not item_list: # ga punya apa apa
        ui.enter_to_continue_menu(f"Kamu ga punya {kind} sama sekali!", "Kembali")
        return "continue"

    owca_left_text = " O.W.C.A. Coin Kamu: {text: {align}{width}}".format(text=oc, align=">", width=18)
    identifier, width, table_size = ('id', 64, [4, 14, 14, 14, 9, 9]) if kind == 'monster' else ('type', 40, [20, 20])
    while True:
        contents = [
        {"type": "ASCII", "text": "INVENTORY", "width": 98, "align": "^"},
        {"type": "TEXT", "text": f"Silahkan pilih salah satu {kind} yang ingin kamu lihat detailnya", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "TABLE", "data": item_list, "width": 98, "align": "^", "inner_width": width, "inner_align": "<", "size": table_size},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": owca_left_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
            ]
        item_id = ui.render_menu([], contents, f"Masukkan {identifier} {kind} untuk menampilkan detail")
        
        if item_id == 'exit':
            return 'exit'
        for item in item_list:
            if str(item[identifier]) == item_id:
                return item_id
        ui.enter_to_continue_menu(f"Mohon masukkan {identifier} {kind} yang sesuai dengan tabel!", "Ulangi")

def _detail_menu(message: str, item_type: str):

    contents = [
        {"type": "TEXT", "text": '', "width": 10, "align": "<", "max_length": 10, "inner_align": "<"},
        {"type": "TEXT", "text": message, "width": 60, "align": "<", "max_length": 60, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Kembali ke menu", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu([], contents, "Tekan Enter untuk kembali")
