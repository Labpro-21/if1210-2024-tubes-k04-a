# Import library yang diperlukan
from file_io import read_csv, write_csv
from rng import get
from battle import run

# Fungsi untuk mendapatkan hadiah berdasarkan stage
def get_reward(stage: int) -> int:
    rewards = {
        1: 30,
        2: 50,
        3: 100,
        4: 165,
        5: 296,
    }
    return rewards.get(stage, 0)

# Fungsi untuk menginisialisasi data monster dari file CSV
def load_monsters() -> list[dict[str, int]]:
    monster_data = read_csv("", "monster_inventory.csv")
    monsters = []
    for row in monster_data:
        monsters.append({
            "name": row['monster_id'],
            "level": int(row['level'])
        })
    return monsters

# Fungsi untuk menjalankan sesi latihan
def arena_main(GAME_STATE: dict[str,int]) -> None:
    # Inisialisasi data monsters
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
        result = run(GAME_STATE)

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


