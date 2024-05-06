import os
from src.file_io import read_csv

file_path = str(input())
data = read_csv(file_path)

def potion(id,level,current_hp) -> list[int] :
    """
    Menerima data id dan level monster untuk mengakses base attribute hp, atk_power, dan def_power monster; selain itu 
    menerima data hp monster saat potion digunakan lalu mengembalikannya setelah penggunaan dalam list of integer
    """
    
    # Perhitungan base hp, atk, dan def monster
    data[id-1]['hp'] = int(int(data[id-1]['hp'])+((((level - 1) * 10)/100)*int(data[id-1]['hp'])))
    data[id-1]['atk_power'] = int(int(data[id-1]['atk_power'])+((((level - 1) * 10)/100)*int(data[id-1]['atk_power'])))
    data[id-1]['def_power'] = int(int(data[id-1]['def_power'])+((((level - 1) * 10)/100)*int(data[id-1]['def_power'])))
    
    base_attributes = [data[id-1]['hp'],data[id-1]['atk_power'],data[id-1]['def_power']]

    # Penggunaan potion saat battle
    atk_power = base_attributes[1]
    def_power = base_attributes[2]

    choice = (str(input("Pilih potion yang ingin digunakan ( Heal / ATK / DEF ) : ")))
    if choice == "Heal" :
        if current_hp + 0.25* base_attributes[0] >= base_attributes[0] :
            current_hp = base_attributes[0]
        else :
            current_hp += 0.25 * base_attributes[0] 
    elif choice == "ATK" :
        atk_power = 1.05 * atk_power 
    elif choice == "DEF" :
        def_power = 1.05 * def_power
    
    return[current_hp,atk_power,def_power]
