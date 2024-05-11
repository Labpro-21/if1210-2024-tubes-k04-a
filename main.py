from src import register, login, file_io, save, ui, battle, help
import argparse
import os
import time

SAVE_FOLDER = ""

def main():

    GAME_STATE = {"user": {},
                  "monster": file_io.read_csv("", "monster.csv"),
                  "monster_inventory": file_io.read_csv(SAVE_FOLDER, "monster_inventory.csv"),
                  "item_inventory": file_io.read_csv(SAVE_FOLDER, "item_inventory.csv"),
                  "monster_shop": file_io.read_csv(SAVE_FOLDER, "monster_shop.csv"),
                  "item_shop": file_io.read_csv(SAVE_FOLDER, "item_shop.csv"),
                  "user_list": file_io.read_csv("", "user.csv"),
                  "user_monster_inventory": [],
                  "user_item_inventory": {},
                  "isPlaying": False,
                  "isLogin": False,
                  }

    isExit = False
    while not isExit:
        _start_menu(GAME_STATE)

        if not GAME_STATE["isLogin"]:
            break

        while GAME_STATE["isLogin"]:
            _start_menu_already_login(GAME_STATE)
            
            while GAME_STATE["isPlaying"]:
                _main_menu(GAME_STATE)


        
    print("TERIMAKASIH SUDAH BERMAIN!")
    

    # print(save.save(SAVE_FOLDER, GAME_STATE))


def _start_menu(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    # tampilan masih sementara yang penting jadi dulu wkwjkwk

    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "REGISTER", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LOGIN", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "HELP", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "EXIT", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        ]
        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka: ")
        if option == "1":
            new_game_state = register.run(GAME_STATE)
            if new_game_state["user_list"][0]["id"] != "failed":
                GAME_STATE = new_game_state
        elif option == "2":
            login.run(GAME_STATE)
            if GAME_STATE["user"]:
                return
        elif option == "3":
            _help_menu(GAME_STATE)
        elif option == "4":
            return 
        option = ""

def _start_menu_already_login(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "START GAME", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LOGOUT", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        ]
        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka: ")
        if option == "1":
            GAME_STATE["isPlaying"] = True
            return
        elif option == "2":
            GAME_STATE["user"] = {}
            GAME_STATE['user_monster_inventory'] = []
            GAME_STATE['user_item_inventory'] = {}
            GAME_STATE["isLogin"] = False
            return
        else:
            option = ""

def _main_menu(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    option = ""
    while not option:
        contents = [
        {"type": "BUTTON", "text": "BATTLE", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "ARENA", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "SHOP", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LABORATORY", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "INVENTORY", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "SAVE", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "HELP", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "EXIT", "inner_width": 30, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        ]

        option = ui.render_menu(["TITLE", False], contents, "Pilih menu yang ingin dibuka: ")
        if option == "1":
            battle_result = battle.run(GAME_STATE)
            print(battle_result)
            time.sleep(3)
            if battle_result == "":
                return 
            elif battle_result == "win":
                return 
            elif battle_result == "lose":
                return 
        elif option == "7":
            _help_menu(GAME_STATE)
        elif option == "8":
            GAME_STATE["isPlaying"] = False
            return 
        elif option == "debug":
            print(GAME_STATE)
            _ = input("enter untuk lanjut")
            return
        else:
            option = ""

def _help_menu(GAME_STATE: dict[dict[str, str]]):
    if GAME_STATE['isLogin']:
        if GAME_STATE['user']['role'] == 'admin':
            message = help.help_login_admin(GAME_STATE['user']['username'])
        else:
            message = help.help_login(GAME_STATE['user']['username'])
    else:
        message = help.help_not_login()

    contents = [
        {"type": "TEXT", "text": message, "width": 0, "align": "^", "max_length": 94, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Kembali ke menu", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu(['HELP', True], contents, "Tekan Enter untuk kembali")

    return
        

def _get_folders(directory: str):
    folders = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            folders.append(item)
    return folders

if __name__ == "__main__":
    saved_folders = _get_folders(os.getcwd() + "/data")
    parser = argparse.ArgumentParser()
    parser.add_argument("save_folder", help="insert your save folder name to be loaded by the game", nargs="?")
    args = parser.parse_args()
    
    if os.get_terminal_size()[0] < 100:
        print("Mohon perbesar layar/window Anda sebelum memulai demi pengalaman bermain yang maksimal.")

    elif args.save_folder:
        if args.save_folder in saved_folders:
            SAVE_FOLDER = args.save_folder
            main()
        else:
            print(f"Folder save {args.save_folder} tidak ditemukan!")
    else:
        print("Tidak ada nama folder save yang diberikan!")
        print("Usage: python main.py <nama_folder_save>")
    
