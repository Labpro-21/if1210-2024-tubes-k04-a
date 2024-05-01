import os

DIR_NAME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def read(file_name: str) -> list[dict[str, str]]:
    file_name = DIR_NAME + "/data/" + file_name
    with open(file_name, "r") as f:
        lines = f.readlines()
    parsed_lines = []
    for line in lines:
        parsed_lines.append(parse(line))
    
    keys = parsed_lines[0]
    formatted_data = []

    for i in range(1, len(parsed_lines)):
        data = {}
        for j in range(len(parsed_lines[i])):
            data[keys[j]] = parsed_lines[i][j]
        formatted_data.append(data)
    
    return formatted_data

def write(file_name: str, data: list[dict[str, str]]):
    file_name = DIR_NAME + "/data/" + file_name
    
    data_csv = []
    data_csv.append(to_csv(list(data[0].keys())))

    for i in range(len(data)):
        data_csv.append(to_csv(list(data[i].values())))

    with open(file_name, 'w') as f:
        for i in range(len(data_csv)):
            f.write(data_csv[i])



def parse(data: str) -> list[str]:
    parsed = []
    temp = ""
    for i in range(len(data)):
        if data[i] == ';':
            parsed.append(temp)
            temp = ""
        elif data[i] == "\n":
            break
        else:
            temp += data[i]
    
    if temp: 
        parsed.append(temp)
    return parsed

def to_csv(data: list[str]) -> str:
    joined = ""
    for i in range(len(data)):
        joined += data[i]
        if i != len(data) - 1:
            joined += ';'
        else:
            joined += '\n'

    return joined

if __name__ == "__main__":
    x = read("test.csv")
    print(x)

    write("test2.csv", x)

    
