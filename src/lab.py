from file_io import read_csv, write_csv

def get_monster_type(monster_id: int, monster_types: list[dict[int, str]]) -> int:
    """
    Menentukan nama monster berdasarkan pada monster_id
    """
    for monster_type in monster_types:
        if monster_type['id'] == monster_id:
            return monster_type['type']
    return "Unknown"

def lab_detail(user_id: int, monsters: list[dict[int, int, int]], monster_types: list[dict[int, str]]) -> None:
    """
    Memberikan output berupa list monster yang dimiliki user dan total OC yang dibutuhkan untuk mengupgrade setiap levelnya
    """
    user_monsters = [monster for monster in monsters if monster['user_id'] == str(user_id)]

    print("User's Monsters Inventory:")
    for monster in user_monsters:
        monster_type = get_monster_type(monster['monster_id'], monster_types)
        print(f"{monster['monster_id']} Type: {monster_type}, Level: {monster['level']}")

    print("\nPrice List:")
    for level in range(1, 6):
        needed_currency = 100 * level ** 2
        print(f"Level {level} -> {level + 1 if level < 5 else level}: {needed_currency} coins")

def upgrade_monster(user_id: int, monster_id: int, monsters: list[dict[int, int, int]], users: list[dict[str, str]]) -> None:
    """
    Mengupgrade monster jika memenuhi kriteria level dan oc owned
    """
    for monster in monsters:
        if monster['user_id'] == str(user_id) and monster['monster_id'] == str(monster_id):
            if int(monster['level']) < 5:
                needed_currency = 100 * int(monster['level']) ** 2
                user_currency = int([user['currency'] for user in users if user['id'] == str(user_id)][0])
                if user_currency >= needed_currency:
                    print(f"\n{get_monster_type(monster_id, monster_types)} will be upgraded to level {int(monster['level'])+ 1}.")
                    print(f"The price to upgrade {get_monster_type(monster_id, monster_types)} is {needed_currency} OC.")
                    
                    confirmation = input("Do you want to upgrade this monster? (yes/no): ")
                    if confirmation.lower() == "yes":
                        monster['level'] = str(int(monster['level']) + 1)
                        user_currency -= needed_currency
                        for user in users:
                            if user['id'] == str(user_id):
                                user['currency'] = str(user_currency)
                                break
                        print(f"\n{get_monster_type(monster_id, monster_types)} upgraded successfully! Current level: {monster['level']}")
                        return
                    else:
                        print("Upgrade canceled.")
                        return
                else:
                    print("Insufficient currency for upgrade.")
                    return
            else:
                print("This monster cannot be upgraded anymore.")
                return
    print("Monster not found in inventory.")


users = read_csv("test_folder", "user_test1.csv")
monsters = read_csv("test_folder", "monster_inventory_test1.csv")
monster_types = read_csv("test_folder", "monster_test1.csv")
print("WELCOME TO THE LABORATORY!!")
user_id = 1
lab_detail(user_id, monsters, monster_types)

monster_id = input("Pick a monster to upgrade: ")
upgrade_monster(user_id, monster_id, monsters, users)

write_csv("test_folder", "monster_inventory_test1.csv", monsters)
write_csv("test_folder", "user_test1.csv", users)
