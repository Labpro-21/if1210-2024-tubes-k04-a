if __package__ is None or __package__ == "":
    import ui
    from utils import dict_copy, list_copy, is_number
else:
    from . import ui
    from .utils import dict_copy, list_copy, is_number

# Main function to manage the shop
def manage_shop(GAME_STATE: dict[str, dict[str, str]]) -> None:
    while True:
        contents = [
        {"type": "ASCII", "text": "SHOP", "width": 98, "align": "^"},
        {"type": "BUTTON", "text": "Beli Potions", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Beli Monster", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Keluar dari shop", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu([], contents, "Masukkan pilihanmu")

        if choice == '1':
            while True:
                if buy_potion(GAME_STATE):
                    break
        elif choice == '2':
            while True:
                if buy_monster(GAME_STATE):
                    break
        elif choice == '3':
            break
        else:
            continue

def potion_available(GAME_STATE: dict[str, dict[str, str]], potion_type: str) -> dict[str, str]:
    owned = {}
    for item in GAME_STATE['user_item_inventory']:
        if item['type'] == potion_type:
            return item
    return owned

def monster_owned(GAME_STATE: dict[str, dict[str, str]], monster_id: str) -> dict[str, str]:
    owned = False
    for monster in GAME_STATE['user_monster_inventory']:
        if monster['id'] == monster_id:
            owned = True
            break
    return owned


def buy_potion(GAME_STATE: dict[str, dict[str, str]]) -> bool:
    potion_type = show_potion(GAME_STATE)
    if potion_type == "exit": return True # Return true berarti udahan
    for item in GAME_STATE['item_shop']:
        if item['type'] == potion_type:
            if item['stock'] == 0:
                ui.enter_to_continue_menu("Potion yang ingin kamu beli sudah habis!", "Kembali")
                return False # Return false berarti milih lagi
            item_price = int(item['price'])
            item_amount = ask_item_amount(item)
            if item_amount * item_price > GAME_STATE['user']['oc']:
                ui.enter_to_continue_menu("O.W.C.A. Coin kamu tidak cukup!", "Kembali")
                return False 
            confirm = ui.confirm_menu(f"Apakah kamu yakin ingin membeli potion {item['type']} sebanyak {item_amount} dengan total harga\n{item_price * item_amount} OC?")
            if not confirm: return False
            GAME_STATE['user']['oc'] -= item_amount * item_price
            item['stock'] -= item_amount
            potion_owned = potion_available(GAME_STATE, potion_type)
            if potion_owned:
                potion_owned['quantity'] += item_amount
            else:
                new_user_item = {}
                for key in item:
                    if key != 'stock':
                        new_user_item[key] = item[key]
                new_user_item['quantity'] = item_amount
                GAME_STATE['user_item_inventory'].append(new_user_item)

                new_item = {'user_id': GAME_STATE['user']['id'], 'type': item['type'], 'quantity': item_amount}
                GAME_STATE['item_inventory'].append(new_item)
            _ = ui.enter_to_continue_menu('Pembelian berhasil\nTerimakasih sudah berbelanja di toko kami!', "Lanjut")
            return True
    _ = ui.enter_to_continue_menu('Potion tidak ditemukan!', "Kembali")
    return False

def buy_monster(GAME_STATE: dict[str, dict[str, str]]) -> tuple[bool, int]:
    monster_id = show_monster(GAME_STATE)
    if monster_id == "exit": return True
    for monster in GAME_STATE['monster_shop']:
        if str(monster['monster_id']) == monster_id:
            if monster['stock'] == 0:
                ui.enter_to_continue_menu("Monster yang ingin kamu beli sudah habis!", "Kembali")
                return False # Return false berarti milih lagi

            item_price = monster['price']
            if monster_owned(GAME_STATE, monster['monster_id']):
                    ui.enter_to_continue_menu("Kamu sudah memiliki monster ini!", "Kembali")
                    return False
            if GAME_STATE['user']['oc'] >= item_price:
                confirm = ui.confirm_menu(f"Apakah kamu yakin ingin membeli monster ini dengan harga {item_price} OC?")
                if not confirm: return False 
                else:
                    GAME_STATE['monster_inventory'].append({'user_id': GAME_STATE['user']['id'], 'monster_id': monster['monster_id'], 'level': 1})
                    user_monster = {}
                    for monster_data in GAME_STATE['monster']:
                        if monster['monster_id'] == monster_data['id']:
                            monster_copy = dict_copy(monster_data)
                            monster_copy['level'] = 1
                            user_monster = monster_copy
                            break
                    GAME_STATE['user_monster_inventory'].append(user_monster)
                    GAME_STATE['user']['oc'] -= monster['price']
                    monster['stock'] -= 1
                    _ = ui.enter_to_continue_menu('Pembelian berhasil\nTerimakasih sudah berbelanja di toko kami!', "Lanjut")
                    return True

            else:
                ui.enter_to_continue_menu("O.W.C.A. Coin kamu tidak cukup!", "Kembali")
                return False 

    _ = ui.enter_to_continue_menu('Monster tidak ditemukan!', "Kembali")
    return False

def show_potion(GAME_STATE: dict[str, dict[str, str]]) -> str:
    owca_left_text = " O.W.C.A. Coin Kamu: {text: {align}{width}}".format(text=GAME_STATE['user']['oc'], align=">", width=18)
    contents = [
        {"type": "ASCII", "text": "SHOP", "width": 98, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih salah satu potion yang ingin kamu beli", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "TABLE", "data": GAME_STATE['item_shop'], "width": 98, "align": "^", "inner_width": 78, "inner_align": "<", "size": [20, 10, 10, 38]},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": owca_left_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
            ]
    inp = ui.render_menu([], contents, "Masukkan type potion yang dipilih")
    return inp

    

def show_monster(GAME_STATE: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    user_monsters_with_price = []
    for monster in GAME_STATE['monster_shop']:
        for monster_data in GAME_STATE['monster']:
            if monster_data['id'] == monster['monster_id']:
                monster_with_price = dict_copy(monster_data)
                monster_with_price['stock'] = monster['stock']
                monster_with_price['price'] = monster['price']
                user_monsters_with_price.append(monster_with_price)

    owca_left_text = " O.W.C.A. Coin Kamu: {text: {align}{width}}".format(text=GAME_STATE['user']['oc'], align=">", width=18)
    contents = [
        {"type": "ASCII", "text": "SHOP", "width": 98, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih salah satu monster yang ingin kamu beli", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "TABLE", "data": user_monsters_with_price, "width": 98, "align": "^", "inner_width": 83, "inner_align": "<", "size": [4, 14, 8, 8, 8, 26, 7, 8]},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": owca_left_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
            ]
    inp = ui.render_menu([], contents, "Masukkan id monster yang dipilih")
    return inp

def ask_item_amount(item: dict[str, str]) -> int:
    while True:
        message = f"""
        Berapa banyak potion {item['type']} dengan harga {item['price']} OC yang ingin kamu beli?
        (sisa stock: {item['stock']})
        """
        contents = [
            {'type': "NEWLINE"},
            {'type': "NEWLINE"},
            {'type': "NEWLINE"},
            {"type": "TEXT", "text": message, "width": 0, "align": "*", "max_length": 80, "inner_align": "^"},
            {'type': "NEWLINE"},
            {'type': "NEWLINE"},
            {'type': "NEWLINE"},
            
        ]

        user_inp = ui.render_menu([], contents, "Masukkan jumlah item")
        if is_number(user_inp) and user_inp:
            amount = int(user_inp)
            if amount > 0 and amount <= item['stock']:
                return amount
        ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Oke!")


