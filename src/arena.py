# Import library yang diperlukan
from file_io import read_csv, write_csv
from rng import get
from battle import Battle

# Fungsi untuk mendapatkan hadiah berdasarkan stage
def get_reward(stage):
    rewards = {
        1: 30,
        2: 50,
        3: 100,
        4: 165,
        5: 296,
    }
    return rewards.get(stage, 0)

# Fungsi untuk menginisialisasi data monster dari file CSV
def load_monsters():
    monster_data = read_csv("test_folder", "monster_inventory.csv")
    monsters = []
    for row in monster_data:
        monsters.append({
            "name": row[0],
            "level": int(row[1])
        })
    return monsters

# Fungsi untuk menjalankan sesi latihan
def arena_main():
    # Inisialisasi data
    monsters = load_monsters()
    total_reward = 0
    total_damage_given = 0
    total_damage_taken = 0
    stage = 1
    game_over = False

    # Loop untuk setiap stage
    while stage <= 5:
        # Memilih angka acak
        random_number = get(0, len(monsters) - 1)
        # Memilih monster secara acak
        selected_monster = monsters[random_number]
        monster_name = selected_monster["name"]
        monster_level = selected_monster["level"]

        # Memulai pertarungan
        print(f"Stage {stage}: Melawan {monster_name} (Level {monster_level})")
        battle = Battle()
        result = battle.start_fight(monster_level)

        # Menangani hasil pertarungan
        if result == "win":
            reward = get_reward(stage)
            total_reward += reward
            print(f"Berhasil mengalahkan {monster_name} pada Stage {stage}. Hadiah: {reward} OC")
            stage += 1
        else:
            print(f"Game over! Gagal mengalahkan {monster_name} pada Stage {stage}.")
            game_over = True
            break

    # Menampilkan hasil sesi latihan
    if not game_over:
        print("Sesi latihan selesai! Anda berhasil melewati semua stage.")
    print(f"Total hadiah yang diterima: {total_reward} OC")
    
    # write_csv("scoreboard.csv", [[total_reward, stage-1, total_damage_given, total_damage_taken]])

# Jalankan sesi latihan
arena_main()
