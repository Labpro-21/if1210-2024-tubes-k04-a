from src import register, login, file_io, save, ui
import argparse
import os

SAVE_FOLDER = ""

def main():
    print(SAVE_FOLDER)


    GAME_STATE = {"user": {},
                  "monster": file_io.read_csv("", "monster.csv"),
                  "monster_inventory": file_io.read_csv(SAVE_FOLDER, "monster_inventory.csv"),
                  "item_inventory": file_io.read_csv(SAVE_FOLDER, "item_inventory.csv"),
                  "monster_shop": file_io.read_csv(SAVE_FOLDER, "monster_shop.csv"),
                  "item_shop": file_io.read_csv(SAVE_FOLDER, "item_shop.csv"),
                  "user_list": file_io.read_csv("", "user.csv")
                  }
    isExit = False
    while not isExit:
        GAME_STATE = _ask_to_login(GAME_STATE)
        print(GAME_STATE)

        if not GAME_STATE["user"]:
            isExit = True
            continue
        isLogin = True
        # while isLogin:
        
    print("TERIMAKASIH SUDAH BERMAIN!")
    

    # SEMUA DATA DARI GAME ADA DI GAME_STATE
    # SILAHKAN TERIMA GAME_STATE SEBAGAI ARGUMEN DI FUNGSI UTAMA FITUR KAMU
    # JANGAN LUPA BUAT RETURN GAME_STATE YANG UDAH DI UPDATE DARI FITUR KAMU

    # SILAHKAN TAMBAH KODE KAMU DIBAWAH INI



    # -------------------------------------
    # print(save.save(SAVE_FOLDER, GAME_STATE))


def _ask_to_login(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    # tampilan masih sementara yang penting jadi dulu wkwjkwk

    option = ""
    while not option:
        buttons = [["REGISTER", 22, "^", 98, "^", True],
                ["LOGIN", 22, "^", 98, "^", True],
                ["HELP", 22, "^", 98, "^", True],
                ["EXIT", 22, "^", 98, "^", True],
               ]
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
            user_data = login.run(GAME_STATE["user_list"])
            if user_data:
                GAME_STATE["user"] = user_data
                return GAME_STATE
        elif option == "4":
            return GAME_STATE
        option = ""

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
    
