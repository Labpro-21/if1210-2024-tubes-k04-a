# Import library yang diperlukan

if __package__ is None or __package__ == "":
    import rng
    import battle
    from utils import dict_copy, list_copy
else:
    from . import rng
    from . import battle
    from .utils import dict_copy, list_copy


# Fungsi untuk menjalankan sesi latihan
def run(GAME_STATE: dict[str, dict[str, str]]) -> dict[str, int]:
    # Inisialisasi data monsters
    monsters = list_copy(GAME_STATE['monster'])
    result = {"agent": GAME_STATE['user']['username'], "total_reward": 0, "total_damage_given": 0, "total_damage_taken": 0, "total_stage": 0}
    stage = 1
    game_over = False

    # Loop untuk setiap stage
    while stage <= 5:
        # Memilih angka acak
        random_number = rng.get(0, len(monsters) - 1)
        # Memilih monster secara acak
        selected_monster = dict_copy(monsters[random_number])
        selected_monster['level'] = stage
        # Memulai pertarungan
        print(f"Stage {stage}: Melawan {selected_monster['type']} (Level {selected_monster['level']})")
        _ = input("Enter untuk mulai")

        battle_result = battle.run(GAME_STATE, selected_monster)
        
        result['total_damage_given'] += battle_result['damage_given']
        result['total_damage_taken'] += battle_result['damage_taken']

        # Menangani hasil pertarungan
        if battle_result['status'] == "win":
            result['total_reward'] += battle_result['reward']
            result['total_stage'] += 1
            print(battle_result)
            _ = input("Enter untuk lanjut")
            stage += 1
        else:
            print(battle_result)
            print(battle_result)
            game_over = True
            break

    # Menampilkan hasil sesi latihan
    if not game_over:
        print("Sesi latihan selesai! Anda berhasil melewati semua stage.")
        _ = input("Enter untuk lanjut")
    else:
        print("Yah kalah! kacian deh")
        _ = input("Enter untuk lanjut")
    return result

