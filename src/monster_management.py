from file_io import read_csv , write_csv

def _max_type(data_monster):
    """
    fungsi ini untuk styling tampilan message (masih belum sempurna)
    """
    type_monster = []
    for i in range (len(data_monster)):
        type_monster.append(data_monster[i]['type'])

        max_type = len(type_monster[0])
        if max_type < len(type_monster[i]):
            max_type = len(type_monster[i])

    return max_type

def monster_admin():
    """
    Menjalankan fungsi MONSTER jika dipanggil admin (styling masih belum sempurna)
    """
    data_monster = read_csv("test_folder", "monster_test1.csv")
    y = _max_type(data_monster)
  
    while True:
        print("===============================================")
        print("SELAMAT DATANG DI DATABASE PARA MONSTER !!!\n1. Tampilkan semua Monster\n2. Tambah Monster baru\n3. Kembali")
        x = input("Pilih aksi: ")
        if x == '1' or '2' or '3':
            name, atk, defense, hp = False, False, False, False
            if x == '1':
                print("=============== LIST MONSTER ==================")
                print("ID | Type", end='')
                for i in range (y-3):
                    print(" ", end="")
                print("| ATK Power | DEF Power | HP")
                for i in range (len(data_monster)):
                    print(f"{data_monster[i]['id']}  | {data_monster[i]['type']} | {data_monster[i]['atk_power']}       | {data_monster[i]['def_power']}        | {data_monster[i]['hp']}")
            if x == '2':
                print("Memulai pembuatan monster baru")

                while name == False:
                    new_name = input("Masukkan Type / Nama: ")
                    for i in range (len(data_monster)):
                        if new_name.lower() == data_monster[i]['type'].lower():
                            print("Nama sudah terdaftar, silahkan coba lagi!")
                            name = False
                            break
                        else:
                            name = True

                while atk == False:
                    new_atk = input("Masukkan ATK Power: ")
                    if not new_atk.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        atk = True

                while defense == False:
                    new_def = input("Masukkan DEF Power: ")
                    if not new_def.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        if not 0<=int(new_def)<=50:
                            print("DEF Power harus bernilai 0-50, silahkan coba lagi!")
                        else:
                            defense = True

                while hp == False:
                    new_hp = input("Masukkan HP: ")
                    if not new_hp.isnumeric():
                        print("Masukkan input bertipe integer positif, silahkan coba lagi!")
                    else: 
                        hp = True
                print("Monster baru telah dibuat!")
                print(f"Type     : {new_name}\nATK Power : {new_def}\nDEF Power : {new_def}\nHP        : {new_hp}")
                option = False

                while option == False:
                    add_option = input("Tambahkan monster ke database (Y/N): ")
                    if add_option == 'N' or add_option == 'n' :
                        print("Monster gagal ditambahkan :(")
                        print()
                        option = True
                    elif add_option == 'Y' or add_option == 'y':
                        print("Monster baru telah ditambahkan :D")
                        print()
                        new_monster = {}
                        new_monster['id'] = len(data_monster) + 1
                        new_monster['type'] = new_name
                        new_monster['atk_power'] = new_atk
                        new_monster['def_power'] = new_def
                        new_monster['hp'] = new_hp

                        data_monster.append(new_monster)
                        option = True
                    else:
                        print("Yang bener aja wak, cuma bisa (Y/N)")
                        print()
            if x == '3':
                return data_monster
                break
        else:
            print("masukkan hanya dapat berupa integer dengan opsi yang tersedia")

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    x = monster_admin()