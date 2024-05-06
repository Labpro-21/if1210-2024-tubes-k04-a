from file_io import read_csv , write_csv
from rng import get

def _monster_attribute(monster_id:int, monster_level:int): 
    """
    Mengkalkulasikan atribut monster sesuai levelnya
    """
    x = read_csv("test_folder", "monster_test1.csv")
    x[monster_id]['atk_power'] = int(int(x[monster_id]['atk_power'])+((((monster_level - 1) * 10)/100)*int(x[monster_id]['atk_power'])))
    x[monster_id]['def_power'] = int(int(x[monster_id]['def_power'])+((((monster_level - 1) * 10)/100)*int(x[monster_id]['def_power'])))
    x[monster_id]['hp'] = int(int(x[monster_id]['hp'])+((((monster_level - 1) * 10)/100)*int(x[monster_id]['hp'])))

    return x

def _atk_power(monster_id:int, monster_level:int):
    """
    Menentukan berapa damage yang akan dikenakan sebelum defense
    """
    y = _monster_attribute(monster_id, monster_level)
    y = int(y[monster_id]['atk_power']) + (((get(-30,30))/100)*int(y[monster_id]['atk_power']))

    return y

def atk_result(selected_monster_id:int, selected_monster_level:int, defending_monster_id:int, defending_monster_level:int):
    """
    Menentukan total damage akhir yang akan dikenakan
    """
    selected = _monster_attribute(selected_monster_id, selected_monster_level)
    defending = _monster_attribute(defending_monster_id, defending_monster_level)
    z = _atk_power(selected_monster_id, selected_monster_level) * ((100-int(defending[defending_monster_id]['def_power']))/100)
    if z<0:
        z=0

    return z

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    for i in range (10):
        print(atk_result(0,3,2,4))
