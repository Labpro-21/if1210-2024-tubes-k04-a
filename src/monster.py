if __package__ is None or __package__ == "":
    from rng import get
else:
    from .rng import get

def _monster_attribute(monster_id:int, monster_level:int, monster_list: list[dict[str, str]]): 
    """
    Mengkalkulasikan atribut monster sesuai levelnya
    """
    x = {}
    for monster in monster_list:
        if monster['id'] == monster_id:
            x = monster

    x['atk_power'] = int(int(x['atk_power'])+((((monster_level - 1) * 10)/100)*int(x['atk_power'])))
    x['def_power'] = int(int(x['def_power'])+((((monster_level - 1) * 10)/100)*int(x['def_power'])))
    if int(x['def_power']) > 50:
        x['def_power'] = 50
    x['hp'] = int(int(x['hp'])+((((monster_level - 1) * 10)/100)*int(x['hp'])))

    return x

def _atk_power(monster_id:int, monster_level:int, monster_list: list[dict[str, str]]):
    """
    Menentukan berapa damage yang akan dikenakan sebelum defense
    """
    y = _monster_attribute(monster_id, monster_level, monster_list)
    y = int(y['atk_power']) + (((get(-30,30))/100)*int(y['atk_power']))

    return y

def atk_result(selected_monster_id:int, selected_monster_level:int, defending_monster_id:int, defending_monster_level:int, monster_list: list[dict[str, str]]):
    """
    Menentukan total damage akhir yang akan dikenakan
    """
    selected = _monster_attribute(selected_monster_id, selected_monster_level, monster_list)
    defending = _monster_attribute(defending_monster_id, defending_monster_level, monster_list)
    z = _atk_power(selected_monster_id, selected_monster_level, monster_list) * ((100-int(defending['def_power']))/100)
    if z<0:
        z=0

    return z

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    for i in range (10):
        print(atk_result(0,3,2,4))
