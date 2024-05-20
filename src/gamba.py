from time import sleep

if __package__ is None or __package__ == "":
    import ui
    import assets
    import rng
    from utils import dict_copy, list_copy, is_number, to_lowercase
else:
    from . import ui
    from . import assets
    from . import rng
    from .utils import dict_copy, list_copy, is_number, to_lowercase

def im_feeling_lucky(GAME_STATE: dict[str, dict[str, str]]) -> None:
    while True:
        contents = [
        {"type": "BUTTON", "text": "Mulai menjadi kaya", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Peraturan", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Kabur (lagi ga hoki)", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu(['GAMBA', False], contents, "Masukkan pilihanmu")
        choice = to_lowercase(choice)

        if choice == '1' or choice == "mulai menjadi kaya" or choice == "mulai":
            while True:
                if _im_rich(GAME_STATE):
                    break
        elif choice == '2' or choice == "peraturan":
                _help_me()
        elif choice == '3' or choice == "kabur (lagi ga hoki)" or choice == "kabur" or choice == "exit":
            break
        else:
            continue

def _im_rich(GAME_STATE: dict[str, dict[str, dict[str, str]]]) -> bool:
    coin = _ask_user_coin(GAME_STATE)
    while True:
        inp = _spin_menu(GAME_STATE, coin, 'OC', 'OC', 'OC', True)
        if inp == 'spin':
            if coin > GAME_STATE['user']['oc']:
                ui.enter_to_continue_menu('OC kamu tidak cukup!\nMohon ganti nilai taruhanmu', 'Kembali')
                continue
            _spin(GAME_STATE, coin)
        elif inp == 'ganti':
            coin = _ask_user_coin(GAME_STATE)
            continue
        elif inp == 'exit':
            return True
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang benar!", "Ulangi")
            
def _spin(GAME_STATE: dict[str, dict[str, str]], coin: int):
    GAME_STATE['user']['oc'] -= coin
    item_list = ['OC',
                 'MONSTER_MINI', 'MONSTER_MINI', 'MONSTER_MINI',
                 'POTION_MINI', 'POTION_MINI', 'POTION_MINI', 'POTION_MINI', 'POTION_MINI',
                 'HAT', 'HAT', 'HAT', 'HAT', 'HAT',
                 'POO', 'POO', 'POO', 'POO', 'POO', 'POO'] # banyak kemunculan berarti lebih gampang muncul

    prize_list = {'OC': 1, 'MONSTER_MINI': 0.5, 'POTION_MINI': 0.3, 'HAT': 0.2, 'POO': 0}
    multi_list = {'OC': 8, 'MONSTER_MINI': 4, 'POTION_MINI': 2, 'HAT': 1, 'POO': 0}
    res = ['OC', 'OC', 'OC']
    for i in range(3):
        
        delay = 3 / 5
        for j in range(5):
            sleep(delay)
            num_of_step = rng.get(1, 100000)
            res[i] = item_list[num_of_step % len(item_list)]
            _spin_menu(GAME_STATE, coin, res[0], res[1], res[2], False)
    
    occurence = {'OC': 0, 'MONSTER_MINI': 0, 'POTION_MINI': 0, 'HAT': 0, 'POO': 0}
    for i in res:
        occurence[i] += 1

    reward = 0
    for key in occurence:
        if occurence[key]:
            reward += coin * prize_list[key] * (occurence[key] ** multi_list[key])

    reward = int(reward)

    GAME_STATE['user']['oc'] += reward

    spin_data = [{' ': assets.ASCII[res[0]], '  ': assets.ASCII[res[1]],'   ': assets.ASCII[res[2]]}]
    
    contents = [
        {"type": "TABLE", "data": spin_data, "width": 98, "align": "^", "inner_width": 82, "inner_align": "^", "size": [27, 28, 27]},
        {"type": "NEWLINE"},
        {"type": "TEXT", "text": f"Kamu mendapatkan {reward} OC dari spin ini!", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        ]
    inp = ui.render_menu(["GAMBA", False], contents, "Enter untuk lanjut")



def _ask_user_coin(GAME_STATE: dict[str, dict[str, str]]) -> int:
    while True:
        contents = [
        {"type": "TEXT", "text": "Berapa banyak OC yang ingin kamu pertaruhkan\nuntuk 1 spin?", "width": 0, "align": "*", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        ]
        coin = ui.render_menu(['GAMBA', False], contents, "Masukkan jumlah OC")
        if is_number(coin) and coin:
            if int(coin) <= 0:
                ui.enter_to_continue_menu("Mohon masukkan input yang sesuai!", "Ulangi")
            elif int(coin) <= GAME_STATE['user']['oc']:
                return int(coin)
            else:
                ui.enter_to_continue_menu("O.W.C.A. Coin kamu tidak cukup!", "Ulangi")
        else:
            ui.enter_to_continue_menu("Mohon masukkan input yang sesuai!", "Ulangi")


def _spin_menu(GAME_STATE: dict[str, dict[str, str]], coin: int, slot1: str, slot2: str, slot3: str, isPrompt: bool) -> int:
    spin_data = [{' ': assets.ASCII[slot1], '  ': assets.ASCII[slot2],'   ': assets.ASCII[slot3]}]
    owca_left_text = " O.W.C.A. Coin Kamu: {text: {align}{width}}".format(text=GAME_STATE['user']['oc'], align=">", width=18)
    oc_per_spin_text = " OC per spin: {text:{align}{width}}".format(text=coin, align=">", width=25)
    
    contents = [
        {"type": "TABLE", "data": spin_data, "width": 98, "align": "^", "inner_width": 82, "inner_align": "^", "size": [27, 28, 27]},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": oc_per_spin_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'ganti' untuk mengubah OC/spin", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
        {"type": "BUTTON", "text": owca_left_text, "inner_width": 43, "inner_align": "<", "width": 49, "align": ">", "isNumbered": False},
        {"type": "BUTTON", "text": "Ketik 'exit' untuk keluar", "inner_width": 43, "inner_align": "^", "width": 49, "align": "<", "isNumbered": False},
            ]
    inp = ui.render_menu(["GAMBA", False], contents, "Ketik 'spin' untuk menjadi kaya" if isPrompt else "")

    return inp

def _help_me():
    message = """
Peraturan permainan:

    1. 99% pemain gamba berhenti sebelum mendapatkan jackpot
    2. Gamba akan membuatmu kaya
    3. Teruslah bermain gamba

Mekanisme perhitungan hadiah:

    Total hadiah adalah penjumlahan hadiah setiap gambar yang muncul.
    Untuk setiap gambar yang muncul:

        hadiah = koin taruhan x multiplier x total kemunculan ^ raiser

    Tabel keterangan gambar:

               | KOIN OC | MONSTER | POTION  |  TOPI   |  POOP   |
    Multiplier |   1x    |  0.5x   |  0.3x   |  0.2x   |   0x    |
    Raiser     |   8     |    4    |    2    |    1    |    0    |
    Rarity     |    5%   |   15%   |   25%   |   25%   |   30%   |

    """
    contents = [
        {"type": "TEXT", "text": message, "width": 0, "align": "^", "max_length": 72, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Kembali ke menu", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu(['GAMBA', True], contents, "Tekan Enter untuk kembali")
