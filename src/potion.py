def use_potion(choice: str, monster: dict[str, str], monster_list: dict[str, str]) -> dict[str, str] :
    """
    Menerima data id dan level monster untuk mengakses base attribute hp, atk_power, dan def_power monster; selain itu 
    menerima data hp monster saat potion digunakan lalu mengembalikannya setelah penggunaan dalam list of integer
    """

    base_monster = {}
    for m in monster_list:
        if m['id'] == monster['id']:
            base_monster = m
            break
    print(base_monster)
    # Perhitungan base hp, atk, dan def monster
    monster['hp'] = int(int(monster['hp'])+((((monster['level'] - 1) * 10)/100)*int(monster['hp'])))
    monster['atk_power'] = int(int(monster['atk_power'])+((((monster['level'] - 1) * 10)/100)*int(monster['atk_power'])))
    monster['def_power'] = int(int(monster['def_power'])+((((monster['level'] - 1) * 10)/100)*int(monster['def_power'])))
    

    # Penggunaan potion saat battle

    if choice == "healing" :
        if monster['hp'] + 0.25 * base_monster['hp'] >= base_monster['hp'] :
            monster['hp'] = base_monster['hp']
        else :
            monster['hp'] += int(0.25 * base_monster['hp'])
    elif choice == "strength" :
        monster['atk_power'] = int(1.25 * monster['atk_power']) 
    elif choice == "resilience" :
        monster['def_power'] = int(1.25 * monster['def_power'])
    
    return monster
