from file_io import read_csv , write_csv
from rgb import rgb_bg, rgb_text
import os 
import time

def _max_space(data_monster, type_data:str):
    """
    fungsi ini untuk styling tampilan message (berapa banyak space yang dibutuhkan untuk align tabel)
    """
    type_monster = []
    for i in range (len(data_monster)):
        type_monster.append(data_monster[i][type_data])

    for i in range (len(data_monster)):
        max_type = len(str(type_monster[0]))
        if max_type < len(str(type_monster[i])):
            max_type = len(str(type_monster[i]))

    return max_type

def _monster_list(data_monster):
    """
    fungsi ini untuk styling tampilan message list monster
    """
    print((" LIST MONSTER ====").center((51+ (_max_space(data_monster, 'description'))), '='))
    if _max_space(data_monster, 'id') < 2:
        print(str('ID').ljust((_max_space(data_monster, 'id') + 2)), end="| ")
    else:
        print(str('ID').ljust((_max_space(data_monster, 'id') + 1 )), end="| ")

    if _max_space(data_monster, 'type') < 4:
        print(str('Type').ljust((_max_space(data_monster, 'type') + 4 )), end="| ")
    else:
        print(str('Type').ljust((_max_space(data_monster, 'type') + 1 )), end="| ")

    if _max_space(data_monster, 'atk_power') < 9:
        print(str('ATK Power').ljust((_max_space(data_monster, 'atk_power') + 9 )), end="| ")
    else:
        print(str('ATK Power').ljust((_max_space(data_monster, 'atk_power') + 1 )), end="| ")

    if _max_space(data_monster, 'def_power') < 9:
        print(str('DEF Power').ljust((_max_space(data_monster, 'def_power') + 9 )), end="| ")
    else:
        print(str('DEF Power').ljust((_max_space(data_monster, 'def_power') + 1 )), end="| ")

    if _max_space(data_monster, 'hp') < 2:
        print(str('HP').ljust((_max_space(data_monster, 'hp') + 2 )), end="| ")
    else:
        print(str('HP').ljust((_max_space(data_monster, 'hp') + 2 )), end="| ")
    
    print("Description")

    for i in range (len(data_monster)):
        if _max_space(data_monster, 'id') < 2:
            print(str(data_monster[i]['id']).ljust((_max_space(data_monster, 'id') + 2)), end="| ")
        else:
            print(str(data_monster[i]['id']).ljust((_max_space(data_monster, 'id') + 1 )), end="| ")

        if _max_space(data_monster, 'type') < 4:
            print(str(data_monster[i]['type']).ljust((_max_space(data_monster, 'type') + 4)), end="| ")
        else:
            print(str(data_monster[i]['type']).ljust((_max_space(data_monster, 'type') + 1 )), end="| ")

        if _max_space(data_monster, 'atk_power') < 9:
            print(str(data_monster[i]['atk_power']).ljust((_max_space(data_monster, 'atk_power') + 9 )), end="| ")
        else:
            print(str(data_monster[i]['atk_power']).ljust((_max_space(data_monster, 'atk_power') + 1 )), end="| ")

        if _max_space(data_monster, 'def_power') < 9:
            print(str(data_monster[i]['def_power']).ljust((_max_space(data_monster, 'def_power') + 9 )), end="| ")
        else:
            print(str(data_monster[i]['def_power']).ljust((_max_space(data_monster, 'def_power') + 1 )), end="| ")

        if _max_space(data_monster, 'hp') < 2:
            print(str(data_monster[i]['hp']).ljust((_max_space(data_monster, 'hp') + 2 )), end="| ")
        else:
            print(str(data_monster[i]['hp']).ljust((_max_space(data_monster, 'hp') + 2 )), end="| ")
        
        print(data_monster[i]['description'])

    print(("=").center((51 + (_max_space(data_monster, 'description'))), '='))
          
def monster_admin():
    """
    Menjalankan fungsi MONSTER jika dipanggil admin
    """
    data_monster = read_csv('data', 'monster.csv')
    os.system('cls||clear')
    print(r"""
            _.------.                        .----.__
           /         \_.       ._           /---.__  \
          |  O    O   |\\___  //|          /       `\ |
          |  .vvvvv.  | )   `(/ |         | o     o  \|
          /  |     |  |/      \ |  /|   ./| .vvvvv.  |\
         /   `^^^^^'  / _   _  `|_ ||  / /| |     |  | \
       ./  /|         | O)  O   ) \|| //' | `^vvvv'  |/\\
      /   / |         \        /  | | ~   \          |  \\
      \  /  |        / \ Y   /'   | \     |          |   ~
       `'   |  _     |  `._/' |   |  \     7        /
         _.-'-' `-'-'|  |`-._/   /    \ _ /    .    |
    __.-'            \  \   .   / \_.  \ -|_/\/ `--.|_
 --'                  \  \ |   /    |  |              `-
                       \uU \UU/     |  /""")
    print("============================================================")
    print("SELAMAT DATANG DI DATABASE PARA MONSTER !!!")
  
    while True:
        print("1. Tampilkan semua Monster\n2. Tambah Monster baru\n3. Atur stat monster\n4. Kembali")
        x = input("Pilih aksi: ")
        if x == '1' or '2' or '3' or '4':
            name, atk, defense, hp, desc = False, False, False, False, False

            if x == '1':
                _monster_list(data_monster)     

            if x == '2':
                os.system('cls||clear')
                print("Memulai pembuatan monster baru")
                time.sleep(1)
                print(".")
                time.sleep(1)
                print(".")
                time.sleep(1)
                os.system('cls||clear')
                print(r''' 
⣣⢍⡓⢮⢳⣒⡬⣩⡙⠮⣳⡝⣎⡳⡝⢎⣱⣷⢯⣭⢋⠶⠐⠎⠒⠑⠒
⣦⢋⣜⢢⣃⠎⡝⠷⢮⣱⠤⢩⡑⢣⣽⣾⣷⠿⣹⠎⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠧⣗⠬⣐⡠⢜⢢⡕⢦⢢⢤⣀⢀⡀⠀⠀⠀⠀⡀
⣿⣯⣮⣳⣌⠯⣜⡱⢢⢍⠖⢢⡆⣤⣀⡀⢄⠠⣄⣀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢛⢳⣼⣿⣿⡿⢫⠟⠁⠀⢀⣄⣀⢀⡀⠠⠀⠀
⣿⣿⣿⣿⣿⣷⣮⡵⣋⡞⢼⣾⣿⣿⣟⠜⠁⠀⠀⠀⣏⠶⣘⠦⣙⠼⣙⠣⠆⡠⠑⠮⣤⢄⠀⠹⣽⣷⢿⡾⣽⣯⣞⣵⢯⣝⢧⣻⣠⣌
⣿⣿⣿⣿⣿⣿⣽⣿⣷⣾⣿⣿⣿⢯⠀⠀⠀⠀⠀⠰⡘⢎⡵⣉⢆⠳⡈⢆⠡⠀⠁⠀⠠⠘⣇⢀⠘⣿⣯⣿⣿⣶⣿⣿⣿⣾⡿⣶⣿⣿
⢎⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⡟⠁⠀⠀⠀⠀⠀⠐⣩⠒⡴⢡⢎⡱⢌⠂⠔⠈⠀⠀⠀⠀⢈⠓⣖⢽⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣧⢚⣿⣿⣿⣿⣿⣟⣼⣿⣿⣿⠡⠀⠀⠀⠀⠀⠀⡘⣄⠋⡔⢃⠎⡐⠈⠀⡀⠀⠀⠀⠀⠀⠠⣉⢬⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡦⡹⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⢀⡀⠄⣴⢵⣦⣣⢼⠀⠊⠀⠄⠰⠀⠀⠀⠀⠀⠈⠐⠠⢎⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣷⡑⢻⣿⣿⣾⣿⣿⣿⣿⣵⡖⠛⢢⢤⡟⡩⠗⠒⠾⣿⣿⡿⢳⣆⢀⠀⡀⠀⡀⠀⠀⠀⠀⠘⢄⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣧⠉⣿⣿⢿⣿⣿⡻⠛⠁⠀⠀⠀⣪⢵⣁⠀⠁⠀⠁⠐⢉⠣⣘⡓⢀⣂⣴⠾⣛⣒⣐⣂⡆⢄⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣦⡿⢣⣿⣿⢸⠀⣄⡣⠀⠀⠀⠄⡇⡀⠙⠂⠀⠀⠀⠀⢀⣫⠗⠲⡾⠠⠚⠻⠶⠑⠈⠉⠑⢎⠙⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢺⣿⣿⢯⣗⣱⣿⡿⡾⠀⢉⡟⠀⠀⠀⠀⣵⠁⠀⠀⠀⠀⠀⠀⣷⢏⡰⠀⣷⣰⠀⠀⠀⠀⠀⠀⠀⢼⠀⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢧⣻⣿⣼⡇⣼⣿⢷⠣⣶⢸⢡⠀⠀⠀⠀⠈⠁⠂⠀⠀⠀⠠⡞⠁⠤⠀⠀⢹⡎⠣⠀⠀⠀⠀⠀⠀⣳⣾⣿⣿⣿⣿⡿⣽⢿⣿⣿⣿⣿
⣏⡷⣿⣿⡼⣷⣿⣏⡀⡆⣛⠈⢀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⣖⠍⠀⠀⠀⢿⠈⠂⠄⠀⠀⠀⢀⡰⣿⣿⣿⣿⣿⣿⢿⣻⣯⣿⣿⣿⣿
⡾⣵⢻⣏⢾⣿⣿⣿⣷⣿⠽⢀⠂⠌⡠⠀⠀⢀⠀⠀⢮⣁⣤⣄⡀⠀⠀⠀⠈⠣⡀⠀⠀⠀⠀⠰⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣟⣾⢹⣿⢾⣿⣿⣿⣿⣿⠈⠠⢈⠐⡀⠀⣴⠫⢤⢔⣠⣬⣹⠟⠿⡲⣥⢶⣦⣬⢀⢠⠀⠀⠀⠠⣹⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣟⣾⣹⣿⣿⣿⣿⣿⣿⣏⠀⠐⡀⠆⢸⡴⣷⠞⢉⠐⠉⠃⠙⠛⠀⠀⠠⠶⣤⡄⢠⡈⢦⠀⡠⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣏⣶⣫⣿⣿⣿⣿⣿⣿⡟⡀⢀⠐⣈⢺⣱⠁⡿⣿⣷⣶⣤⣄⣀⢀⡀⠀⢀⡀⢙⢶⣿⢸⡇⣭⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣾⣿⣾⣿⣿⣿⣿⣿⣟⠀⠂⠄⡀⠌⠘⠀⠁⢻⣟⠻⢿⣿⠛⠙⢹⣯⠉⠓⡻⢿⢿⠾⢯⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠻⢿⣿⣴⣹⣿⣿⣿⣿⣿⠀⢃⠐⠠⠀⠀⠀⠀⠈⣝⠤⠈⠻⣧⣴⠟⠹⢎⡷⠀⠈⢧⣰⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⣒⣾⣿⣿⣿⣿⣿⣿⣿⠀⠌⡠⠁⠀⠀⠀⠀⠀⠈⠁⠑⠀⡀⢠⠨⠭⠞⠀⠁⣠⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡷⢯⣟⣿⣿⣿⣿⣿⣿⣿⠀⠈⠦⣵⡄⢀⠀⠀⠀⠀⢠⣀⠀⠀⠀⠠⣶⠏⠀⣴⠿⣿⣿⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿⠿⢛⠛⠟⢛⡛⠿
⡛⢧⢻⣿⢿⣿⣿⣿⣿⣿⡥⢐⠢⣄⠙⢷⡀⠀⠀⠀⠀⠙⠿⠻⠛⠓⠃⢀⣼⢏⣾⣿⣿⣿⣏⣷⣽⣾⣿⠿⣏⠙⠄⠂⠀⠈⠀⠀⠀⠂
⡙⣎⠳⣜⢫⠞⡿⢿⣿⣿⣟⣦⠩⣒⠭⣿⣿⣶⣠⣤⣦⣠⢀⢀⠤⣀⣶⡿⣋⣼⣿⣿⡿⠿⢛⠉⡍⢯⡑⠣⠠⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠵⣈⠳⡘⢎⡱⡙⢧⡻⡽⢿⣄⡉⠀⠭⠛⠿⣿⣿⣷⣿⣿⣽⣿⡿⣿⡿⠍⠞⠟⠛⠁⠀⠂⠀⠐⡘⠦⡙⠅⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀
                      ''')
                time.sleep(0.7)
                os.system('cls||clear')
                _monster_list(data_monster)

                while name == False:
                    new_name = input("Masukkan Type / Nama baru: ")
                    for i in range (len(data_monster)):
                        if new_name.lower() == data_monster[i]['type'].lower():
                            print("Nama sudah terdaftar, silahkan coba lagi!")
                            name = False
                            break
                        else:
                            name = True

                while atk == False:
                    new_atk = input("Masukkan ATK Power baru: ")
                    if not new_atk.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        atk = True

                while defense == False:
                    new_def = input("Masukkan DEF Power baru: ")
                    if not new_def.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        if not 0<=int(new_def)<=50:
                            print("DEF Power harus bernilai 0-50, silahkan coba lagi!")
                        else:
                            defense = True

                while hp == False:
                    new_hp = input("Masukkan HP baru: ")
                    if not new_hp.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        hp = True

                while desc == False:
                    new_desc = input("Masukkan deskripsi baru: ")
                    desc = True

                os.system('cls||clear')
                print(("+").center((51 + (_max_space(data_monster, 'description'))), '+'))            
                print("Monster baru telah dibuat!")
                print(f"Type        : {new_name}\nATK Power   : {new_def}\nDEF Power   : {new_def}\nHP          : {new_hp}\nDescription : {new_desc}")
                option = False

                while option == False:
                    add_option = input("Tambahkan monster ke database (Y/N): ")
                    if add_option == 'N' or add_option == 'n' :
                        os.system('cls||clear')
                        print("Monster gagal ditambahkan :(")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                        os.system('cls||clear')
                        
                        print(r"""
                              _.------.                        .----.__
                             /         \_.       ._           /---.__  \
                            |  O    O   |\\___  //|          /       `\ |
                            |  .vvvvv.  | )   `(/ |         | o     o  \|
                            /  |     |  |/      \ |  /|   ./| .vvvvv.  |\
                            /   `^^^^^'  / _   _  `|_ ||  / /| |     |  | \
                        ./  /|         | O)  O   ) \|| //' | `^vvvv'  |/\\
                        /   / |         \        /  | | ~   \          |  \\
                        \  /  |        / \ Y   /'   | \     |          |   ~
                        `'   |  _     |  `._/' |   |  \     7        /
                            _.-'-' `-'-'|  |`-._/   /    \ _ /    .    |
                        __.-'            \  \   .   / \_.  \ -|_/\/ `--.|_
                    --'                  \  \ |   /    |  |              `-
                                        \uU \UU/     |  /""")
                        print("============================================================")
                        print("SELAMAT DATANG DI DATABASE PARA MONSTER !!!")
                        option = True
                    elif add_option == 'Y' or add_option == 'y':
                        os.system('cls||clear')
                        print("Monster baru telah ditambahkan :D")
                        
                        new_monster = {}
                        new_monster['id'] = len(data_monster) + 1
                        new_monster['type'] = new_name
                        new_monster['atk_power'] = new_atk
                        new_monster['def_power'] = new_def
                        new_monster['hp'] = new_hp
                        new_monster['description'] = new_desc

                        data_monster.append(new_monster)
                        option = True
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                        os.system('cls||clear')
                        print(r"""
                              _.------.                        .----.__
                             /         \_.       ._           /---.__  \
                            |  O    O   |\\___  //|          /       `\ |
                            |  .vvvvv.  | )   `(/ |         | o     o  \|
                            /  |     |  |/      \ |  /|   ./| .vvvvv.  |\
                            /   `^^^^^'  / _   _  `|_ ||  / /| |     |  | \
                        ./  /|         | O)  O   ) \|| //' | `^vvvv'  |/\\
                        /   / |         \        /  | | ~   \          |  \\
                        \  /  |        / \ Y   /'   | \     |          |   ~
                        `'   |  _     |  `._/' |   |  \     7        /
                            _.-'-' `-'-'|  |`-._/   /    \ _ /    .    |
                        __.-'            \  \   .   / \_.  \ -|_/\/ `--.|_
                    --'                  \  \ |   /    |  |              `-
                                        \uU \UU/     |  /""")
                        print("============================================================")
                        print("SELAMAT DATANG DI DATABASE PARA MONSTER !!!")
                    else:
                        print("Yang bener aja wak, cuma bisa (Y/N)")
                        print()

            if x == '3':
                time.sleep(0.7)
                os.system('cls||clear')
                _monster_list(data_monster)

                customize = False
                while customize == False:
                    customize_monster_id = input("Pilih ID monster yang ingin diubah: ")
                    if not customize_monster_id.isnumeric():
                        print("woilaSh cik masukkin angka buat IDnya")
                    else:
                        if int(customize_monster_id)>len(data_monster) or int(customize_monster_id)<1:
                            print(f"woilah cik liat idnya cuma dari 1 sampe {len(data_monster)}")
                            
                        else:
                            type_custom = False
                            while type_custom == False:
                                name, atk, defense, hp, desc = False, False, False, False, False
                                customize_monster_type = input("Pilih stat yang ingin dirubah (Type/ATK/DEF/HP/Desc): ")

                                if customize_monster_type.lower() == 'type':
                                    while name == False:
                                        new_name = input("Masukkan Type / Nama baru: ")
                                        for i in range (len(data_monster)):
                                            if new_name.lower() == data_monster[i]['type'].lower():
                                                print("Nama sudah terdaftar, silahkan coba lagi!")
                                                name = False
                                                break
                                            else:
                                                name = True
                                                type_custom = True

                                    

                                elif customize_monster_type.lower() == 'atk':
                                    while atk == False:
                                        new_atk = input("Masukkan ATK Power baru: ")
                                        if not new_atk.isnumeric():
                                            print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                                        else: 
                                            
                                            atk = True
                                            type_custom = True

                                elif customize_monster_type.lower() == 'def':
                                    while defense == False:
                                        new_def = input("Masukkan DEF Power baru: ")
                                        if not new_def.isnumeric():
                                            print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                                        else: 
                                            if not 0<=int(new_def)<=50:
                                                print("DEF Power harus bernilai 0-50, silahkan coba lagi!")
                                            else:
                                                
                                                defense = True
                                                type_custom = True

                                elif customize_monster_type.lower() == 'hp':
                                    while hp == False:
                                        new_hp = input("Masukkan HP baru: ")
                                        if not new_hp.isnumeric():
                                            print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                                        else: 
                                            
                                            hp = True
                                            type_custom = True

                                elif customize_monster_type.lower() == 'desc':
                                    while desc == False:
                                        new_desc = input("Masukkan deskripsi baru: ")
                                        
                                        desc = True
                                        type_custom = True

                                else:
                                    print("Woi masukin input sesuai pilihan (Type/ATK/DEF/HP)")

                                    type_custom = False
                                    
                            customize_commit_bool = False
                            while customize_commit_bool == False:
                                customize_commit = input("Yakin ingin merubah stat (Y/N): ")
                                if customize_commit.lower() == 'n':      
                                    customize_commit_bool = True
                                elif customize_commit.lower() == 'y':
                                    customize_commit_bool = True  
                                    if customize_monster_type.lower() == 'type':
                                        data_monster[int(customize_monster_id)-1]['type'] = new_name
                                    if customize_monster_type.lower() == 'atk':
                                        data_monster[int(customize_monster_id)-1]['atk_power'] = new_atk
                                    if customize_monster_type.lower() == 'def':
                                        data_monster[int(customize_monster_id)-1]['def_power'] = new_def
                                    if customize_monster_type.lower() == 'hp':
                                        data_monster[int(customize_monster_id)-1]['hp'] = new_hp
                                    if customize_monster_type.lower() == 'desc':
                                        data_monster[int(customize_monster_id)-1]['description'] = new_desc
                                else:
                                    print("woilah cik ini udah dikasih tau (Y/N) doang masih aja salah, coba lagi")
                                    customize_commit_bool = False 

                            customize_again_bool = False
                            while customize_again_bool == False:
                                customize_again = input("Ingin merubah stat yang lain (Y/N): ")
                                if customize_again.lower() == 'n':      
                                    customize = True
                                    type_custom = True
                                    customize_again_bool = True
                                elif customize_again.lower() == 'y':
                                    customize = False
                                    type_custom = True
                                    customize_again_bool = True
                                else:
                                    print("woilah cik ini udah dikasih tau (Y/N) doang masih aja salah, coba lagi")
                                    customize_again_bool = False
                                
                time.sleep(0.7)
                os.system('cls||clear')

            if x == '4':
                return data_monster
                break

        else:
            print("masukkan hanya dapat berupa integer dengan opsi yang tersedia")

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    x = monster_admin()