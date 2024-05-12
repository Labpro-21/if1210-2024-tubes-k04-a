if __package__ is None or __package__ == "":
    from rng import get
else:
    from .rng import get

def _atk_power(monster: dict[str, str]):
    """
    Menentukan berapa damage yang akan dikenakan sebelum defense
    """
    y = int(monster['atk_power']) + (((get(0,61) - 30)/100)*int(monster['atk_power']))

    return y

def atk_result(attacking_monster: dict[str, str], defending_monster: dict[str, str]):
    """
    Menentukan total damage akhir yang akan dikenakan
    """
    z = int(_atk_power(attacking_monster) * ((100-int(defending_monster['def_power']))/100))
    if z<0:
        z=0

    return z

def _monster_attribute(monster: dict[str, str]) -> dict[str, str]: 
    """
    Mengkalkulasikan atribut monster sesuai levelnya
    """
    
    monster['atk_power'] = int(1.5 ** (monster['level'] - 1) * monster['atk_power'])
    monster['def_power'] = int(1.5 ** (monster['level'] - 1) * monster['def_power'])
    if int(monster['def_power']) > 50:
        monster['def_power'] = 50
    monster['hp'] = int(1.5 ** (monster['level'] - 1) * monster['hp'])

    return monster

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    for i in range (10):
        print(atk_result(0,3,2,4))
