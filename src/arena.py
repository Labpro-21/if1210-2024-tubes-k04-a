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
    result = {"agent": GAME_STATE['user']['username'], "total_reward": 0, "total_damage_given": 0, "total_damage_taken": 0, 'total_hp_healed': 0, "total_stage": 0}
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

        battle_result = battle.run(GAME_STATE, selected_monster, True)
        
        result['total_damage_given'] += battle_result['damage_given']
        result['total_damage_taken'] += battle_result['damage_taken']
        result['total_hp_healed'] += battle_result['hp_healed']

        # Menangani hasil pertarungan
        if battle_result['status'] == "win":
            result['total_reward'] += battle_result['reward']
            result['total_stage'] += 1
            ui.enter_to_continue_menu(f"Teken enter buat lanjut ke stage selanjutnya", "Lanjut")
            stage += 1
        else:
            game_over = True
            break

    # Menampilkan hasil sesi latihan
    _stats_menu(result)
    return result

def _stats_menu(result: dict[str, int]):

    stats = "Sesi latihan selesai! Anda berhasil melewati semua stage.\n" if result['total_stage'] == 5 else ""

    stats += f"""\nStatistik arena

    Total damage diberikan :   {result['total_damage_given']}
    Total damage diterima  :   {result['total_damage_taken']}
    Total HP dipulihkan    :   {result['total_hp_healed']}
    Total stage            :   {result['total_stage']}
    OC didapatkan          :   {result['total_reward']}
        """
    contents = [
        {"type": "TEXT", "text": "", "width": 10, "align": "^", "max_length": 10, "inner_align": "<"},
        {"type": "TEXT", "text": stats, "width": 88, "align": "<", "max_length": 50, "inner_align": "<"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Keluar", "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

    user_inp = ui.render_menu(["MENANG" if result['total_stage'] == 5 else "KALAH", False], contents, "Tekan Enter untuk melanjutkan")


