# Import library yang diperlukan

if __package__ is None or __package__ == "":
    import rng
    import ui
    import battle
    from utils import dict_copy, list_copy
else:
    from . import rng
    from . import ui
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

        battle_result = battle.run(GAME_STATE, selected_monster)
        
        result['total_damage_given'] += battle_result['damage_given']
        result['total_damage_taken'] += battle_result['damage_taken']

        # Menangani hasil pertarungan
        if battle_result['status'] == "win":
            result['total_reward'] += battle_result['reward']
            result['total_stage'] += 1
            ui.enter_to_continue_menu(f"{str(battle_result)}\n\nTeken enter buat lanjut ke stage selanjutnya", "Lanjut")
            stage += 1
        else:
            ui.enter_to_continue_menu(str(battle_result), "Keluar")
            game_over = True
            break

    # Menampilkan hasil sesi latihan
    if not game_over:
        ui.enter_to_continue_menu("Sesi latihan selesai! Anda berhasil melewati semua stage.", "Keluar")
    else:
        ui.enter_to_continue_menu("Yah kalah! kacian deh", "Keluar")
    return result

