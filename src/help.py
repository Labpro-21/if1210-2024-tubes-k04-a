from src.file_io import read_csv , write_csv

import src.xxx as jayadi

def help():
    login = jayadi.masukga
    name = jayadi.namausernya
    if login:
        print(f"""=========== HELP ===========

Halo Agent {name}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:

    1. Logout: Keluar dari akun yang sedang digunakan
    2. Monster: Melihat owca-dex yang dimiliki oleh Agent {name}
    3. Potion: Melihat potion yang dimiliki oleh Agent {name}
    4. Inventory: Melihat jenis potion yang tersedia beserta efeknya
    5. Battle: Bertarung melawan monster secara random 
    6. Arena: Bertarung melawan monster dalam arena sebanyak 5 stage
    7. Shop: Melihat dan membeli item monster atau item dalam shop
    8. Laboratory: Upgrade monster yang dimiliki di inventory
    9. Save: Menyimpan data petualangan Agent {name}
    10. Exit: Keluar dari petualangan Agent {name}

Footnote: 
    1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar
    2. Jangan lupa untuk memasukkan input yang valid""")
    else:
        print("""=========== HELP ===========

Kamu belum login sebagai role apapun. Silahkan login terlebih dahulu.

    1. login: Masuk ke dalam akun yang sudah terdaftar
    2. Register: Membuat akun baru

Footnote: 
    1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar
    2. Jangan lupa untuk memasukkan input yang valid""")