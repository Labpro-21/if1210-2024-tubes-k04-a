import os

# Path direktori parent (path folder repositori)
DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def read_csv(folder_name: str, file_name: str) -> list[dict[str, str]]:
    """
    Membaca data dari file csv yang ditentukan dan mengembalikannya sebagai list dari dictionary.
    """
    file_path = f"{DIR_PATH}/data/{folder_name}/{file_name}"
    text = ""
    with open(file_path, "r") as f:
        text = f.read()

    parsed_lines = _parse(text)
    
    keys = parsed_lines[0]
    formatted_data = []

    for i in range(1, len(parsed_lines)):
        data = {}
        for j in range(len(parsed_lines[i])):
            data[keys[j]] = parsed_lines[i][j]
        formatted_data.append(data)
    
    return formatted_data

def write_csv(folder_name:str, file_name: str, data: list[dict[str, str]]):
    """
    Menulis data ke file csv yang ditentukan.
    """
    file_path = f"{DIR_PATH}/data/{folder_name}/{file_name}"
    
    data_csv = []
    data_csv.append(_to_csv(list(data[0].keys())))

    for i in range(len(data)):
        data_csv.append(_to_csv(list(data[i].values())))

    with open(file_path, 'w') as f:
        for i in range(len(data_csv)):
            f.write(data_csv[i])


def _parse(data: str) -> list[list[str]]:
    """
    Melakukan parsing string csv dan mengembalikan list dari list data per baris.
    """
    parsed_lines = []
    line = []
    temp = ""
    for i in range(len(data)):
        if data[i] == ';':
            line.append(temp)
            temp = ""
        elif data[i] == "\n":
            line.append(temp)
            temp = ""
            parsed_lines.append(line)
            line = []
        else:
            temp += data[i]
    
    if temp: 
        line.append(temp)
    if line:
        parsed_lines.append(line)
    return parsed_lines

def _to_csv(data: list[str]) -> str:
    """
    Mengubah list dari string menjadi string dengan format csv.
    """
    joined = ""
    for i in range(len(data)):
        joined += data[i]
        if i != len(data) - 1:
            joined += ';'
        else:
            joined += '\n'

    return joined

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    x = read_csv("test_folder", "test.csv")
    print(x)

    write_csv("test_folder", "test2.csv", x)

    
