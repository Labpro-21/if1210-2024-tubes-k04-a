def help_login(name: str):
    """
    {Spesifikasi : memunculkan laman help}
    {I.S. pemain dalam login page}
    {F.S. pemain dalam help page}

    """
    return f"""
Halo Agent {name}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:

    1. Battle: Bertarung melawan monster secara random 
    2. Arena: Bertarung melawan monster dalam arena sebanyak 5 stage
    3. Shop: Melihat dan membeli item monster atau item dalam shop
    4. Laboratory: Upgrade monster yang dimiliki Agent {name} di inventory
    5. Inventory: Melihat monster dan potion yang dimiliki {name}
    6. Save: Menyimpan data petualangan Agent {name}
    7. Help: Membuka menu help yang sangat membantu ini
    8. Exit: Kembali ke start menu
    9. GAMBA: Pertaruhkan koin kamu dan menjadi kaya dalam satu putaran

Footnote: 
    1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi atau angka yang terdaftar
    2. Jangan lupa untuk memasukkan input yang valid"""

def help_not_login():
    """
    {Spesifikasi : memunculkan laman help}
    {I.S. pemain dalam login page}
    {F.S. pemain dalam help page}

    """
    return """
Kamu belum login sebagai role apapun. Silahkan login terlebih dahulu.

    1. Login: Masuk ke dalam akun yang sudah terdaftar
    2. Register: Membuat akun baru
    3. Help: Membuka menu help yang sangat membantu ini
    3. Exit: Keluar dari permainan ini T_T

Footnote: 
    1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi atau angka yang terdaftar
    2. Jangan lupa untuk memasukkan input yang valid"""

def help_login_admin(name: str):
    """
    {Spesifikasi : memunculkan laman help}
    {I.S. pemain dalam login page}
    {F.S. pemain dalam help page}

    """
    return f"""
Halo Agent {name}. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian. Berikut adalah hal-hal yang dapat kamu lakukan sekarang:

    1. Battle: Bertarung melawan monster secara random 
    2. Arena: Bertarung melawan monster dalam arena sebanyak 5 stage
    3. Shop: Melihat dan membeli item monster atau item dalam shop
    4. Laboratory: Upgrade monster yang dimiliki Agent {name} di inventory
    5. Inventory: Melihat monster dan potion yang dimiliki {name}
    6. Save: Menyimpan data petualangan Agent {name}
    7. Help: Membuka menu help yang sangat membantu ini
    8. Exit: Kembali ke start menu
    9. GAMBA: Pertaruhkan koin kamu dan menjadi kaya dalam satu putaran
    10. Management: Mengatur item yang dijual di shop dan mengatur database monster
  
Footnote: 
    1. Untuk menggunakan aplikasi, silahkan masukkan nama fungsi atau angka yang terdaftar
    2. Jangan lupa untuk memasukkan input yang valid"""

