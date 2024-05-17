from monster_management import _max_space
from file_io import read_csv , write_csv
from utils import is_number , to_lowercase
import os 
import time

def shop_admin():
    data_monster = read_csv("", 'monster.csv')
    monster_shop = read_csv("", 'monster_shop.csv')
    item_shop = read_csv("", 'item_shop.csv')

    os.system('cls||clear')
    atmin = 'siapa'
    print(f"Selamat datang mas {atmin} di database Shop")
    while True:
        data_monster = read_csv("", 'monster.csv')
        monster_shop = read_csv("", 'monster_shop.csv')
        item_shop = read_csv("", 'item_shop.csv')

        print("1. Aku mau ubah data shop Monster\n2. Aku mau ubah data shop Item\n4. Kembali")

        x = input("Pilih aksi: ")
        if x == '1' or '2' or '3':

            if x == '1':
                os.system('cls||clear')
                print(monster_shop) 

                customize = False
                while customize == False:
                    customize_item_action = input("Pilih aksi (tambah/ubah/hapus/kembali): ")
                        
                    if customize_item_action.to_lowercase() == 'tambah':
                        print(":'(")

                    if customize_item_action.to_lowercase() == 'ubah':
                        customize_ubah = False
                        while customize_ubah == False:
                            customize_monster_id = input("Pilih ID monster yang ingin diubah: ")
                            if not customize_monster_id.is_number():
                                print("woilaSh cik masukkin angka buat IDnya")
                            else:
                                print("masukkan id monster: ")

                                type_custom = False
                                while type_custom == False:
                                    stock, price = False, False
                                    # untuk loop tiap tahap agar tidak terjadi error, asumsikan bisa menginput semua jenis type
                                    stock_monster = input("Masukkan stok baru: ")
                                    monster_shop[id]['stock'] = stock_monster

                                    price_monster = input("Masukkan price baru: ")
                                    monster_shop[id]['price'] = price_monster

                                    stock, price = True, True

                            customize = True    

            if x == '2':
                os.system('cls||clear')
                print(item_shop)

                customize = False
                while customize == False:
                    customize_item_action = input("Pilih aksi (tambah/ubah/hapus/kembali): ")
                        
                    if customize_item_action.to_lowercase() == 'tambah':
                        print(":'(")

                    if customize_item_action.to_lowercase() == 'ubah':
                        customize_ubah = False
                        while customize_ubah == False:
                            customize_potion_id = input("Pilih ID potion yang ingin diubah: ")
                            if not customize_potion_id.is_number():
                                print("woilaSh cik masukkin angka buat IDnya")
                            else:
                                print("masukkan id potion: ")
                                # id -> apa nama potion

                                type_custom = False
                                while type_custom == False:
                                    stock, price = False, False
                                    # untuk loop tiap tahap agar tidak terjadi error, asumsikan bisa menginput semua jenis type
                                    stock_potion = input("Masukkan stok baru: ")
                                    item_shop[id]['stock'] = stock_potion

                                    price_potion = input("Masukkan price baru: ")
                                    item_shop[id]['price'] = price_potion

                                    stock, price = True, True

                            customize = True
                                

                    if customize_item_action.to_lowercase() == 'hapus':
                        print(":'(")

                    if customize_item_action.to_lowercase() == 'kembali':
                        break
        

            if x == '4':
                return monster_shop, item_shop
                break

        else:
            print("masukkan hanya dapat berupa integer dengan opsi yang tersedia")

shop_admin()