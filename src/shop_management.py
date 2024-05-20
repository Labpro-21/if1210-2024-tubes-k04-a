if __package__ is None or __package__ == "":
    import ui
    from utils import to_lowercase, dict_copy, is_number
else:
    from . import ui
    from .utils import to_lowercase, dict_copy, is_number

def shop_admin(GAME_STATE: dict[str, dict[str, str]]):
    _main_menu(GAME_STATE)

def _main_menu(GAME_STATE: dict[str, dict[str, str]]):
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
            menu = _ask_monster_or_potion('lihat')
            _see_data_from_table(GAME_STATE, menu, True)
        elif choice == '2' or choice == "tambah":
            menu = _ask_monster_or_potion('tambah')
            if menu == 'monster':
                _add_monster_menu(GAME_STATE)
            else:
                ui.enter_to_continue_menu("Item pada shop tidak dapat ditambahkan karena mekanik game yang sudah fixed\nJika ingin mengganti jumlah item yang dijual, mohon untuk ke menu 'ubah'", "Kembali")
        elif choice == '3' or choice == "ubah":
            menu = _ask_monster_or_potion('ubah')
            data = _see_data_from_table(GAME_STATE, menu, False)
            if data == 'exit':
                continue
            if menu == 'monster':
                _edit_monster(GAME_STATE, data)
            else:
                _edit_item(GAME_STATE, data)
        elif choice == '4' or choice == "hapus":
            menu = _ask_monster_or_potion('hapus')
            if menu == 'monster':
                _delete_monster_menu(GAME_STATE)
            else:
                ui.enter_to_continue_menu("Item pada shop tidak dapat dihilangkan karena mekanik game yang sudah fixed\nJika ingin mengganti jumlah item yang dijual,  mohon untuk ke kemu 'ubah'", "Kembali")
        elif choice == '5' or choice == "keluar" or choice == 'exit':
            break
        else:
            continue


def _ask_monster_or_potion(menu: str) -> str:
    while True:
        contents = [
        {"type": "ASCII", "text": "MANAGE", "width": 98, "align": "^"},
        {"type": "TEXT", "text": f"Silahkan pilih yang ingin kamu {menu}", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "BUTTON", "text": "Monster", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Item", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu([], contents, "Masukkan pilihanmu")
        choice = to_lowercase(choice)

        if choice == '1' or choice == "monster":
            return 'monster'
        elif choice == '2' or choice == "item":
            return 'item'
        else:
            continue

def _see_data_from_table(GAME_STATE: dict[str, dict[str, str]], kind: str, isSeeOnly: bool):
    if kind == 'monster':
        user_monsters_with_price = []
        for monster in GAME_STATE['monster_shop']:
            for monster_data in GAME_STATE['monster']:
                if monster_data['id'] == monster['monster_id']:
                    monster_with_price = dict_copy(monster_data)
                    monster_with_price['stock'] = monster['stock']
                    monster_with_price['price'] = monster['price']
                    user_monsters_with_price.append(monster_with_price)
        data = user_monsters_with_price
        size = [4, 14, 8, 8, 8, 26, 7, 8]
    else:
        data = GAME_STATE['item_shop']
        size = [20, 10, 10, 38]

    if not data:
        ui.enter_to_continue_menu("Tidak ada data sama sekali!", "Kembali")
        return

     
    if isSeeOnly:
        contents = [
            {"type": "TABLE", "data": data, "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": size},
            {"type": "BUTTON", "text": "Kembali", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
            ]

        user_inp = ui.render_menu([], contents, "Tekan enter untuk kembali")

        return
    while True:
        contents = [
            {"type": "TABLE", "data": data, "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": size},
            {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False},
            ]

        user_inp = ui.render_menu([], contents, f"Silahkan masukkan {'id monster' if kind == 'monster' else 'type item'} yang ingin dipilih")
        if user_inp == 'exit':
            return 'exit'

        if kind == 'monster':
            for monster in GAME_STATE['monster_shop']:
                if str(monster['monster_id']) == user_inp:
                    return monster
        elif kind == 'item':
            for item in GAME_STATE['item_shop']:
                if item['type'] == user_inp:
                    return item
    
        ui.enter_to_continue_menu("Mohon masukkan input yang benar!", "Ulangi")

    return

def _add_monster_menu(GAME_STATE: dict[str, dict[str, str]]):
    monsters_for_sale_id = []
    for monster in GAME_STATE['monster_shop']:
        for monster_data in GAME_STATE['monster']:
            if monster['monster_id'] == monster_data['id']:
                monsters_for_sale_id.append(monster['monster_id'])

    monster_not_for_sale = []

    for monster_data in GAME_STATE['monster']:
        if not monster_data['id'] in monsters_for_sale_id:
            monster_not_for_sale.append(monster_data)

    if not monster_not_for_sale:
        ui.enter_to_continue_menu("Tidak ada data sama sekali!", "Kembali")
        return

    while True:
        contents = [
            {"type": "TABLE", "data": monster_not_for_sale, "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
            {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False},
            ]

        user_inp = ui.render_menu([], contents, f"Silahkan masukkan id monster yang ingin ditambah")
    
        if user_inp == 'exit':
            return
        
        for monster_data in monster_not_for_sale:
            if str(monster_data['id']) == user_inp:
                _add_monster(GAME_STATE, monster_data)
                return 


        ui.enter_to_continue_menu("Mohon masukkan input yang benar!", "Ulangi")

    return

def _add_monster(GAME_STATE: dict[str, dict[str, str]], data: dict[str, str]):
    while True:
        stock, price = None, None

        contents = _get_monster_detail_contents(data['type'], stock, price, True)
        
        while True:
            user_inp = ui.render_menu([], contents, "Masukkan jumlah stock")

            if is_number(user_inp) and user_inp:
                stock = int(user_inp)
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

        contents = _get_monster_detail_contents(data['type'], stock, price, True)

        while True:
            user_inp = ui.render_menu([], contents, "Masukkan nilai price")

            if is_number(user_inp) and user_inp:
                price = int(user_inp)
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

        message = f"Apakah kamu yakin ingin menambah monster {data['type']}\ndengan harga {price} OC sebanyak {stock} ?"
        isDone = ui.confirm_menu(message)

        if isDone:
            temp = {'monster_id': data['id'], 'stock': stock, 'price': price}
            GAME_STATE['monster_shop'].append(temp)
            ui.enter_to_continue_menu("MONSTER BERHASIL DITAMBAHKAN!\n\nMohon untuk segera melakukan save agar perubahan dapat tersimpan", "Kembali")
            return
        else:
            continue


def _delete_monster_menu(GAME_STATE: dict[str, dict[str, str]]):

    monster_for_sale = []

    for monster in GAME_STATE['monster_shop']:
        for monster_data in GAME_STATE['monster']:
            if monster_data['id'] == monster['monster_id']:
                monster_for_sale.append(monster_data)

    if not monster_for_sale:
        ui.enter_to_continue_menu("Tidak ada data sama sekali!", "Kembali")
        return
    while True:
        contents = [
            {"type": "TABLE", "data": monster_for_sale, "width": 98, "align": "^", "inner_width": 87, "inner_align": "<", "size": [4, 15, 12, 12, 8, 34]},
            {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False},
            ]

        user_inp = ui.render_menu([], contents, f"Silahkan masukkan id monster yang ingin dihapus dari shop")
    
        if user_inp == 'exit':
            return
        
        for monster_data in monster_for_sale:
            if str(monster_data['id']) == user_inp:
                res = _delete_monster(GAME_STATE, monster_data)
                if res:
                    return
                else:
                    break


        ui.enter_to_continue_menu("Mohon masukkan input yang benar!", "Ulangi")

    return


def _delete_monster(GAME_STATE: dict[str, dict[str, str]], data: dict[str, str]) -> list[dict[str, str]]:
    isConfirm = ui.confirm_menu(f"Apakah kamu yakin ingin menghapus monster {data['type']} dari shop?")
    if isConfirm:
        temp = []
        for monster in GAME_STATE['monster_shop']:
            if monster['monster_id'] != data['id']:
                temp.append(monster)

        GAME_STATE['monster_shop'] = temp

        ui.enter_to_continue_menu("MONSTER BERHASIL DIHAPUS DARI SHOP!\n\nMohon untuk segera melakukan save agar perubahan dapat tersimpan", "Kembali")
        return temp
    else:
        return []

def _edit_monster(GAME_STATE: dict[str, dict[str, str]], data: dict[str, str]):
    monster_data = {}
    for monster in GAME_STATE['monster']:
        if monster['id'] == data['monster_id']:
            monster_data = monster
    while True:
        stock, price = data['stock'], data['price']

        contents = _get_monster_detail_contents(monster_data['type'], stock, price)

        while True:
            user_inp = ui.render_menu([], contents, "Masukkan jumlah stock yang baru")

            if is_number(user_inp) and user_inp:
                stock = int(user_inp)
                break
            elif user_inp == 'tetap':
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")


        contents = _get_monster_detail_contents(monster_data['type'], stock, price)


        while True:
            user_inp = ui.render_menu([], contents, "Masukkan nilai price yang baru")

            if is_number(user_inp) and user_inp:
                price = int(user_inp)
                break
            elif user_inp == 'tetap':
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

        message = f"Apakah kamu yakin ingin mengubah data monster {monster_data['type']}\ndengan harga {price} OC sebanyak {stock} ?"
        isDone = ui.confirm_menu(message)

        if isDone:
            data['stock'] = stock
            data['price'] = price
            ui.enter_to_continue_menu("DATA MONSTER BERHASIL DIUBAH!\n\nMohon untuk segera melakukan save agar perubahan dapat tersimpan", "Kembali")
            return
        else:
            continue


def _edit_item(GAME_STATE: dict[str, dict[str, str]], data: dict[str, str]):
    while True:
        stock, price, description = data['stock'], data['price'], data['description']

        contents = _get_item_detail_contents(data['type'], stock, price, description)

        while True:
            user_inp = ui.render_menu([], contents, "Masukkan jumlah stock yang baru")

            if is_number(user_inp) and user_inp:
                stock = int(user_inp)
                break
            elif user_inp == 'tetap':
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

        contents = _get_item_detail_contents(data['type'], stock, price, description)

        while True:
            user_inp = ui.render_menu([], contents, "Masukkan nilai price yang baru")

            if is_number(user_inp) and user_inp:
                price = int(user_inp)
                break
            elif user_inp == 'tetap':
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")

        contents = _get_item_detail_contents(data['type'], stock, price, description)

        while True:
            user_inp = ui.render_menu([], contents, "Masukkan deskripsi baru")

            if user_inp:
                description = user_inp
                break
            elif user_inp == 'tetap':
                break
            else:
                ui.enter_to_continue_menu("Mohon masukkan input yang valid!", "Ulangi")


        message = f"Apakah kamu yakin ingin mengubah data item {data['type']}\ndengan harga {price} OC sebanyak {stock} juga deskripsi sebagai berikut:\n{description}\n?"
        isDone = ui.confirm_menu(message)

        if isDone:
            data['stock'] = stock
            data['price'] = price
            data['description'] = description
            ui.enter_to_continue_menu("DATA ITEM BERHASIL DIUBAH!\n\nMohon untuk segera melakukan save agar perubahan dapat tersimpan", "Kembali")
            return
        else:
            continue
 
def _get_monster_detail_contents(name: str, stock:int, price:int, isNew: bool = False) -> list[dict[str, str]]:
    content = f"""\n\n
    {name}
    stock : {stock}
    price : {price}
    """
    contents = [
            {"type": "ASCII", "text": "MONSTER7", "width": 38, "align": "^"},
            {"type": "TEXT", "text": content, "width": 60, "align": "<", "max_length": 54, "inner_align": "<"},
            {"type": "NEWLINE"},
        ]

    if not isNew:
        contents.append({"type": "BUTTON", "text": "Ketik 'tetap' untuk menggunakan data sebelumnya", "inner_width": 51, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False})

    return contents

def _get_item_detail_contents(name:str, stock: int, price: int, description: str) -> list[dict[str, str]]:
    content = f"""\n\n
    {name}
    stock       : {stock}
    price       : {price}
    description : {description}
    """

    contents = [
        {"type": "ASCII", "text": "POTION_BOTTLE", "width": 38, "align": "^"},
        {"type": "TEXT", "text": content, "width": 60, "align": "<", "max_length": 54, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Ketik 'tetap' untuk menggunakan data sebelumnya", "inner_width": 51, "inner_align": "^", "width": 94, "align": ">", "isNumbered": False}
    ]
    
    return contents

