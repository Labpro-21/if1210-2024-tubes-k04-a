import os
import argparse
from src.menu import start_menu, start_menu_already_login, main_menu, alert_menu
from src import file_io

SAVE_FOLDER = "default_folder"

def main():

    GAME_STATE = {"user": {},
                  "monster": file_io.read_csv(SAVE_FOLDER, "monster.csv"),
                  "monster_inventory": file_io.read_csv(SAVE_FOLDER, "monster_inventory.csv"),
                  "item_inventory": file_io.read_csv(SAVE_FOLDER, "item_inventory.csv"),
                  "monster_shop": file_io.read_csv(SAVE_FOLDER, "monster_shop.csv"),
                  "item_shop": file_io.read_csv(SAVE_FOLDER, "item_shop.csv"),
                  "user_list": file_io.read_csv(SAVE_FOLDER, "user.csv"),
                  "user_monster_inventory": [],
                  "user_item_inventory": [],
                  "isPlaying": False,
                  "isLogin": False,
                  "save_folder": SAVE_FOLDER,
                  }

    isExit = False
    while not isExit:
        start_menu(GAME_STATE)

        if not GAME_STATE["isLogin"]:
            break

        while GAME_STATE["isLogin"]:
            start_menu_already_login(GAME_STATE)
            
            while GAME_STATE["isPlaying"]:
                main_menu(GAME_STATE)


        
    print("TERIMAKASIH SUDAH BERMAIN!")
    

    # print(save.save(SAVE_FOLDER, GAME_STATE))

if __name__ == "__main__":
    saved_folders = file_io.get_folders(os.getcwd() + "/data")
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
        message = """
Tidak ada nama folder save yang diberikan!
Kamu akan bermain dengan save folder default hingga kamu membuat save baru

Jika kamu ingin memulai dengan folder save kamu, jalankan program
dengan perintah seperti berikut: 'python main.py <nama_folder_save_kamu>'

Apakah kamu tetap ingin bermain?
        """
        res = alert_menu(message)
        if res:
            main()
        else:
            print("Tidak ada nama folder save yang diberikan!")
            print("Usage: python main.py <nama_folder_save>")
    
