import os
from rng import get

# from battle import Battle # Import kelas Battle dari file battle.py

class Monster:
    def __init__(self, type, atk_power, def_power, hp, level):
        self.type = type
        self.atk_power = atk_power
        self.def_power = def_power
        self.hp = hp
        self.level = level

class Arena:
    from file_io import read_csv, write_csv
    def __init__(self):
        # Membaca data monster dari file CSV menggunakan metode read_csv dan menyimpannya dalam atribut monsters
        self.monsters = self.read_csv("monster_inventory.csv")
        # Mendefinisikan hadiah untuk setiap stage
        self.stage_rewards = {1: 30, 2: 50, 3: 100, 4: 150, 5: 200}


    def display_monsters(self):
        # Menampilkan daftar monster yang tersedia untuk dipilih
        print("============ MONSTER LIST ============")
        for i in range(len(self.monsters)):
            monster = self.monsters[i]
            print(f"{i + 1}. {monster.type}")

    def choose_monster(self):
        i = 1
        while i <= len(self.monsters):
            monster = self.monsters[i - 1]
            print(f"{i}. {monster.type}")
            i += 1

        while True:
            # Meminta pengguna memilih monster untuk bertarung
            choice = input("Pilih monster untuk bertarung: ")
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.monsters):
                    return self.monsters[index]  # Mengembalikan monster yang dipilih
            print("Pilihan nomor tidak tersedia!")

    def start_session(self):
        print("Selamat datang di Arena!!")
        # Membuat objek monster agent sebagai representasi pemain
        agent = Monster("Agent X", 30, 20, 200, 1)
        total_reward = 0
        total_damage_given = 0
        total_damage_taken = 0
        stage = 1

        while stage <= 5 and agent.hp > 0:
            print(f"\n============= STAGE {stage} =============")
            monster = rng.choice(self.monsters)
            print(f"\nRAWRRR, Monster {monster.type} telah muncul !!!\n")
            
            # Memulai pertarungan menggunakan kelas Battle dari battle.py
            battle = Battle(agent, monster)
            battle.start_battle()
            
            if agent.hp > 0:
                print(f"Selamat, Anda berhasil mengalahkan monster {monster.type} !!!")
                reward = self.stage_rewards.get(stage, 0)
                total_reward += reward
                print(f"\nSTAGE CLEARED! Anda akan mendapatkan {reward} OC pada sesi ini!")
                agent.hp = 200  # Mereset kesehatan agent untuk stage berikutnya
                stage += 1
            else:
                print(f"Yahhh, Anda dikalahkan oleh monster {monster.type}. Jangan menyerah, coba lagi !!!")
        print("\n============== STATS ==============")
        print(f"Total hadiah      : {total_reward} OC")
        print(f"Jumlah stage      : {stage - 1}")
        print(f"Damage diberikan  : {200 - agent.hp}")
        print(f"Damage diterima   : {total_damage_taken}")

