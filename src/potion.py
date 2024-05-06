import os

def read_csv(file_path: str) -> list[dict[str, str]]:
    """
    Membaca data dari file csv yang ditentukan dan mengembalikannya sebagai list dari dictionary.
    """
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines.append(line)
    
    parsed_lines = _parse(lines)
    keys = parsed_lines[0]
    formatted_data = []

    for i in range(1, len(parsed_lines)):
        data = {}
        for j in range(len(parsed_lines[i])):
            data[keys[j]] = parsed_lines[i][j]
        formatted_data.append(data)
    
    return formatted_data

def _parse(lines: list[str]) -> list[list[str]]:
    """
    Melakukan parsing string csv dan mengembalikannya sebagai list dari list data per baris.
    """
    parsed_lines = []
    parsed_words = []
    temp = ""

    for line in lines:
        for char in line:
            if char == ';':
                parsed_words.append(temp)
                temp = ""
            elif char == '\n':
                parsed_words.append(temp)
                parsed_lines.append(parsed_words)
                parsed_words = []
                temp = ""
            else:
                temp += char

    if temp:
        parsed_words.append(temp)

    if parsed_words:
        parsed_lines.append(parsed_words)

    return parsed_lines

file_path = "D:\\Uni\\TPB\\Semester 2\\Daspro\\if1210-2024-tubes-k04-a\\monster.csv"
data = read_csv(file_path)

def potion(id,level,hp) -> list[int] :
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
        if hp + 0.25* base_attributes[0] >= base_attributes[0] :
            hp = base_attributes[0]
        else :
            hp += 0.25 * base_attributes[0] 
    elif choice == "ATK" :
        atk_power = 1.05 * atk_power 
    elif choice == "DEF" :
        def_power = 1.05 * def_power
    
    return[hp,atk_power,def_power]
