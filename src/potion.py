def use_potion(choice: str, monster: dict[str, str], base_monster: dict[str, str]) -> dict[str, str] :
    """
    Menerima data id dan level monster untuk mengakses base attribute hp, atk_power, dan def_power monster; selain itu 
    menerima data hp monster saat potion digunakan lalu mengembalikannya setelah penggunaan dalam list of integer
    """


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
        if monster['def_power'] > 50: monster['def_power'] = 50
    
    return monster
