from file_io import read_csv, write_csv


def potion_available(item_inventory, user_id, potion_type):
    owned = False
    for potion in item_inventory:
        if potion['user_id'] == user_id:
            if potion['type'] == potion_type:
                owned = True
                break
    return owned

def monster_owned(monster_inventory, user_id, monster_id):
    owned = False
    for monster in monster_inventory:
        if (monster['user_id'] == user_id) and (monster['monster_id'] == int(monster_id)):
            owned = True
            break
    return owned

def show_potion(shop_potions):
    print("\nPotions:")
    for potion in shop_potions:
        print(f"Type: {potion['type']}, Stock: {potion['stock']}, Price: {potion['price']} OC, Description: {potion['description']}")

def show_monster(shop_monsters,monster_data):
    print("\nMonsters:")
    for shop_monster in shop_monsters:
        monster_id = int(shop_monster['monster_id'])
        for monster in monster_data:
            if int(monster['id']) == monster_id:
                print(f"ID: {monster['id']}, Type: {monster['type']}, HP: {monster['hp']}, ATK: {monster['atk_power']}, DEF: {monster['def_power']}, Stock: {shop_monster['stock']}, Price: {shop_monster['price']} OC")

def buy_potion(user_currency,user_id, user_data, potion_type, shop_items, amount, item_inventory):
    for item in shop_items:
        if item['type'] == potion_type:
            item_price = int(item['price'])
            if user_currency >= item_price:
                if potion_available(item_inventory, user_id, potion_type) == True:
                    for potion in item_inventory:
                        if potion['user_id'] == str(user_id):
                            if potion['type'] == potion_type:
                                potion['quantity'] = str(int(potion['quantity']) + amount)
                else:
                    item_inventory.append({'user_id': str(user_id), 'type': item['type'], 'quantity': str(amount)})
                user_currency -= item_price * amount
                for user in user_data:
                    if user['id'] == user_id:
                        user['currency'] == user_currency
                        break
                write_csv('test_folder', 'user_test1.csv', user_data)
                print("Purchase successful!")
                item['stock'] = str(int(item['stock']) - amount)
                return True, user_currency
            else:
                print("Insufficient currency!")
                return False, user_currency
    print("Item not found in shop!")
    return False, user_currency

def buy_monster(user_currency,user_id, monster_id, shop_monsters, monster_inventory):
    for monster in shop_monsters:
        if monster['monster_id'] == int(monster_id):
            item_price = int(monster['price'])
            if user_currency >= item_price:
                if monster_owned(monster_inventory, user_id, monster_id) == True:
                    print("Anda sudah memiliki monster ini!")
                    return False, user_currency
                else:
                    monster_inventory.append({'user_id': str(user_id), 'monster_id': monster['monster_id'], 'level': "1"})
                    user_currency -= item_price
                    for user in user_data:
                        if user['id'] == user_id:
                            user['currency'] = user_currency
                            break
                    write_csv('test_folder', 'user_test1.csv', user_data)
                    print("Pembelian berhasil!")
                    monster['stock'] = str(int(monster['stock']) - 1)
                    return True, user_currency
            else:
                print("Insufficient currency!")
                return False, user_currency
    print(monster_id)
    print("Item not found in shop!")
    return False, user_currency

# Read data from CSV files
shop_potions = read_csv('test_folder','item_shop.csv')
shop_monsters = read_csv('test_folder','monster_shop.csv')
user_data = read_csv('test_folder','user_test1.csv')
monster_data = read_csv('test_folder','monster_test1.csv')

# Main function to manage the shop
def manage_shop(user_currency, item_inventory, monster_inventory):
    while True:
        print("\nWelcome to the Shop!")
        print("1. Show Potions")
        print("2. Show Monsters")
        print("3. Buy Item")
        print("4. Exit Shop")
        choice = input("Enter your choice: ")

        if choice == '1':
            show_potion(shop_potions)
        elif choice == '2':
            show_monster(shop_monsters, monster_data)
        elif choice == '3':
            print("Your Currency:", user_currency, "OC")
            item_type = input("Enter the type of item you want to buy (potion/monster): ")
            if item_type == "potion":
                potion_type = input("Jenis potion yang akan dibeli: ")
                amount = int(input("Jumlah potion yang akan dibeli: "))
                buy_potion(user_currency, user_id, potion_type, shop_potions, amount, item_inventory)
            else:
                monster_id = str(input("Masukkan ID monster yang akan dibeli: "))
                buy_monster(user_currency,user_id, monster_id, shop_monsters, monster_inventory)
            
        elif choice == '4':
            print("Exiting Shop...")
            break
        else:
            print("Invalid choice!")

user_currency = int(user_data[0]['currency'])
user_id = user_data[0]['id']
item_inventory = read_csv('test_folder', "item_inventory.csv")
monster_inventory = read_csv('test_folder', 'monster_inventory_test1.csv')
manage_shop(user_currency, item_inventory, monster_inventory)
write_csv('test_folder', 'item_inventory.csv', item_inventory)
write_csv('test_folder', 'monster_inventory.csv', monster_inventory)
write_csv('test_folder', 'item_shop.csv', shop_potions)
write_csv('test_folder', 'monster_shop.csv', shop_monsters)