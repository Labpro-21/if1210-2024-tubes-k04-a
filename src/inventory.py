import os

def read_csv(file_path: str) -> list[dict[str, str]]:
    """
    Membaca data dari file csv yang ditentukan dan mengembalikannya sebagai list dari dictionary.
    """
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines.append(line.strip())
    
    parsed_lines = _parse(lines)
    keys = parsed_lines[0]
    formatted_data = []

    for i in range(1, len(parsed_lines)):
        data = {}
        for j in range(len(parsed_lines[i])):
            data[keys[j]] = parsed_lines[i][j]
        formatted_data.append(data)
    
    return formatted_data

def _parse(lines: list[str]) -> list[list[str]]:
    """
    Melakukan parsing string csv dan mengembalikannya sebagai list dari list data per baris.
    """
    parsed_lines = []
    for line in lines:
        parsed_lines.append(line.split(';'))
    return parsed_lines

file_user = str(input())
data_user = read_csv(file_user) # data user berupa id dan currency

file_monster = str(input())
data_monster = read_csv(file_monster) # data monster berupa atk power, def power, dan hp

file_monster_inventory = str(input())
data_monster_inventory = read_csv(file_monster_inventory) # data monster yang dimiliki tiap user dan levelnya

file_item_inventory = str(input())
data_item_inventory = read_csv(file_item_inventory) #  data potion yang dimiliki tiap user dan jumlahnya

def monster_attributes(monster_id: int, level: int) -> list[str]:
    """
    Menampilkan secara singkat maupun detail attribute monster dalam list of strings
    """
    monster = data_monster[monster_id - 1]
    hp = int(monster['hp']) + int(((level - 1) * 0.1) * int(monster['hp']))
    atk_power = int(monster['atk_power']) + int(((level - 1) * 0.1) * int(monster['atk_power']))
    def_power = int(monster['def_power']) + int(((level - 1) * 0.1) * int(monster['def_power']))
    return [monster['type'], atk_power, def_power, hp, level]

def inventory(user_id: int) -> None:
    """
    Menampilkan fitur inventory agent dengan id yang diinput ketika memilih opsi 'Inventory' pada menu help.
    """
    if user_id < 0 or user_id >= len(data_user):
        print(f"User ID {user_id} tidak ditemukan.")
        return

    while True:
        os.system('cls')
        inventory_info = f"============ INVENTORY LIST (User Name: {data_user[user_id]['name']}) ============\n"
        inventory_info += f"Jumlah O.W.C.A. Coin-mu sekarang {data_user[user_id]['currency']}\n"

        num = 1
        inventory_list = []
        for i in range(len(data_monster_inventory)):
            if int(data_monster_inventory[i]['user_id']) == user_id:
                details = monster_attributes(int(data_monster_inventory[i]['monster_id']), int(data_monster_inventory[i]['level']))
                inventory_list.append((f"{num}. Monster       (Name: {details[0]}, Lvl: {details[4]}, HP: {details[3]})", 'monster', details))
                num += 1
        
        for i in range(len(data_item_inventory)):
            if int(data_item_inventory[i]['user_id']) == user_id:
                inventory_list.append((f"{num}. Potion        (Type: {data_item_inventory[i]['type']}, Qty:{data_item_inventory[i]['quantity']})", 'potion', None))
                num += 1

        for item in inventory_list:
            inventory_info += item[0] + '\n'
        
        print(inventory_info)
        item_id = int(input("Ketikkan id untuk menampilkan detail item (0 untuk keluar): "))
        
        if item_id == 0: # keluar dari inventory
            break
        
        if 1 <= item_id <= len(inventory_list):
            item_type = inventory_list[item_id - 1][1]
            os.system('cls')
            if item_type == 'monster': # menampilkan detail monster
                print("\nMonster\n")
                details = inventory_list[item_id - 1][2]
                print(f"Name      : {details[0]}")
                print(f"ATK Power : {details[1]}")
                print(f"DEF Power : {details[2]}")
                print(f"HP        : {details[3]}")
                print(f"Level     : {details[4]}")
            elif item_type == 'potion': # menampilkan detail potion
                print("\nPotion\n")
                potion_details = data_item_inventory[item_id - 1 - len(data_monster_inventory)]
                print(f"Type      : {potion_details['type']}")
                print(f"Quantity  : {potion_details['quantity']}")
            input("\nTekan Enter untuk kembali ke inventory list")
        else: # jika input ID tidak ditemukan pada inventory
            os.system('cls')
            print("Invalid item ID\n")
            input("Tekan Enter untuk kembali ke inventory list")

